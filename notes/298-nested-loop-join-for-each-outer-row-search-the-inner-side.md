# 298: nested loop join, for each outer row search the inner side
builds on: [297 statistics, how the planner guesses row counts](./297-statistics-how-the-planner-guesses-row-counts.md), [296 the query planner, picking the cheapest plan](./296-the-query-planner-picking-the-cheapest-plan.md), [285 full table scan, reading every page](./285-full-table-scan-reading-every-page.md), [272 a loop inside a loop, the steps are one list times the other](./272-a-loop-inside-a-loop-the-steps-are-one-list-times-the-other.md), [156 inner join traced by hand](./156-inner-join-traced-by-hand.md)
section: inside a database server, part 15, ~2 min read

you join order 500 to its customer and Postgres runs the loop inside a loop from [272](./272-a-loop-inside-a-loop-the-steps-are-one-list-times-the-other.md). drop the WHERE, the row filter, and it runs something else. why would the same join change?

a nested loop join is that loop inside a loop, run by Postgres, the database server these notes use, to pair rows of two tables ([156](./156-inner-join-traced-by-hand.md)). each row of the outer side, read once, gets a search of the inner side, the other table, for its matches.

the shop, the imaginary gujarati snack store these notes run on, as 100000 made up orders and 5 customers. the plan, the steps the [planner](./296-the-query-planner-picking-the-cheapest-plan.md) picked, as the EXPLAIN command prints it:

```text
-- Postgres 16
EXPLAIN SELECT o.order_id, c.name
FROM orders100k o JOIN customers c ON c.customer_id = o.customer_id
WHERE o.order_id = 500;

 Nested Loop  (cost=0.29..9.42 rows=1 ...)
   Join Filter: (c.customer_id = o.customer_id)
   ->  Index Scan using orders100k_pkey on orders100k o     <- outer: 1 row
         Index Cond: (order_id = 500)
   ->  Seq Scan on customers c                              <- inner: 5 rows
```

the first child is the outer side, one order found by its [index](./286-index-a-sorted-shortcut-to-rows.md) (a sorted list of values and row addresses). the second is the inner side, a [Seq Scan](./285-full-table-scan-reading-every-page.md) (read every page) of 5 customers, once per outer row. 1 times 5 is 5 looks, finding Asha.

EXPLAIN shows only the winner, so i switched other methods off to see losers, like a hash join (builds a lookup table of the inner side). cost is a made up number for comparing plans ([296](./296-the-query-planner-picking-the-cheapest-plan.md)):

| orders on the outer side | nested loop cost | hash join cost | planner picks |
|---|---|---|---|
| 1 (order 500) | 9.42 | 9.43 | nested loop |
| 100000 (no WHERE) | 3940.88 | 2126.11 | hash join |

i assumed a nested loop was the naive join Postgres only fell back on, but with one outer row it won, by 0.01 on this data.

how many outer rows to expect is one of the guesses from [297](./297-statistics-how-the-planner-guesses-row-counts.md). if it expects 1 and 20000 arrive, the inner side runs 20000 times.

### check yourself

1. a plain loop has the 7 real shop orders on the outside, customers inside. how many inner looks, and what comes back?

```sql
SELECT o.order_id, c.name FROM orders o JOIN customers c ON c.customer_id = o.customer_id WHERE o.status = 'cancelled'
```

<details><summary>answer</summary>

```result
order_id | name
104 | Chirag
```

5 looks, 1 outer row times 5 customers. the WHERE runs before the loop, so only one order goes round. the tempting answer is 35, from all 7 orders times 5 customers like in 156.

</details>

2. the planner expected 1 outer order, but 20000 made up orders arrive (a real planner would then switch methods). against the 5 customers, how many inner looks instead of 5?

<details><summary>answer</summary>

100000, 20000 times 5. the tempting answer is 20000, from counting outer rows and forgetting each one searches the whole inner side.

</details>

---
prev: [297 statistics, how the planner guesses row counts](./297-statistics-how-the-planner-guesses-row-counts.md) | next: not written yet
