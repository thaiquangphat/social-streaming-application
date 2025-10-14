from pyspark.sql import SparkSession
import yaml

def get_spark_session(app_name="SparkPreprocessing"):
    master = "local[*]"
    partitions = 4

    spark = (SparkSession.builder
             .appName(app_name)
             .master(master)
             .config("spark.sql.shuffle.partitions", partitions)
             .getOrCreate())
    return spark
