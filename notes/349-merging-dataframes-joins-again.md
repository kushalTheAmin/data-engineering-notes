# 349: merging dataframes, joins again
builds on: [348 groupby in pandas, next to GROUP BY](./348-groupby-in-pandas-next-to-group-by.md), [345 a dataframe, a table in memory](./345-a-dataframe-a-table-in-memory.md), [156 inner join traced by hand](./156-inner-join-traced-by-hand.md), [159 left join, keep every row from the left table](./159-left-join-keep-every-row-from-the-left-table.md), [164 fan out, when a join multiplies rows](./164-fan-out-when-a-join-multiplies-rows.md), [031 null, a marker for a missing value](./031-null.md), [019 floating point, digits plus where the point sits](./019-floating-point.md), [332 merge conflicts, when git cant combine two edits](./332-merge-conflicts-when-git-cant-combine-two-edits.md)
section: python for data work, part 25, ~2 min read

i merged 5 customers with their orders and Esha was gone, no error, no warning. then i fixed it, and did you know the order ids turn into decimals?

merge is how pandas (a python package for data analysis) does a join: `cust.merge(orders, on="customer_id")` matches rows where that column is equal (not a [git merge](./332-merge-conflicts-when-git-cant-combine-two-edits.md), this is a join). the default is an [inner join](./156-inner-join-traced-by-hand.md) (keeps only pairs that match), and `how="left"` is a [left join](./159-left-join-keep-every-row-from-the-left-table.md) (keeps every row of the first table). here are the shop customers, the imaginary gujarati snack store these notes run on, and its 7 orders, as [dataframes](./345-a-dataframe-a-table-in-memory.md) (tables held in memory):

```python
import pandas as pd

cust = pd.DataFrame([
    {"customer_id": 1, "name": "Asha"}, {"customer_id": 2, "name": "Bhavin"},
    {"customer_id": 3, "name": "Chirag"}, {"customer_id": 4, "name": "Disha"},
    {"customer_id": 5, "name": "Esha"},
])
orders = pd.DataFrame([
    {"order_id": 101, "customer_id": 1}, {"order_id": 102, "customer_id": 2},
    {"order_id": 103, "customer_id": 1}, {"order_id": 104, "customer_id": 3},
    {"order_id": 105, "customer_id": 4}, {"order_id": 106, "customer_id": 1},
    {"order_id": 107, "customer_id": 2},
])
inner = cust.merge(orders, on="customer_id")
left = cust.merge(orders, on="customer_id", how="left")
print(len(inner), len(left))
print(left.tail(3))
print(inner["order_id"].dtype, left["order_id"].dtype)
```

```output
7 8
   customer_id    name  order_id
5            3  Chirag     104.0
6            4   Disha     105.0
7            5    Esha       NaN
int64 float64
```

the left merge has 8 rows, the same 8 as 159, and Eshas order_id is NaN, not a number, a float pandas uses in a number column where SQL (the language for asking databases questions) has [NULL](./031-null.md), a missing value. i expected the ids to stay whole numbers, but NaN is a float (a number with a decimal point, [019](./019-floating-point.md)), so one missing value (here only the left merge has an unmatched row, the inner one stayed int64) turned the whole column into 104.0, 105.0. int64 is whole numbers, float64 has decimals.

a merge [fans out](./164-fan-out-when-a-join-multiplies-rows.md) (copies a row per match) just like a join, Asha got 3 rows. compare len before and after every merge. it is how a report quietly counts 13 orders when there are 7, after merging in the items.

### check yourself

1. orders 104, 105 and 106 as a dataframe, and the items of just 104 and 105 (104 has 1 item row, 105 has 3). predict the printed line.
```python
import pandas as pd

orders = pd.DataFrame([{"order_id": 104}, {"order_id": 105}, {"order_id": 106}])
items = pd.DataFrame([
    {"order_id": 104, "product_id": 1, "quantity": 3},
    {"order_id": 105, "product_id": 4, "quantity": 2},
    {"order_id": 105, "product_id": 3, "quantity": 2},
    {"order_id": 105, "product_id": 5, "quantity": 1},
])
a = orders.merge(items, on="order_id")
b = orders.merge(items, on="order_id", how="left")
print(len(a), len(b), b["quantity"].tolist())
```
<details><summary>answer</summary>

```output
4 5 [3.0, 2.0, 2.0, 1.0, nan]
```
order 105 fans out to 3 rows, so the inner merge has 1 + 3 = 4. the left merge adds 106 with nothing, 5 rows, and its quantity becomes NaN, which turns the others into floats. the tempting answer for the first number is 3, one row per order.

</details>

2. same 7 orders and 5 customers as above, but the other way round: `orders.merge(cust, on="customer_id", how="left")`. how many rows, and is order_id still int64?
<details><summary>answer</summary>

7 rows, and int64. every order has a customer, so nothing is missing, and Esha is not kept because she is on the right. the tempting answer is 8 rows with floats, from thinking how="left" always adds Esha. it only keeps every row of the table you call merge on.

</details>

---
prev: [348 groupby in pandas, next to GROUP BY](./348-groupby-in-pandas-next-to-group-by.md) | next: [350 connecting python to a database, a result you read once](./350-connecting-python-to-a-database-a-result-you-read-once.md)
