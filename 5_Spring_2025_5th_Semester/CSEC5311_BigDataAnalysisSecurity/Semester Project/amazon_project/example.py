import os
import re
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, col
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

# ---------------------------
# CONFIGURABLE PATHS
# ---------------------------
input_file_path = r"C:\Users\rubva\OneDrive\Desktop\amazon-meta.txt"
output_file_path = r"C:\Users\rubva\GitHub\MS-CSEC\5_Fall_2025_5th_Semester\CSEC5311_BigDataAnalysisSecurity\Semester Project\amazon_project\amazon_recommendations_output.csv"

# Optional: Use absolute path to Python 3.10 executable in your working environment
venv_python_path = r"C:\Users\rubva\AppData\Local\Programs\Python\Python310\python.exe"

# ---------------------------
# FUNCTIONS
# ---------------------------
def load_data(spark, input_file, max_samples=5000):
    print("[INFO] Loading and processing data...")

    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"[ERROR] File not found: {input_file}")

    raw_rdd = spark.sparkContext.textFile(input_file)
    asin_pattern = re.compile(r"^ASIN:\s*(\S+)")
    similar_pattern = re.compile(r"^.*similar:\s*\d+\s+(.*)")

    def parse_lines_partition(partition):
        asin = None
        for line in partition:
            line = line.strip()
            if line.startswith("ASIN:"):
                match = asin_pattern.match(line)
                if match:
                    asin = match.group(1)
            elif line.startswith("similar:") and asin:
                match = similar_pattern.match(line)
                if match:
                    similars = match.group(1).split()
                    for sim in similars:
                        yield (asin, sim)

    parsed_pairs_rdd = raw_rdd.mapPartitions(parse_lines_partition)
    sampled_pairs = parsed_pairs_rdd.take(max_samples)

    print(f"[INFO] Sampled {len(sampled_pairs)} product pairs.")
    if not sampled_pairs:
        raise ValueError("[ERROR] No product pairs found after sampling.")

    parsed_df = spark.createDataFrame(sampled_pairs, ["asin_user", "asin_item"])

    # Unique ASINs to ID mapping
    unique_asins = parsed_df.select("asin_user").union(parsed_df.select("asin_item")).distinct()
    asin_id_df = unique_asins.rdd.zipWithIndex().toDF(["asin", "id"])

    # Join for userId
    user_id_df = asin_id_df.withColumnRenamed("asin", "asin_user").withColumnRenamed("id", "userId")
    item_id_df = asin_id_df.withColumnRenamed("asin", "asin_item").withColumnRenamed("id", "itemId")

    df_with_user_id = parsed_df.join(user_id_df, on="asin_user", how="inner")
    final_df = df_with_user_id.join(item_id_df, on="asin_item", how="inner")

    ratings_df = final_df.select("userId", "itemId").withColumn("rating", lit(1.0))
    return ratings_df

def train_als(ratings_df):
    print("[INFO] Training ALS model...")
    als = ALS(
        maxIter=10,
        regParam=0.1,
        userCol="userId",
        itemCol="itemId",
        ratingCol="rating",
        coldStartStrategy="drop"
    )
    model = als.fit(ratings_df)
    print("[INFO] ALS model training completed.")
    return model

def generate_recommendations(model, user_count=10):
    print("[INFO] Generating recommendations...")
    return model.recommendForAllUsers(10).limit(user_count)

def save_recommendations_to_csv(recommendations_df, output_file_path):
    print(f"[INFO] Saving recommendations to: {output_file_path}")
    pdf = recommendations_df.toPandas()

    flat_rows = []
    for _, row in pdf.iterrows():
        userId = row["userId"]
        for rec in row["recommendations"]:
            flat_rows.append({
                "userId": userId,
                "itemId": rec["itemId"],
                "rating": rec["rating"]
            })

    pd.DataFrame(flat_rows).to_csv(output_file_path, index=False)
    print("[INFO] File saved successfully.")

# ---------------------------
# MAIN
# ---------------------------
def main():
    try:
        # Python version handling
        if os.path.isfile(venv_python_path):
            os.environ['PYSPARK_PYTHON'] = venv_python_path
            os.environ['PYSPARK_DRIVER_PYTHON'] = venv_python_path
        os.environ['SPARK_LOCAL_IP'] = '127.0.0.1'

        spark = SparkSession.builder \
            .appName("AmazonRecommendationSystem") \
            .master("local[*]") \
            .config("spark.driver.memory", "4g") \
            .config("spark.executor.memory", "4g") \
            .getOrCreate()

        spark.sparkContext.setLogLevel("ERROR")
        print("[INFO] Spark session started successfully with 4GB of RAM.")

        ratings_df = load_data(spark, input_file_path)
        model = train_als(ratings_df)
        recommendations_df = generate_recommendations(model)
        save_recommendations_to_csv(recommendations_df, output_file_path)

        print("\n[INFO] Process completed successfully!")

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        try:
            spark.stop()
            print("[INFO] Spark session stopped.")
        except Exception as e:
            print(f"[ERROR] Failed to stop Spark session: {e}")

if __name__ == "__main__":
    main()
