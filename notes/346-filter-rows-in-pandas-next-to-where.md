# 346: filter rows in pandas, next to WHERE
builds on: [345 a dataframe, a table in memory](./345-a-dataframe-a-table-in-memory.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [108 AND and OR, combining two tests](./108-and-or-combining-two-tests.md), [023 true and false, the boolean](./023-true-and-false-the-boolean.md)
section: python for data work, part 22, ~2 min read

i filtered 4 orders down to the delivered ones and the row labels came back as 0 and 3. where did 1 and 2 go, and why didnt it renumber?

filtering in pandas is [WHERE](./106-where-keeping-only-the-rows-that-match.md) (keep only rows whose condition is true) written as df[df["status"] == "delivered"]. the inner part compares every row at once and gives a mask, a column of True and False, one per row. the outer brackets keep the True rows. here is the same 4 order slice of the shop, the imaginary gujarati snack store, as the [dataframe](./345-a-dataframe-a-table-in-memory.md) in 345 (a table held in memory by pandas, a python package for data analysis):

| label | order_id | customer_id | status | mask |
|---|---|---|---|---|
| 0 | 101 | 1 | delivered | True |
| 1 | 104 | 3 | cancelled | False |
| 2 | 106 | 1 | pending | False |
| 3 | 107 | 2 | delivered | True |

```python
import pandas as pd

df = pd.DataFrame([
    {"order_id": 101, "customer_id": 1, "status": "delivered"},
    {"order_id": 104, "customer_id": 3, "status": "cancelled"},
    {"order_id": 106, "customer_id": 1, "status": "pending"},
    {"order_id": 107, "customer_id": 2, "status": "delivered"},
])
print(df[df["status"] == "delivered"])
print(df[(df["status"] == "delivered") & (df["customer_id"] == 1)])
print(len(df))
```

```output
   order_id  customer_id     status
0       101            1  delivered
3       107            2  delivered
   order_id  customer_id     status
0       101            1  delivered
4
```

the labels 0 and 3 are the pandas index from 345, and a row keeps its label when it survives a filter. the original df is untouched, still 4 rows, you just got a new dataframe back.

for [AND](./108-and-or-combining-two-tests.md) you write & and for OR you write |, with each test in its own parentheses. the pandas docs say why: python does the & before the ==, so without parentheses it reads the test wrong.

i kept reading pythons plain and as the same thing as AND. but and wants one [True or False](./023-true-and-false-the-boolean.md), and a mask holds four, so pandas raises a ValueError instead of guessing.

next you pick columns and sort, the SELECT and ORDER BY half.

---
prev: [345 a dataframe, a table in memory](./345-a-dataframe-a-table-in-memory.md) | next: not written yet
