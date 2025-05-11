from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("Test HDFS Read") \
        .master("spark://localhost:7077") \
        .config("spark.hadoop.fs.defaultFS", "hdfs://localhost:8020") \
        .getOrCreate()
    # Read the CSV file from HDFS

    df = spark.read.option("header", "true").csv("hdfs://localhost:8020/user/root/donnees/data.csv")
    df.show()
