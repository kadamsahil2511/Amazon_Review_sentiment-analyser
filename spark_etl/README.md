# spark_etl

PySpark batch job for Amazon review polarity CSVs.

```
extract   headerless CSV  →  polarity, title, text
transform clean text, map 1/2 → negative/positive, drop empty / polarity-3 rows
load      Parquet partitioned by sentiment + a summary table
```

## Layout

| Path | Role |
| --- | --- |
| `amazon_reviews_etl.py` | Spark job (`transform`, `summarize`, CLI) |
| `transforms.py` | Row helpers shared with tests |
| `fixtures/sample_reviews.csv` | 12-row fixture (10 usable reviews) |
| `tests/test_transforms.py` | Unit tests (no Spark cluster) |
| `requirements-spark.txt` | `pyspark` |

## Setup

Python 3.10+ and **Java 17 or 21**. Then:

```sh
python -m venv spark_etl/.venv
spark_etl/.venv/bin/pip install -r spark_etl/requirements-spark.txt
```

## Run

From the repo root:

```sh
python -m unittest discover -s spark_etl/tests -v

python spark_etl/amazon_reviews_etl.py \
  --input spark_etl/fixtures/sample_reviews.csv \
  --output spark_etl/output
```

Writes:

- `spark_etl/output/reviews_clean/sentiment=positive/` and `.../negative/`
- `spark_etl/output/sentiment_summary/`

Full Kaggle `train.csv` (after the notebook download):

```sh
python spark_etl/amazon_reviews_etl.py \
  --input /path/to/train.csv \
  --output spark_etl/output \
  --limit 50000
```
