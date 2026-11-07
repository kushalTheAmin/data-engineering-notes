# checks for notes/346-filter-rows-in-pandas-next-to-where.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
import pandas as pd
con = shop()
got = con.execute("SELECT order_id, customer_id, status FROM orders WHERE order_id IN (101,104,106,107) ORDER BY order_id").fetchall()
assert got == [(101, 1, "delivered"), (104, 3, "cancelled"), (106, 1, "pending"), (107, 2, "delivered")]  # the table rows are real shop rows
df = pd.DataFrame([dict(zip(("order_id", "customer_id", "status"), r)) for r in got])
mask = df["status"] == "delivered"
assert list(mask) == [True, False, False, True]  # the mask column
done = df[mask]
assert list(done.index) == [0, 3] and list(done["order_id"]) == [101, 107]  # labels survive the filter
both = df[(df["status"] == "delivered") & (df["customer_id"] == 1)]
assert list(both.index) == [0] and list(both["order_id"]) == [101]
assert len(df) == 4  # original untouched
try:
    df[df["status"] == "delivered" and df["customer_id"] == 1]
    raise SystemExit("and should have raised")
except ValueError:
    pass
# without parentheses & binds tighter than ==, so the test is read wrong (fails here)
try:
    df[df["status"] == "delivered" & df["customer_id"] == 1]
    raise SystemExit("no parentheses should have failed")
except Exception:
    pass
# source: https://pandas.pydata.org/docs/user_guide/indexing.html
# opened this run: boolean indexing uses | for or, & for and, ~ for not, and these must be grouped with parentheses because python would evaluate df['A'] > 2 & df['B'] < 3 as df['A'] > (2 & df['B']) < 3
# audit: python does & before ==, so a == 1 & b == 2 groups 1 & b first
import ast
_e = ast.parse("a == 1 & b == 2", mode="eval").body
assert isinstance(_e.comparators[0], ast.BinOp) and isinstance(_e.comparators[0].op, ast.BitAnd)
