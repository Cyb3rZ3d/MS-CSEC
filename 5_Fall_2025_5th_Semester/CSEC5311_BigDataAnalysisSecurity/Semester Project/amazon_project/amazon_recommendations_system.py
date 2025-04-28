# amazon_recommendation_system.py

from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql import Row
import re

# Function to create Spark session (limited to 2g memory)
def create_spark_session():
    spark = SparkSession.builder \
        .appName("Amazon Co-Purchase Recommendation System") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()
    return spark

# Function to load and preprocess data
def load_and_preprocess_data(file_path):
    print("[INFO] Loading and preprocessing data...")
    user_product_pairs = []
    with open(file_path, 'r', encoding='latin-1') as file:
        current_product = None
        for line in file:
            line = line.strip()
            if line.startswith("Id"):
                continue
            if line.startswith("ASIN"):
                asin_match = re.match(r'ASIN:\s+(\S+)', line)
                if asin_match:
                    current_product = asin_match.group(1)
            if line.startswith("  similar") and current_product:
                parts = line.split()
                similar_products = parts[2:]  # Skip 'similar' count
                for similar_product in similar_products:
                    user_product_pairs.append(Row(user=current_product, item=similar_product, rating=1.0))
    print(f"[INFO] Total co-purchase pairs extracted: {len(user_product_pairs)}")
    return user_product_pairs

# Function to train ALS model
def train_als_model(ratings_df):
    print("[INFO] Training ALS model...")
    als = ALS(
        maxIter=10,
        regParam=0.1,
        userCol="user_index",
        itemCol="item_index",
        ratingCol="rating",
        coldStartStrategy="drop",
        nonnegative=True
    )
    model = als.fit(ratings_df)
    return model

# Function to evaluate the model
def evaluate_model(model, ratings_df):
    print("[INFO] Evaluating model...")
    predictions = model.transform(ratings_df)
    evaluator = RegressionEvaluator(
        metricName="rmse",
        labelCol="rating",
        predictionCol="prediction"
    )
    rmse = evaluator.evaluate(predictions)
    print(f"[RESULT] Root-mean-square error = {rmse:.4f}")

# Function to show sample recommendations
def show_recommendations(model, user_index_mapping, num_recommendations=5):
    print("[INFO] Generating sample recommendations...")
    users = user_index_mapping.select("user_index").limit(5).collect()
    for user_row in users:
        user_id = user_row.user_index
        recommendations = model.recommendForUserSubset(user_index_mapping.filter(user_index_mapping.user_index == user_id), num_recommendations)
        recommendations.show(truncate=False)

# Main function
def main():
    file_path = "C:\Users\rubva\Documents\amazon-meta.txt"

    spark = create_spark_session()

    user_product_pairs = load_and_preprocess_data(file_path)
    ratings_df = spark.createDataFrame(user_product_pairs)

    # Index users and items to integers (ALS needs numeric IDs)
    from pyspark.ml.feature import StringIndexer

    user_indexer = StringIndexer(inputCol="user", outputCol="user_index")
    item_indexer = StringIndexer(inputCol="item", outputCol="item_index")

    ratings_df = user_indexer.fit(ratings_df).transform(ratings_df)
    ratings_df = item_indexer.fit(ratings_df).transform(ratings_df)

    model = train_als_model(ratings_df)
    evaluate_model(model, ratings_df)

    # Prepare user index mapping to sample recommendations
    user_index_mapping = ratings_df.select("user", "user_index").distinct()
    show_recommendations(model, user_index_mapping)

    spark.stop()

if __name__ == "__main__":
    main()
