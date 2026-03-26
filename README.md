# Amazon Review Analyzer

Classify Amazon product reviews as **positive** or **negative**, then batch-process the same CSV with Spark.

Dataset: [Amazon Review Polarity](https://www.kaggle.com/datasets/kritanjalijain/amazon-reviews) (`polarity`, `title`, `text`). Polarity `1` is negative, `2` is positive.

## Layout

| Path | What it is |
| --- | --- |
| [`notebooks/sentiment-analysis-amazon-reviews.ipynb`](notebooks/sentiment-analysis-amazon-reviews.ipynb) | Pandas + scikit-learn training notebook |
| [`spark_etl/`](spark_etl/) | PySpark job: clean reviews → Parquet by sentiment |
| [`amazon-review-frontend/`](amazon-review-frontend/) | React UI for trying a trained classifier |

## 1. Sentiment notebook

Uses TF-IDF, logistic regression, and K-means on a 50k-row sample so a laptop does not load all 3.6M training rows.

1. Open `notebooks/sentiment-analysis-amazon-reviews.ipynb`.
2. Run the first cell (installs `pandas`, `scikit-learn`, `kagglehub`).
3. Run All. The notebook downloads the Kaggle set into cache; you do not copy CSVs by hand.

## 2. PySpark ETL

Same CSV layout, as a Spark job: filter/label → write partitioned Parquet + a summary table. Details in [`spark_etl/README.md`](spark_etl/README.md).

```sh
python -m unittest discover -s spark_etl/tests -v
python spark_etl/amazon_reviews_etl.py \
  --input spark_etl/fixtures/sample_reviews.csv \
  --output spark_etl/output
```

Needs Java 17 or 21 for Spark. This repo runs **local Spark**. Databricks is a hosted notebook/jobs product that runs Spark; it is not required here.

## 3. Frontend

```sh
cd amazon-review-frontend
npm install
npm run dev
```
