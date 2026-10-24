# 194: removing duplicates with ROW_NUMBER
builds on: [121 DISTINCT, removing duplicate rows](./121-distinct-removing-duplicate-rows.md), [175 subquery in FROM](./175-subquery-in-from.md), [186 PARTITION BY, a separate window per group](./186-partition-by-a-separate-window-per-group.md), [187 ROW_NUMBER, numbering rows in order](./187-row-number-numbering-rows-in-order.md), [193 top N per group](./193-top-n-per-group.md)
section: bigger queries, part 21, ~2 min read

Asha (customer 1) is in my feed twice with two different cities, so which one is true? DISTINCT cant tell me, and thats the whole problem.

deduplicating means keeping one row per thing when the data holds several. the shop, the imaginary snack store these notes run on, got a raw feed of city updates, a table i added called city_feed (all 5 rows):

```sql
SELECT customer_id, city, changed_at FROM city_feed
```

```result
customer_id | city | changed_at
1 | Jersey City | 2026-04-10 09:00:00
2 | Edison | 2026-04-10 09:05:00
1 | Hoboken | 2026-04-12 18:30:00
4 | Hoboken | 2026-04-11 07:45:00
2 | Edison | 2026-04-10 09:05:00
```

[DISTINCT](./121-distinct-removing-duplicate-rows.md) (keeps one copy of identical rows) only removes Bhavins (customer 2) exact copy, so Asha still has 2 rows. her rows differ, so DISTINCT sees two different rows. the fix is [top N per group](./193-top-n-per-group.md) with N = 1: number each customers rows newest first with [ROW_NUMBER](./187-row-number-numbering-rows-in-order.md) per [PARTITION BY](./186-partition-by-a-separate-window-per-group.md) customer (a separate count per customer), then keep number 1 in a [subquery in FROM](./175-subquery-in-from.md):

```sql
SELECT customer_id, city, changed_at FROM (SELECT customer_id, city, changed_at, row_number() OVER (PARTITION BY customer_id ORDER BY changed_at DESC) AS rn FROM city_feed) AS t WHERE rn = 1 ORDER BY customer_id
```

```result
customer_id | city | changed_at
1 | Hoboken | 2026-04-12 18:30:00
2 | Edison | 2026-04-10 09:05:00
4 | Hoboken | 2026-04-11 07:45:00
```

3 customers, 3 rows. Ashas newest row won, so she lives in Hoboken now. the ORDER BY inside OVER is where you decide which copy survives, and i hadnt thought of it as a choice before.

Bhavins two rows are identical, so either one can be number 1 and you cant tell which was kept. if two different rows tie on the sort, add a second sort column or the winner isnt promised.

### check yourself

1. a teammate runs SELECT DISTINCT customer_id, city, changed_at on city_feed. how many rows come back, and does Asha appear once?
<details><summary>answer</summary>

4 rows, and Asha still appears twice. only Bhavins exact copy collapses. the tempting answer is 3, from thinking DISTINCT means one row per customer, but it compares whole rows.

</details>

2. change the filter to rn > 1 on the same query. predict the rows.
```sql
SELECT customer_id, city FROM (SELECT customer_id, city, row_number() OVER (PARTITION BY customer_id ORDER BY changed_at DESC) AS rn FROM city_feed) AS t WHERE rn > 1 ORDER BY customer_id
```
<details><summary>answer</summary>

```result
customer_id | city
1 | Jersey City
2 | Edison
```
these are the rows the dedup threw away: Ashas old city and Bhavins copy. the tempting answer is 1 row, from forgetting Bhavins copy counts as extra.

</details>

---
prev: [193 top N per group](./193-top-n-per-group.md) | next: [195 gaps and islands, date minus row number](./195-gaps-and-islands-date-minus-row-number.md)
