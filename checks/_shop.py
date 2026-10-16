"""Shared helper for checks: a fresh DuckDB loaded with data/shop.sql."""
import os
import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def shop():
    con = duckdb.connect(":memory:")
    with open(os.path.join(ROOT, "data", "shop.sql"), encoding="utf-8") as f:
        con.execute(f.read())
    return con
