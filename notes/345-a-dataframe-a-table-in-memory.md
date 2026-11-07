# 345: a dataframe, a table in memory
builds on: [344 practice, dedupe and count orders in plain python](./344-practice-dedupe-and-count-orders-in-plain-python.md), [340 reading a csv in python, row by row](./340-reading-a-csv-in-python-row-by-row.md), [327 packages and pip, installing code other people wrote](./327-packages-and-pip-installing-code-other-people-wrote.md), [080 every column holds one type](./080-every-column-holds-one-type.md), [036 memory vs disk](./036-memory-vs-disk.md), [286 index, a sorted shortcut to rows](./286-index-a-sorted-shortcut-to-rows.md)
section: python for data work, part 21, ~2 min read

every count in 344 was a loop over a list of dictionaries. what if the list already knew it was a table?

a dataframe is a table held in [memory](./036-memory-vs-disk.md), the computers working space: rows, named columns, and one type per column. it comes from pandas, a [package](./327-packages-and-pip-installing-code-other-people-wrote.md) (code other people wrote and shared) you get with pip install pandas (pip is the installer).

here is a slice of 4 orders from the shop, the imaginary gujarati snack store these notes run on, as the same list of row dictionaries [344](./344-practice-dedupe-and-count-orders-in-plain-python.md) looped over:

```python
import pandas as pd

rows = [
    {"order_id": 101, "customer_id": 1, "status": "delivered"},
    {"order_id": 104, "customer_id": 3, "status": "cancelled"},
    {"order_id": 106, "customer_id": 1, "status": "pending"},
    {"order_id": 107, "customer_id": 2, "status": "delivered"},
]
df = pd.DataFrame(rows)
print(df)
print(df.shape)
print(df["order_id"].sum())
```

```output
   order_id  customer_id     status
0       101            1  delivered
1       104            3  cancelled
2       106            1    pending
3       107            2  delivered
(4, 3)
418
```

pd is a nickname for pandas. each dictionary became a row and the dictionary keys became the column names. shape is rows by columns.

the 0 to 3 down the left is pandas labelling the rows, and it calls that the index. dont confuse it with a [database index](./286-index-a-sorted-shortcut-to-rows.md), a sorted shortcut a database keeps for finding rows fast.

what got me is the last line. i expected adding up a column to need a loop like in 344, but df["order_id"] hands back the whole column as one object that sums itself. it came out as whole numbers because pandas gives each column [one type](./080-every-column-holds-one-type.md),.

the catch is the same one [340](./340-reading-a-csv-in-python-row-by-row.md) hit with list(reader), which loads every csv row into a list: all of it sits in memory at once. a 50 gigabyte file will not fit in a dataframe on a laptop.

---
prev: [344 practice, dedupe and count orders in plain python](./344-practice-dedupe-and-count-orders-in-plain-python.md) | next: [346 filter rows in pandas, next to WHERE](./346-filter-rows-in-pandas-next-to-where.md)
