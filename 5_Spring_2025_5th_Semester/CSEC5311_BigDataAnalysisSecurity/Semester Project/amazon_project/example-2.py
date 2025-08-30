import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pyspark.sql import SparkSession, Row
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
import webbrowser

# Configurable file paths
input_file_path = r"C:\Users\rubva\Documents\amazon-meta.txt"
output_file_path = r"C:\Users\rubva\GitHub\MS-CSEC\5_Fall_2025_5th_Semester\CSEC5311_BigDataAnalysisSecurity\Semester Project\amazon_project"

def load_data(spark, input_file):
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"[ERROR] File not found: {input_file}")

    raw_rdd = spark.sparkContext.textFile(input_file)

    asin_pattern = re.compile(r"^ASIN:\s*(\S+)")
    title_pattern = re.compile(r"^title:\s*(.*)")
    group_pattern = re.compile(r"^group:\s*(.*)")
    similar_pattern = re.compile(r"^similar:\s*\d+\s+(.*)")

    def parse_product_blocks(partition):
        block = []
        for line in partition:
            line = line.strip()
            if line.startswith("Id:"):
                if block:
                    yield block
                    block = []
            block.append(line)
        if block:
            yield block

    asin_to_info = {}
    parsed_pairs = []

    for block in raw_rdd.mapPartitions(parse_product_blocks).collect():
        asin = title = group = None
        similars = []
        for line in block:
            if line.startswith("ASIN:"):
                match = asin_pattern.match(line)
                if match:
                    asin = match.group(1)
            elif line.startswith("title:"):
                title = title_pattern.match(line).group(1)
            elif line.startswith("group:"):
                group = group_pattern.match(line).group(1)
            elif "similar:" in line:
                match = similar_pattern.match(line)
                if match:
                    similars = match.group(1).split()

        if asin:
            asin_to_info[asin] = (title or "N/A", group or "N/A")
            for sim in similars:
                parsed_pairs.append((asin, sim))

    asin_set = set(u for u, i in parsed_pairs) | set(i for u, i in parsed_pairs)
    asin_to_int = {asin: idx for idx, asin in enumerate(asin_set)}
    int_to_asin = {v: k for k, v in asin_to_int.items()}
    mapped_pairs = [(asin_to_int[u], asin_to_int[i]) for u, i in parsed_pairs if u in asin_to_int and i in asin_to_int]

    ratings_df = spark.createDataFrame([Row(userId=u, itemId=i, rating=1.0) for u, i in mapped_pairs])
    return ratings_df, asin_to_int, int_to_asin, asin_to_info

def train_als(ratings_df):
    (train_data, test_data) = ratings_df.randomSplit([0.8, 0.2])
    als = ALS(
        maxIter=10,
        regParam=0.1,
        userCol="userId",
        itemCol="itemId",
        ratingCol="rating",
        coldStartStrategy="drop"
    )
    model = als.fit(train_data)
    predictions = model.transform(test_data)

    evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")
    rmse = evaluator.evaluate(predictions)
    print(f"[INFO] Root-mean-square error = {rmse:.4f}")
    return model, rmse

def generate_recommendations(model, user_count=10):
    return model.recommendForAllUsers(10).limit(user_count)

def save_recommendations_to_csv(recommendations_df, output_file_path, int_to_asin, asin_to_info):
    pdf = recommendations_df.toPandas()
    flattened_rows = []

    for _, row in pdf.iterrows():
        userId = row['userId']
        for rec in row['recommendations']:
            itemId = rec['itemId']
            asin = int_to_asin.get(itemId, "N/A")
            title, group = asin_to_info.get(asin, ("N/A", "N/A"))
            flattened_rows.append({
                'userId': userId,
                'itemId': itemId,
                'ASIN': asin,
                'Title': title,
                'Group': group,
                'PredictedRating': rec['rating']
            })

    final_df = pd.DataFrame(flattened_rows)
    final_df.to_csv(output_file_path, index=False)
    print(f"[INFO] Recommendations saved to {output_file_path}")

def visualize_recommendations(output_file_path):
    df = pd.read_csv(output_file_path)

    # Top 10 Recommended Products
    top_items = df['Title'].value_counts().head(10)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=top_items.values, y=top_items.index)
    plt.title('Top 10 Most Recommended Products')
    plt.xlabel('Recommendation Count')
    plt.ylabel('Product Title')
    plt.tight_layout()
    plt.show()

    # User-Item Heatmap
    sample = df.sample(n=min(1000, len(df)))
    pivot = sample.pivot_table(index='userId', columns='itemId', values='PredictedRating', fill_value=0)
    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot, cmap="YlGnBu", cbar_kws={'label': 'Predicted Rating'})
    plt.title('User-Item Recommendation Heatmap')
    plt.tight_layout()
    plt.show()

def main():
    spark = None
    try:
        spark = SparkSession.builder \
            .appName("AmazonRecommendationSystem") \
            .config("spark.driver.memory", "4g") \
            .config("spark.executor.memory", "4g") \
            .getOrCreate()

        spark.sparkContext.setLogLevel("ERROR")
        print("[INFO] Spark session started.")
        webbrowser.open("http://localhost:4040")

        ratings_df, asin_to_int, int_to_asin, asin_to_info = load_data(spark, input_file_path)
        model, rmse = train_als(ratings_df)
        recommendations_df = generate_recommendations(model)
        save_recommendations_to_csv(recommendations_df, output_file_path, int_to_asin, asin_to_info)
        visualize_recommendations(output_file_path)

        input("[INFO] Press ENTER to stop Spark and exit...")

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        if spark:
            spark.stop()
            print("[INFO] Spark session stopped.")

if __name__ == "__main__":
    main()
