from ultis.spark import get_spark_session
from processing.cleaner import clean_text_udf
from processing.keyword_extractor import keyword_extractor_udf
from processing.embedder import embedder_udf
from pyspark.sql.functions import col

def main():
    spark = get_spark_session("SparkPreprocessing")

    df = spark.read.option("multiLine", True).json(r"/opt/spark-data/raw/sample.json")
    df.printSchema()

    df = df.withColumn("clean_text", clean_text_udf(col("text")))
    df = df.withColumn("keywords", keyword_extractor_udf(col("clean_text")))
    df = df.withColumn("embedding", embedder_udf(col("clean_text")))

    df.write.mode("overwrite").json(r"/opt/spark-data/processed/")
    spark.stop()

if __name__ == "__main__":
    main()