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
        "pre": np.random.randint(15, size=num_rows, dtype=np.uint32),
        "succ": np.random.randint(15, size=num_rows, dtype=np.uint32),
        "duration": np.random.randint(10000, size=num_rows, dtype=np.uint32),
        "flag": np.random.binomial(2, 0.2, num_rows),
    }
)

df = df.with_columns([
    col("flag").cast(pl.Utf8).cast(pl.Categorical),
])

df.write_parquet("random_int.parquet")

df_cat = df.with_columns([
    col("pre").cast(pl.Utf8).cast(pl.Categorical),
    col("succ").cast(pl.Utf8).cast(pl.Categorical),

])

df_cat.write_parquet("random_cat.parquet")

with Timer(text=f"groupby from in memory int\t{{milliseconds:.0f}}"):
    aggregated = (
        df
        .filter(col("flag") == lit("1"))
        .groupby(["pre", "succ"]).agg([
            col("duration").mean(),
            col("duration").median().alias("MedianDuration"),
            pl.count().alias("Count")
        ])
    )


with Timer(text=f"groupby from in memory cat\t{{milliseconds:.0f}}"):
    aggregated = (
        df_cat
        .filter(col("flag") == lit("1"))
        .groupby(["pre", "succ"]).agg([
            col("duration").mean(),
            col("duration").median().alias("MedianDuration"),
            pl.count().alias("Count")
        ])
    )


for f in ["random_int.parquet", "random_cat.parquet"]:

    df2 = pl.scan_parquet(f)

    with Timer(text=f"groupby {f}\t{{milliseconds:.0f}}"):
        aggregated = (
            df2
            .filter(col("flag") == lit("1"))
            .groupby(["pre", "succ"]).agg([
                col("duration").mean(),
                col("duration").median().alias("MedianDuration"),
                pl.count().alias("Count")
            ])
        ).collect()