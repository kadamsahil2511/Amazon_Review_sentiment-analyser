#!/usr/bin/env python3
"""PySpark ETL for Amazon review polarity CSVs.

Extract: read headerless CSV (polarity, title, text) — the Kaggle Amazon Reviews
Polarity layout used by the pandas notebook.

Transform: clean text, map 1/2 polarity to negative/positive, drop empty rows,
add title/body length.

Load: write Parquet partitioned by sentiment, plus a small aggregate summary.

Run locally (same job shape as a Databricks notebook / scheduled job):

    python spark_etl/amazon_reviews_etl.py \\
        --input spark_etl/fixtures/sample_reviews.csv \\
        --output spark_etl/output
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, StringType, StructField, StructType

SCHEMA = StructType(
    [
        StructField("polarity", IntegerType(), False),
        StructField("title", StringType(), True),
        StructField("text", StringType(), True),
    ]
)


def build_spark(app_name: str = "amazon-reviews-etl") -> SparkSession:
    return (
        SparkSession.builder.appName(app_name)
        .master("local[*]")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )


def transform(reviews):
    cleaned = (
        reviews.withColumn("title", F.trim(F.col("title")))
        .withColumn("text", F.trim(F.regexp_replace(F.col("text"), r"\\n", " ")))
        .withColumn(
            "sentiment",
            F.when(F.col("polarity") == 1, F.lit("negative"))
            .when(F.col("polarity") == 2, F.lit("positive"))
            .otherwise(F.lit(None)),
        )
        .withColumn("title_len", F.length(F.col("title")))
        .withColumn("text_len", F.length(F.col("text")))
        .withColumn("word_count", F.size(F.split(F.col("text"), r"\s+")))
    )
    return cleaned.filter(
        F.col("sentiment").isNotNull()
        & (F.col("text_len") >= 8)
        & F.col("text").isNotNull()
    )


def summarize(reviews):
    return (
        reviews.groupBy("sentiment")
        .agg(
            F.count("*").alias("review_count"),
            F.round(F.avg("text_len"), 1).alias("avg_text_len"),
            F.round(F.avg("word_count"), 1).alias("avg_word_count"),
        )
        .orderBy("sentiment")
    )


def run(input_path: str, output_dir: str, limit: int | None) -> None:
    spark = build_spark()
    source = spark.read.csv(input_path, schema=SCHEMA, header=False)
    if limit is not None:
        source = source.limit(limit)

    reviews = transform(source)
    summary = summarize(reviews)

    out = Path(output_dir)
    reviews_path = str(out / "reviews_clean")
    summary_path = str(out / "sentiment_summary")

    reviews.write.mode("overwrite").partitionBy("sentiment").parquet(reviews_path)
    summary.write.mode("overwrite").parquet(summary_path)
    summary.show(truncate=False)

    print(f"Wrote partitioned reviews to {reviews_path}")
    print(f"Wrote sentiment summary to {summary_path}")
    spark.stop()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Amazon reviews PySpark ETL")
    parser.add_argument(
        "--input",
        default=str(Path(__file__).parent / "fixtures" / "sample_reviews.csv"),
        help="Headerless CSV: polarity,title,text",
    )
    parser.add_argument(
        "--output",
        default=str(Path(__file__).parent / "output"),
        help="Directory for Parquet outputs",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional row cap (use on the full 3.6M Kaggle train.csv)",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    run(args.input, args.output, args.limit)
