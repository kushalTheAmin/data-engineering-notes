# 348: groupby in pandas, next to GROUP BY
builds on: [347 select columns and sort in pandas, next to SELECT and ORDER BY](./347-select-columns-and-sort-in-pandas-next-to-select-and-order-by.md), [345 a dataframe, a table in memory](./345-a-dataframe-a-table-in-memory.md), [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md), [137 aggregate functions, many rows in, one value out](./137-aggregate-functions-many-rows-in-one-value-out.md), [031 null, a marker for a missing value](./031-null.md), [118 no ORDER BY, no promised order](./118-no-order-by-no-promised-order.md)
section: python for data work, part 24, ~2 min read

i grouped 4 orders by customer and printed the result, and customer_id had stopped being a column. it was down the left, where the row labels go (pandas calls them the [index](./345-a-dataframe-a-table-in-memory.md)).

groupby in pandas, a python package for data analysis, is [GROUP BY](./143-group-by-one-group-per-value.md) (one group per different value) written as df.groupby("customer_id"), followed by the [aggregate](./137-aggregate-functions-many-rows-in-one-value-out.md) (many rows in, one value out) you want per group. here is the 4 order slice of the shop, the imaginary gujarati snack store these notes run on, as the [dataframe](./345-a-dataframe-a-table-in-memory.md) (a table held in memory) from [347](./347-select-columns-and-sort-in-pandas-next-to-select-and-order-by.md), now with an items column, the total quantity across the order:

```python
import pandas as pd

df = pd.DataFrame([
    {"order_id": 101, "customer_id": 1, "status": "delivered", "items": 4},
    {"order_id": 104, "customer_id": 3, "status": "cancelled", "items": 3},
    {"order_id": 106, "customer_id": 1, "status": "pending", "items": 2},
    {"order_id": 107, "customer_id": 2, "status": "delivered", "items": 2},
])
print(df.groupby("customer_id")["items"].agg(["count", "sum"]))
print(df.groupby("customer_id", as_index=False)["items"].sum())
```

```output
             count  sum
customer_id            
1                2    6
2                1    2
3                1    3
   customer_id  items
0            1      6
1            2      2
2            3      3
```

customer 1 has orders 101 and 106, so count is 2 and sum is 4 plus 2, 6. the group values became the row labels, and as_index=False puts them back as a normal column. pandas also sorts the groups by key, where SQL (the language for asking databases questions) has [no promised order](./118-no-order-by-no-promised-order.md).

now the part that surprised me. Esha has no city, a [null](./031-null.md) (a missing value), and 143 showed GROUP BY giving her own group. pandas drops her by default, because her group key (the value you group by) is missing, no error:

```python
import pandas as pd

cust = pd.DataFrame([
    {"name": "Asha", "city": "Jersey City"}, {"name": "Bhavin", "city": "Edison"},
    {"name": "Chirag", "city": "Jersey City"}, {"name": "Disha", "city": "Hoboken"},
    {"name": "Esha", "city": None},
])
print(cust.groupby("city")["name"].count().sum())
print(cust.groupby("city", dropna=False)["name"].count().sum())
```

```output
4
5
```

dropna=False keeps the missing group. a report built on the default says 4 customers when you have 5.

### check yourself

1. same 4 order slice, now grouped by status. predict what this prints.
```python
import pandas as pd

df = pd.DataFrame([
    {"order_id": 101, "customer_id": 1, "status": "delivered", "items": 4},
    {"order_id": 104, "customer_id": 3, "status": "cancelled", "items": 3},
    {"order_id": 106, "customer_id": 1, "status": "pending", "items": 2},
    {"order_id": 107, "customer_id": 2, "status": "delivered", "items": 2},
])
print(df.groupby("status")["items"].sum().to_dict())
```
<details><summary>answer</summary>

```output
{'cancelled': 3, 'delivered': 6, 'pending': 2}
```
groups come out sorted by key, so cancelled leads even though delivered appears first in df. delivered is 4 plus 2, orders 101 and 107. the tempting answer lists delivered first, from assuming order of appearance.

</details>

2. 5 orders have ratings: 101 got 5, 102 got 4, 103 got none (missing), 105 got 3, 107 got none. with stars holding those values, what does this print?
```python
import pandas as pd

r = pd.DataFrame({"order_id": [101, 102, 103, 105, 107], "stars": [5, 4, None, 3, None]})
g = r.groupby("stars")["order_id"].count()
print(len(g), g.sum())
```
<details><summary>answer</summary>

```output
3 3
```
the 2 unrated orders have a missing key, so they get dropped: 3 groups and 3 counted orders. the tempting answer is 4 and 5, from expecting a group for the missing stars like SQL gives.

</details>

---
prev: [347 select columns and sort in pandas, next to SELECT and ORDER BY](./347-select-columns-and-sort-in-pandas-next-to-select-and-order-by.md) | next: not written yet
