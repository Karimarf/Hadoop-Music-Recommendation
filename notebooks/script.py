from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Analyse CSV") \
    .master("spark://spark-master:7077") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://hadoop-namenode1:8020") \
    .getOrCreate()

df = spark.read.option("header", "true").csv("hdfs://hadoop-namenode1:8020/user/root/donnees/data.csv")
df.show()
