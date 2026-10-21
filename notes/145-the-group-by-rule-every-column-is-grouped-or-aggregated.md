# 145: the GROUP BY rule, every column is grouped or aggregated
builds on: [137 aggregate functions, many rows in, one value out](./137-aggregate-functions-many-rows-in-one-value-out.md), [142 MIN and MAX, the smallest and biggest value](./142-min-and-max-the-smallest-and-biggest-value.md), [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md), [144 grouping by more than one column](./144-grouping-by-more-than-one-column.md)
section: summarizing data, part 9, ~2 min read

i asked for each customers order count and also their status, and the database refused. which status was it supposed to show for Asha?

the rule: once you [GROUP BY](./143-group-by-one-group-per-value.md) (one row per different value), every column in SELECT must be grouped or inside an [aggregate](./137-aggregate-functions-many-rows-in-one-value-out.md) (many rows in, one value out). each group becomes exactly one row, so each column needs exactly one value per group.

```sql
-- fails on purpose
SELECT customer_id, status, count(*) AS n FROM orders GROUP BY customer_id
```

here is the group of Asha, customer 1 of the shop, the imaginary gujarati snack store these notes run on, as the dictionary of lists from 143:

```python
orders = [(1, "delivered"), (2, "delivered"), (1, "delivered"), (3, "cancelled"),
          (4, "delivered"), (1, "pending"), (2, "delivered")]
groups = {}
for customer_id, status in orders:
    groups.setdefault(customer_id, []).append(status)
print(groups[1])
```

```output
['delivered', 'delivered', 'pending']
```

three statuses, one cell to put them in. there is no right pick, so DuckDB, the database these notes run queries in, errors instead of guessing. i assumed it would quietly take the first one, like groups[1][0].

to fix it, ask for something that has one answer per group, like [max](./142-min-and-max-the-smallest-and-biggest-value.md) of the order time:

```sql
SELECT customer_id, count(*) AS n, max(ordered_at) AS latest FROM orders GROUP BY customer_id ORDER BY customer_id
```

```result
customer_id | n | latest
1 | 3 | 2026-04-08 10:00:00
2 | 2 | 2026-04-09 13:45:00
3 | 1 | 2026-04-04 08:30:00
4 | 1 | 2026-04-06 19:10:00
```

or add status to the GROUP BY, which is [144](./144-grouping-by-more-than-one-column.md) again.

so what: MySQL has a mode, ONLY_FULL_GROUP_BY, that is on by default. switch it off and the server picks any value from each group, and its docs call that nondeterministic (it can differ run to run).

### check yourself

1. does this run, or error? and if it runs, how many rows?
```sql
SELECT customer_id, count(*) AS n FROM orders GROUP BY customer_id, status ORDER BY customer_id, status
```
<details><summary>answer</summary>

```result
customer_id | n
1 | 2
1 | 1
2 | 2
3 | 1
4 | 1
```
it runs, 5 rows. the rule only covers what SELECT shows, and a grouped column can stay hidden. Asha appears twice because she has two groups. the tempting answer is an error, from reading it as the failing query above.

</details>

2. you want the cheapest product per category. the query below errored on name, so you add name to the GROUP BY. how many rows come back?
```sql
SELECT category, name, min(price) AS lowest FROM products GROUP BY category, name ORDER BY category, name
```
<details><summary>answer</summary>

```result
category | name | lowest
drink | masala chai | 3.00
snack | dhokla | 6.00
snack | fafda | 4.50
snack | khandvi | 7.50
sweet | jalebi | 5.00
sweet | kaju katli | 12.00
```
6 rows, not 3. every name is different, so every group holds one product and min has nothing to compare. the tempting answer is 3, from assuming the fix kept the category groups.

</details>

---
prev: [144 grouping by more than one column](./144-grouping-by-more-than-one-column.md) | next: not written yet
