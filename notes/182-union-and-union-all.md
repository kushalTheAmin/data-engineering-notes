# 182: UNION and UNION ALL
builds on: [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [175 subquery in FROM](./175-subquery-in-from.md), [181 views, a saved query with a name](./181-views-a-saved-query-with-a-name.md)
section: bigger queries, part 9, ~2 min read

the shop has 7 orders. i split them into delivered and not delivered, stack the customer ids of both groups, and ask for rows. do you get 7, or 4?

UNION stacks the rows of one query under the rows of another. UNION ALL does the same, and plain UNION then throws away repeated rows. the shop, the imaginary gujarati snack store these notes run on, has 5 delivered orders and 2 that are not, each [WHERE](./106-where-keeping-only-the-rows-that-match.md) (keeps rows passing a test) picking one group:

```sql
SELECT customer_id FROM orders WHERE status = 'delivered' UNION ALL SELECT customer_id FROM orders WHERE status <> 'delivered' ORDER BY customer_id
```

```result
customer_id
1
1
1
2
2
3
4
```

```sql
SELECT customer_id FROM orders WHERE status = 'delivered' UNION SELECT customer_id FROM orders WHERE status <> 'delivered' ORDER BY customer_id
```

```result
customer_id
1
2
3
4
```

in python, UNION ALL is `a + b` and UNION is `sorted(set(a + b))`. i figured stacking two lists couldnt lose rows, but plain UNION quietly drops repeats, and Asha has three real orders that collapse into one row.

two rules. both queries need the same number of columns, and columns line up by position, not by name. the result takes its names from the first query.

so default to UNION ALL. Postgres (a server database) docs say it is usually significantly quicker, since nothing has to be compared. this is how teams glue monthly tables or logs into one.

### check yourself

1. predict n. snacks are dhokla, khandvi, fafda. products under 6 are jalebi, masala chai, fafda. dhokla costs exactly 6.00.
```sql
SELECT count(*) AS n FROM (SELECT name FROM products WHERE category = 'snack' UNION SELECT name FROM products WHERE price < 6)
```
<details><summary>answer</summary>

```result
n
5
```
fafda is in both lists, so UNION keeps it once: 3 + 3 minus 1. the tempting answer is 6, from adding the two lists.

</details>

2. no error here, but is it what you wanted? predict the rows.
```sql
SELECT name, city FROM customers WHERE customer_id = 1 UNION ALL SELECT city, name FROM customers WHERE customer_id = 1
```
<details><summary>answer</summary>

```result
name | city
Asha | Jersey City
Jersey City | Asha
```
columns match by position and both are text, so the second row puts a city under name. the tempting answer is that the database matches names and fixes it.

</details>

---
prev: [181 views, a saved query with a name](./181-views-a-saved-query-with-a-name.md) | next: not written yet
