"""Row-level transforms shared by the Spark job and unit tests.

These are the same steps a Databricks notebook would apply with PySpark:
drop empty reviews, map polarity to a label, and add simple text metrics.
"""

from __future__ import annotations

import re

POLARITY_TO_SENTIMENT = {1: "negative", 2: "positive"}
_WHITESPACE = re.compile(r"\s+")


def clean_text(value: str | None) -> str:
    if value is None:
        return ""
    text = str(value).replace("\\n", " ").strip()
    return _WHITESPACE.sub(" ", text)


def sentiment_from_polarity(polarity: int | None) -> str | None:
    if polarity is None:
        return None
    try:
        return POLARITY_TO_SENTIMENT.get(int(polarity))
    except (TypeError, ValueError):
        return None


def is_usable_review(title: str, text: str, sentiment: str | None) -> bool:
    return bool(sentiment) and bool(text) and len(text) >= 8
