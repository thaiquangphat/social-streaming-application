from pyspark.sql import SparkSession
import yaml

def get_spark_session(app_name="SparkPreprocessing"):
    master = "local[*]"
    partitions = 4

    spark = (
          SparkSession.builder
          .appName(app_name)
          .master(master)
          .config("spark.sql.shuffle.partitions", partitions)
          .config(
              "spark.jars.packages",
              ",".join([
                  "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5",
                  "org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.5.5",
              ])
          )
          .getOrCreate()
      )
    return spark
