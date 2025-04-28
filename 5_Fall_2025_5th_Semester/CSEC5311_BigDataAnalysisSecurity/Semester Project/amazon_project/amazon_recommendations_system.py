# amazon_recommendations_system.py

import os
import random
import re
import argparse

from pyspark.sql import SparkSession, Row
from pyspark.ml.feature import StringIndexer
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

# --- ENVIRONMENT FORCE TO LOCAL ---
os.environ["SPARK_MASTER_HOST"] = "127.0.0.1"
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"

# --- Create Spark Session ---
def create_spark_session():
    spark = SparkSession.builder \
        .appName("Amazon Co-Purchase Recommendation System") \
        .master("local[2]") \
        .config("spark.driver.memory", "4g") \
        .config("spark.executor.memory", "2g") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("DEBUG")  # Enable debug logging
    return spark

def parse_args():
    parser = argparse.ArgumentParser(description="Amazon Recommendation System")
    parser.add_argument("--file_path", type=str, default="amazon-meta.txt", help="Path to the input data file")
    parser.add_argument("--limit", type=int, default=1000, help="Limit the number of rows to process")
    return parser.parse_args()

# --- Load and preprocess the amazon-meta.txt data ---
def load_and_preprocess_data(file_path):
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        exit(1)
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
            if "similar:" in line and current_product:
                parts = line.split()
                if len(parts) > 2:
                    similar_products = parts[2:]
                    for similar_product in similar_products:
                        user_product_pairs.append(Row(user=current_product, item=similar_product, rating=1.0))

    print(f"[INFO] Total co-purchase pairs extracted: {len(user_product_pairs)}")

    if not user_product_pairs:
        print("[ERROR] No user-product pairs found. Exiting program.")
        exit(1)

    if len(user_product_pairs) > 50:
        sample_fraction = 0.02
        user_product_pairs = random.sample(user_product_pairs, int(len(user_product_pairs) * sample_fraction))
    return user_product_pairs

# --- Train ALS Model ---
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

# --- Evaluate Model ---
def evaluate_model(model, ratings_df):
    print("[INFO] Evaluating model...")
    predictions = model.transform(ratings_df)
    evaluator = RegressionEvaluator(
        metricName="rmse",
        labelCol="rating",
        predictionCol="prediction"
    )
    rmse = evaluator.evaluate(predictions)
    print(f"[RESULT] Root-mean-square error (RMSE) = {rmse:.4f}")

# --- Show Sample Recommendations ---
def show_recommendations(spark, model, user_index_mapping, num_recommendations=5):
    users = user_index_mapping.select("user_index").limit(5).collect()
    for user_row in users:
        user_id = user_row.user_index
        recommendations = model.recommendForUserSubset(
            spark.createDataFrame([Row(user_index=user_id)]),
            num_recommendations
        )
        recommendations.show(truncate=False)

# --- Main Program ---
def main():
    args = parse_args()
    file_path = args.file_path

    spark = create_spark_session()
    user_product_pairs = load_and_preprocess_data(file_path)
    ratings_df = spark.createDataFrame(user_product_pairs).limit(args.limit)

    if ratings_df.rdd.isEmpty():
        print("[ERROR] No data available for training. Exiting program.")
        spark.stop()
        exit(1)

    ratings_df.cache()  # Cache only once
    user_indexer = StringIndexer(inputCol="user", outputCol="user_index")
    item_indexer = StringIndexer(inputCol="item", outputCol="item_index")
    user_indexer_model = user_indexer.fit(ratings_df)
    item_indexer_model = item_indexer.fit(ratings_df)
    ratings_df = user_indexer_model.transform(ratings_df)
    ratings_df = item_indexer_model.transform(ratings_df)

    model = train_als_model(ratings_df)
    evaluate_model(model, ratings_df)
    user_index_mapping = ratings_df.select("user", "user_index").distinct()
    show_recommendations(spark, model, user_index_mapping)
    spark.stop()

if __name__ == "__main__":
    main()
