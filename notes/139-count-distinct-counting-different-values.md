# 139: COUNT DISTINCT, counting different values
builds on: [031 null, a marker for a missing value](./031-null.md), [121 DISTINCT, removing duplicate rows](./121-distinct-removing-duplicate-rows.md), [137 aggregate functions, many rows in, one value out](./137-aggregate-functions-many-rows-in-one-value-out.md), [138 COUNT star vs COUNT of a column](./138-count-star-vs-count-of-a-column.md)
section: summarizing data, part 3, ~2 min read

the shop has 7 orders, so does that mean 7 customers? the people who ordered are fewer, and count(*) from [138](./138-count-star-vs-count-of-a-column.md) can only give you rows.

count(DISTINCT column) counts how many different values show up, not how many rows. it is the [DISTINCT](./121-distinct-removing-duplicate-rows.md) idea (keep one copy of each) inside an [aggregate function](./137-aggregate-functions-many-rows-in-one-value-out.md) (many rows in, one value out). in python it is a loop with a seen list, count a value only the first time:

```python
customer_ids = [1, 2, 1, 3, 4, 1, 2]
seen = []
for c in customer_ids:
    if c not in seen:
        seen.append(c)
print(len(customer_ids), len(seen))
```

```output
7 4
```

those 7 ids are the customer_id column of orders, from the shop, the imaginary gujarati snack store these notes run on. same thing in SQL:

```sql
SELECT count(*) AS orders, count(DISTINCT customer_id) AS customers FROM orders
```

```result
orders | customers
7 | 4
```

7 orders, 4 people. Asha ordered 3 times and Bhavin twice, so they got counted once each.

now the part that surprised me. customers has a city column, and Esha has none, so that cell is [null](./031-null.md) (a missing value):

```sql
SELECT count(*) AS rows_in, count(city) AS with_city, count(DISTINCT city) AS cities FROM customers
```

```result
rows_in | with_city | cities
5 | 4 | 3
```

4 cities filled in, but Jersey City appears twice, so 3 different ones. i assumed the null would count as its own value, since DISTINCT in 121 collapses nulls into one kept row. count(DISTINCT) skips it, just like count(column) did.

so what: this is how you ask "how many customers" or "how many products sold" and not "how many rows". the docs of Postgres, a server database, say it directly, count(distinct f1) yields the number of distinct non-null values of f1.

---
prev: [138 COUNT star vs COUNT of a column](./138-count-star-vs-count-of-a-column.md) | next: not written yet
