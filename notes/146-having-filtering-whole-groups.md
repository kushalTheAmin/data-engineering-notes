# 146: HAVING, filtering whole groups
builds on: [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [137 aggregate functions, many rows in, one value out](./137-aggregate-functions-many-rows-in-one-value-out.md), [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md), [145 the GROUP BY rule, every column is grouped or aggregated](./145-the-group-by-rule-every-column-is-grouped-or-aggregated.md)
section: summarizing data, part 10, ~2 min read

after [145](./145-the-group-by-rule-every-column-is-grouped-or-aggregated.md) each group is a row, so a new question shows up: how do you keep only some of those rows, like the customers who ordered at least twice?

HAVING is a filter that runs on the groups after [GROUP BY](./143-group-by-one-group-per-value.md) (one row per different value) has built them. you write a test on an [aggregate](./137-aggregate-functions-many-rows-in-one-value-out.md) (many rows in, one value out) and groups where it isnt true are dropped. here are the 7 orders of the shop, the imaginary gujarati snack store these notes run on, counted per customer (count(*) is the number of rows in a group):

```sql
SELECT customer_id, count(*) AS n FROM orders GROUP BY customer_id HAVING count(*) >= 2 ORDER BY customer_id
```

```result
customer_id | n
1 | 3
2 | 2
```

customers 3 and 4 had one order each, so their groups are gone. in python it is one more loop:

```python
counts = {1: 3, 2: 2, 3: 1, 4: 1}
kept = {c: n for c, n in counts.items() if n >= 2}
print(kept)
```

```output
{1: 3, 2: 2}
```

i kept reading HAVING as a fussy second WHERE, but a [WHERE](./106-where-keeping-only-the-rows-that-match.md) (keeps rows that match) looks at single rows, and a single row has no count yet, so the count can only be tested after the groups exist.

one thing i didnt expect: the aggregate in HAVING doesnt have to be one you SELECT. HAVING max(ordered_at) > TIMESTAMP '2026-04-05 00:00:00' keeps customers 1, 2 and 4 and shows only the count. the orders behind it, a slice, customer then time: 1 on april 8, 2 on april 9, 3 on april 4, 4 on april 6.

so what: "customers with 2 or more orders", "products sold in at least 10 orders", duplicate hunting with HAVING count(*) > 1, since any id that shows up twice has a count above 1.

### check yourself

1. how many rows come back, and does it error?
```sql
SELECT customer_id, count(*) AS n FROM orders GROUP BY customer_id HAVING count(*) > 5
```
<details><summary>answer</summary>

```result
customer_id | n
```
it runs and returns 0 rows. the biggest group has 3 orders, so every group fails the test, and filtering everything out is not an error. the tempting answer is an error, from thinking an empty answer means something broke.

</details>

2. same idea, a later cutoff. predict the rows, then count them.
```sql
SELECT customer_id FROM orders GROUP BY customer_id HAVING max(ordered_at) > TIMESTAMP '2026-04-08 12:00:00' ORDER BY customer_id
```
<details><summary>answer</summary>

```result
customer_id
2
```
1 row. customer 1 also ordered on april 8, but at 10:00, which is before the cutoff, so their newest order fails. only customer 2, on april 9, passes. the tempting answer is 2 rows, from reading the cutoff as just the day april 8.

</details>

---
prev: [145 the GROUP BY rule, every column is grouped or aggregated](./145-the-group-by-rule-every-column-is-grouped-or-aggregated.md) | next: not written yet
