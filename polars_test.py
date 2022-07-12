#!/usr/bin/env python3.10

import polars as pl
from polars import col, lit
from codetiming import Timer

pl.version()
import numpy as np

np.random.seed(12)
num_rows = 33000000

df = pl.DataFrame(
    {
        "pre": np.random.randint(15, size=num_rows, dtype=np.uint8),
        "succ": np.random.randint(15, size=num_rows, dtype=np.uint8),
        "duration": np.random.randint(10000, size=num_rows, dtype=np.uint16),
        "flag": np.random.binomial(2, 0.2, num_rows),
    }
)

df = df.with_columns([
    # col("pre").cast(pl.Utf8).cast(pl.Categorical),
    # col("succ").cast(pl.Utf8).cast(pl.Categorical),
    col("flag").cast(pl.Utf8).cast(pl.Categorical),
    col("flag").cast(pl.Utf8).cast(pl.Categorical).alias("flag2"),
])

df.write_parquet("random.parquet")

df2 = pl.scan_parquet("random.parquet")

with Timer("groupby"):
    aggregated = (
        df2
        .filter(col("flag") == lit("1"))
        .groupby(["pre", "succ"]).agg([
            col("duration").mean(),
            col("duration").median().alias("MedianDuration"),
            pl.count().alias("Count")
        ])
    ).collect()