import os
import re
import pandas as pd
from pyspark.sql import SparkSession, Row
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

# ---------------------------
# CONFIGURABLE PATHS
# ---------------------------
input_file_path = "/mnt/c/Users/rubva/GitHub/WSL_Ubuntu_20.04/amazon-meta.txt"
output_file_path = "/mnt/c/Users/rubva/GitHub/WSL_Ubuntu_20.04/amazon_recommendations_output.csv"

# ---------------------------
# FUNCTIONS
# ---------------------------
def load_data(spark, input_file):
    print("[INFO] Loading and processing data...")

    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"[ERROR] File not found: {input_file}")

    raw_rdd = spark.sparkContext.textFile(input_file)

    asin_pattern = re.compile(r"^ASIN:\s*(\S+)")
    similar_pattern = re.compile(r"^.*similar:\s*\d+\s*(.*)")

    # Parse ASIN and similar products together
    def parse_lines(lines):
        asin = None
        pairs = []
        for line in lines:
            line = line.strip()
            if line.startswith("ASIN:"):
                match = asin_pattern.match(line)
                if match:
                    asin = match.group(1)
            elif "similar:" in line and asin:
                match = similar_pattern.match(line)
                if match:
                    similars = match.group(1).split()
                    for sim in similars:
                        pairs.append((asin, sim))
        return pairs

    # Group lines to reconstruct each product block
    parsed_pairs = raw_rdd.mapPartitions(lambda partition: parse_lines(partition)).collect()

    print(f"[INFO] Total Product Pairs Parsed: {len(parsed_pairs)}")

    if not parsed_pairs:
        raise ValueError("[ERROR] No product pairs found after parsing. Check file format.")

    # Map ASINs to integer IDs
    asin_set = set()
    for u, i in parsed_pairs:
        asin_set.add(u)
        asin_set.add(i)

    asin_to_int = {asin: idx for idx, asin in enumerate(asin_set)}
    mapped_pairs = [(asin_to_int[u], asin_to_int[i]) for u, i in parsed_pairs]

    ratings_df = spark.createDataFrame([Row(userId=int(u), itemId=int(i), rating=1.0) for u, i in mapped_pairs])
    return ratings_df, asin_to_int


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
    user_recs = model.recommendForAllUsers(10)
    return user_recs.limit(user_count)


def save_recommendations_to_csv(recommendations_df, output_file_path):
    print(f"[INFO] Saving recommendations to: {output_file_path}")
    pdf = recommendations_df.toPandas()

    # Flatten recommendations
    flattened_rows = []
    for _, row in pdf.iterrows():
        userId = row['userId']
        recs = row['recommendations']
        for rec in recs:
            flattened_rows.append({
                'userId': userId,
                'itemId': rec['itemId'],
                'rating': rec['rating']
            })

    final_df = pd.DataFrame(flattened_rows)
    final_df.to_csv(output_file_path, index=False)
    print("[INFO] File saved successfully.")


# ---------------------------
# MAIN
# ---------------------------
def main():
    try:
        # Initialize Spark session with 4GB RAM
        spark = SparkSession.builder \
            .appName("AmazonRecommendationSystem") \
            .config("spark.driver.memory", "4g") \
            .config("spark.executor.memory", "4g") \
            .getOrCreate()

        spark.sparkContext.setLogLevel("ERROR")  # Suppress INFO/WARN logs

        print("[INFO] Spark session started successfully with 4GB of RAM.")

        # Load data
        ratings_df, id_mapping = load_data(spark, input_file_path)

        # Train ALS model
        model = train_als(ratings_df)

        # Generate recommendations
        recommendations_df = generate_recommendations(model)

        # Save recommendations to CSV
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
