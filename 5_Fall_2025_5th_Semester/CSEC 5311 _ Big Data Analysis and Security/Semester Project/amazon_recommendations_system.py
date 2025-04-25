# amazon_recommendation_system.py

# Step 1: Import necessary libraries
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.functions import col
import re

# Step 2: Initialize Spark Session
spark = SparkSession.builder \
    .appName("Amazon Co-Purchase Recommendation System") \
    .getOrCreate()

# Step 3: Load and Preprocess Dataset
# Define the updated file path to your dataset
file_path = r"C:\Users\rubva\OneDrive - Texas A&M University-San Antonio\TAMUSA\MS CyberSecurity\'5 _ Spring 2025'\'Big Data Analysis and Security _ CSEC 5311'\Project\amazon-meta.txt\amazon-meta.txt"

# Read the file into RDD
rdd = spark.sparkContext.textFile(file_path)

# Helper function to parse the file
def parse_amazon_meta(rdd):
    product_id_pattern = re.compile(r"Id:\s+(\d+)")
    similar_pattern = re.compile(r"similar:\s+\d+\s+(.*)")

    products = []

    current_id = None
    for line in rdd.collect():
        product_match = product_id_pattern.search(line)
        similar_match = similar_pattern.search(line)

        if product_match:
            current_id = int(product_match.group(1))

        if similar_match and current_id is not None:
            similars = similar_match.group(1).split()
            for similar_id in similars:
                products.append((current_id, int(similar_id), 1))  # Using '1' as dummy rating
    return products

# Parse the dataset
parsed_data = parse_amazon_meta(rdd)

# Create a DataFrame
columns = ["user", "item", "rating"]
df = spark.createDataFrame(parsed_data, columns)

# Step 4: Split the data into training and test sets
(training, test) = df.randomSplit([0.8, 0.2], seed=42)

# Step 5: Build the ALS model
als = ALS(
    maxIter=10,
    regParam=0.1,
    userCol="user",
    itemCol="item",
    ratingCol="rating",
    coldStartStrategy="drop",
    nonnegative=True
)

# Train the model
model = als.fit(training)

# Step 6: Evaluate the model
predictions = model.transform(test)
evaluator = RegressionEvaluator(
    metricName="rmse",
    labelCol="rating",
    predictionCol="prediction"
)
rmse = evaluator.evaluate(predictions)
print(f"Root-mean-square error = {rmse}")

# Step 7: Generate top-10 product recommendations for all users
user_recs = model.recommendForAllUsers(10)

# Save recommendations to CSV for Power BI visualization
user_recs.write.mode("overwrite").csv("./user_recommendations.csv")

# Step 8: Stop Spark session
spark.stop()

# ---------------------------
# How to Run This Program:
# 1. Make sure you have PySpark installed.
#    pip install pyspark
# 2. Open a terminal inside VSCode.
# 3. Execute:
#    python amazon_recommendation_system.py
#
# Output:
# - RMSE printed on terminal.
# - 'user_recommendations.csv' file generated for Power BI.
# ---------------------------