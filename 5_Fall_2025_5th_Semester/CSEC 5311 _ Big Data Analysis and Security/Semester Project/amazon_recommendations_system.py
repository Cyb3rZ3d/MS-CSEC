# amazon_recommendation_system.py

# Step 1: Import necessary libraries
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.functions import col
import re
import os

# Step 2: Prompt user for file path
#file_path = input("Enter the full path to your amazon-meta.txt file: ").strip()
file_path = input("Enter the full path to your amazon-meta.txt file: ").strip().strip('"')

if not os.path.isfile(file_path):
    print("[ERROR] Invalid file path. Please check and try again.")
    exit(1)

# Step 3: Initialize Spark Session
spark = SparkSession.builder \
    .appName("Amazon Co-Purchase Recommendation System") \
    .getOrCreate()

# Step 4: Load Dataset
rdd = spark.sparkContext.textFile(file_path)

# Check if file was loaded correctly
if rdd.isEmpty():
    print("[ERROR] The file was not loaded. Please check the file path and ensure the file exists.")
    spark.stop()
    exit(1)
else:
    print("[INFO] File loaded successfully. Line count:", rdd.count())

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

        elif similar_match and current_id is not None:
            similars = similar_match.group(1).split()
            for similar_id in similars:
                try:
                    products.append((current_id, int(similar_id), 1))  # Using '1' as dummy rating
                except ValueError:
                    continue

    return products

# Parse the dataset
parsed_data = parse_amazon_meta(rdd)

# Show a sample of parsed data
if parsed_data:
    print("Sample parsed data:", parsed_data[:5])
else:
    print("No data parsed. Check file format or parsing logic.")

# Create a DataFrame
columns = ["user", "item", "rating"]
df = spark.createDataFrame(parsed_data, columns)

# Show the DataFrame structure
df.show(5)

# Step 5: Split the data into training and test sets
(training, test) = df.randomSplit([0.8, 0.2], seed=42)

# Step 6: Build the ALS model
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

# Step 7: Evaluate the model
predictions = model.transform(test)
evaluator = RegressionEvaluator(
    metricName="rmse",
    labelCol="rating",
    predictionCol="prediction"
)
rmse = evaluator.evaluate(predictions)
print(f"Root-mean-square error = {rmse}")

# Step 8: Generate top-10 product recommendations for all users
user_recs = model.recommendForAllUsers(10)

# Save recommendations to text file for Power BI visualization
user_recs.write.mode("overwrite").text("./user_recommendations.txt")

# Step 9: Stop Spark session
spark.stop()

# ---------------------------
# How to Run This Program:
# 1. Make sure you have PySpark installed.
#    pip install pyspark
# 2. Open a terminal inside VSCode.
# 3. Execute:
#    python amazon_recommendation_system.py
# 4. Enter the full path to the amazon-meta.txt file when prompted.
#
# Output:
# - RMSE printed on terminal.
# - 'user_recommendations.txt' file generated for Power BI.
# ---------------------------
