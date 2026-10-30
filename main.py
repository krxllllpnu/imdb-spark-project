from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import IntegerType, StringType, StructField, StructType


def main() -> None:
    spark = (
        SparkSession.builder.appName("imdb-spark-project-setup")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.shuffle.partitions", "2")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    try:
        schema = StructType([
            StructField("id", IntegerType(), False),
            StructField("title", StringType(), False),
            StructField("year", IntegerType(), False),
        ])
        frame = spark.createDataFrame(
            [(1, "Spark setup", 2024), (2, "IMDb project", 2025),
             (3, "Ready to analyse", 2026)],
            schema,
        )
        frame.show(truncate=False)
        frame.createOrReplaceTempView("setup_check")
        result = spark.sql(
            "SELECT COUNT(*) AS rows, SUM(id) AS id_sum FROM setup_check"
        ).first()
        if result.rows != 3 or result.id_sum != 6:
            raise RuntimeError(f"Unexpected DataFrame result: {result}")
        if frame.filter(F.col("year") >= 2025).count() != 2:
            raise RuntimeError("DataFrame filter check failed")
        print(f"SETUP_OK: Spark {spark.version}; rows=3; id_sum=6; filtered=2")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
