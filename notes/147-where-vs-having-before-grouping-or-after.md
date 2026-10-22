# 147: WHERE vs HAVING, before grouping or after
builds on: [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [134 the order SQL really runs in](./134-the-order-sql-really-runs-in.md), [137 aggregate functions, many rows in, one value out](./137-aggregate-functions-many-rows-in-one-value-out.md), [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md), [146 HAVING, filtering whole groups](./146-having-filtering-whole-groups.md)
section: summarizing data, part 11, ~2 min read

after [146](./146-having-filtering-whole-groups.md) my first instinct for "customers with at least 2 orders" was WHERE count(*) >= 2 (count(*) is how many rows). the database errored, so why does HAVING take the exact same test?

timing. [WHERE](./106-where-keeping-only-the-rows-that-match.md) (keeps rows that match) runs on single rows, before [GROUP BY](./143-group-by-one-group-per-value.md) (one row per different value) builds any group, so no count exists yet. [HAVING](./146-having-filtering-whole-groups.md) (filters groups) runs after, when the counts are there.

```sql
-- fails on purpose
SELECT customer_id, count(*) AS n FROM orders WHERE count(*) >= 2 GROUP BY customer_id
```

in practice you use both. here are the orders of the shop, the imaginary gujarati snack store these notes run on, asking for customers with at least 2 delivered orders, and what is left after each step:

| step | what is left |
| --- | --- |
| FROM orders | 7 rows |
| WHERE status = 'delivered' | 5 rows, order ids 101, 102, 103, 105, 107 |
| GROUP BY customer_id | 3 groups, sizes 2, 2 and 1 for customers 1, 2 and 4 (customer 3 has none left) |
| HAVING count(*) >= 2 | 2 groups, customers 1 and 2 |

```sql
SELECT customer_id, count(*) AS n FROM orders WHERE status = 'delivered' GROUP BY customer_id HAVING count(*) >= 2 ORDER BY customer_id
```

```result
customer_id | n
1 | 2
2 | 2
```

i assumed the two filters were interchangeable, but they change what gets counted. the WHERE ran first, so Asha, customer 1, had her pending order thrown out before counting, and her n is 2. in [146](./146-having-filtering-whole-groups.md) it was 3. customer 3 isnt a group with 0, they have no group at all, since their only order was cancelled.

so the rule: a test on one rows own column goes in WHERE, a test on an aggregate (like count or max) goes in HAVING. a test on a grouped column would run in either, but the docs of Postgres, a server database, say WHERE is more efficient there, because rows that fail it never get grouped. the full order with both clauses comes in a later note.

### check yourself

1. a teammate wants delivered orders only, and writes the test in HAVING. does this run?
```sql
-- fails on purpose
SELECT customer_id FROM orders GROUP BY customer_id HAVING status = 'delivered'
```
<details><summary>answer</summary>

in DuckDB it errors (some databases accept it, but then status is an arbitrary pick). after grouping, each group becomes one row, but a group can hold several statuses (Asha has delivered and pending), and status is neither grouped nor inside an aggregate, so one cell cant hold them, the rule from [145](./145-the-group-by-rule-every-column-is-grouped-or-aggregated.md). the test belongs in WHERE. the tempting answer is that it works and returns the delivered customers.

</details>

2. how many rows come back?
```sql
SELECT customer_id, count(*) AS n FROM orders WHERE status = 'delivered' GROUP BY customer_id HAVING count(*) >= 3
```
<details><summary>answer</summary>

```result
customer_id | n
```
0 rows. Asha has 3 orders in total, but WHERE removes her pending one first, so her group has 2 and fails the test. the tempting answer is 1 row, customer 1, from counting all their orders.

</details>

---
prev: [146 HAVING, filtering whole groups](./146-having-filtering-whole-groups.md) | next: not written yet
