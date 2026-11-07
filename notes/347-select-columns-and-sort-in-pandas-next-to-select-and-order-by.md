# 347: select columns and sort in pandas, next to SELECT and ORDER BY
builds on: [346 filter rows in pandas, next to WHERE](./346-filter-rows-in-pandas-next-to-where.md), [345 a dataframe, a table in memory](./345-a-dataframe-a-table-in-memory.md), [104 SELECT and FROM, picking columns](./104-select-and-from-picking-columns.md), [117 ORDER BY, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md), [118 no ORDER BY, no promised order](./118-no-order-by-no-promised-order.md)
section: python for data work, part 23, ~2 min read

i typed df["status"] and got one thing, then df[["status"]] and got something that prints differently. whats the second pair of brackets for?

in pandas, a python package for data analysis, picking columns is [SELECT](./104-select-and-from-picking-columns.md) (keep only the columns you name) written as a list of names inside the brackets. sorting is [ORDER BY](./117-order-by-sorting-by-one-or-more-columns.md) (put the rows in order) written as sort_values. here is the same 4 order slice of the shop, the imaginary gujarati snack store these notes run on, as the [dataframe](./345-a-dataframe-a-table-in-memory.md) (a table held in memory) from [346](./346-filter-rows-in-pandas-next-to-where.md):

```python
import pandas as pd

df = pd.DataFrame([
    {"order_id": 101, "customer_id": 1, "status": "delivered"},
    {"order_id": 104, "customer_id": 3, "status": "cancelled"},
    {"order_id": 106, "customer_id": 1, "status": "pending"},
    {"order_id": 107, "customer_id": 2, "status": "delivered"},
])
print(type(df["status"]).__name__, type(df[["status"]]).__name__)
print(df[["order_id", "status"]])
out = df.sort_values(["customer_id", "order_id"], ascending=[True, False])
print(out)
print(list(df["order_id"]))
```

```output
Series DataFrame
   order_id     status
0       101  delivered
1       104  cancelled
2       106    pending
3       107  delivered
   order_id  customer_id     status
2       106            1    pending
0       101            1  delivered
3       107            2  delivered
1       104            3  cancelled
[101, 104, 106, 107]
```

one name gives a Series, pandas word for a single column on its own. a list of names, so two pairs of brackets, gives a dataframe with just those columns. i assumed the extra brackets were style, but they decide whether you get a column or a table.

ascending=[True, False] means customer_id smallest first, order_id biggest first, the 2 column tie rule from [117](./117-order-by-sorting-by-one-or-more-columns.md). customer 1 has two orders, so order_id breaks the tie, 106 before 101.

the labels, the numbers down the left, travel with their rows: 2, 0, 3, 1. and df still prints 101, 104, 106, 107, you got a new dataframe back.

a table in SQL (the language for asking databases questions) has [no promised order](./118-no-order-by-no-promised-order.md) unless you ask. a dataframe always has one, so sort_values really moves rows.

---
prev: [346 filter rows in pandas, next to WHERE](./346-filter-rows-in-pandas-next-to-where.md) | next: not written yet
