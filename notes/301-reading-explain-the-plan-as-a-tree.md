# 301: reading EXPLAIN, the plan as a tree
builds on: [300 merge join, walk two sorted lists side by side](./300-merge-join-walk-two-sorted-lists-side-by-side.md), [299 hash join, build a hash table then look up each row](./299-hash-join-build-a-hash-table-then-look-up-each-row.md), [298 nested loop join, for each outer row search the inner side](./298-nested-loop-join-for-each-outer-row-search-the-inner-side.md), [297 statistics, how the planner guesses row counts](./297-statistics-how-the-planner-guesses-row-counts.md), [296 the query planner, picking the cheapest plan](./296-the-query-planner-picking-the-cheapest-plan.md), [280 trees, data that branches](./280-trees-data-that-branches.md)
section: inside a database server, part 18, ~2 min read

below, the top line of a plan costs 136.31 and the Index Scan under it costs 134.20. so is the top line the expensive step? [296](./296-the-query-planner-picking-the-cheapest-plan.md) said EXPLAIN prints the plan, the steps Postgres picked.

a plan is a [tree](./280-trees-data-that-branches.md) (boxes linked parent to children), and each step line is one [node](./280-trees-data-that-branches.md). indentation says whose child it is ([docs](https://www.postgresql.org/docs/16/using-explain.html)). rows travel up, from the leaves (nodes with no children, which read tables) to the root (the top line), and the root hands you the answer.

the shop, the imaginary gujarati snack store these notes run on, as 100000 made up orders in Postgres 16. cancelled orders per customer (with pending orders too, so costs differ from 296):

```text
-- Postgres 16
EXPLAIN SELECT c.name, count(*)
FROM orders100k o JOIN customers c ON c.customer_id = o.customer_id
WHERE o.status = 'cancelled' GROUP BY c.name;

 HashAggregate  (cost=136.26..136.31 rows=5 ...)        <- root: groups, hands you the answer
   ->  Hash Join  (cost=1.41..135.78 rows=97 ...)       <- pairs rows from its 2 children
         ->  Index Scan using orders100k_status_idx on orders100k o
                    (cost=0.29..134.20 rows=97 ...)     <- leaf: the cancelled orders
         ->  Hash  (cost=1.05..1.05 rows=5 ...)         <- loads customers into a hash table
               ->  Seq Scan on customers c
                    (cost=0.00..1.05 rows=5 ...)       <- leaf: reads all 5 customers
```

i trimmed the detail lines. the Hash Join probes with the order scan and builds the Hash, as in [299](./299-hash-join-build-a-hash-table-then-look-up-each-row.md). strictly the root asks its child for rows, which asks its child, so the asking goes down while the rows come back up.

the cost is the made up score from 296, the second number of each pair is the total, and a parent includes its children: 134.20 sits inside 135.78 inside 136.31. so the root is usually biggest. the root itself adds only 0.53, so the top line isnt the expensive step. rows= is the guess from [297](./297-statistics-how-the-planner-guesses-row-counts.md), 97 against 100 really cancelled.

i read it like a script, first line first, but the deepest lines feed the ones above. the next one runs the plan for real, to put the guesses next to the truth.

### check yourself

1. run the same query on the 7 real shop orders, where only order 104, Chirags, is cancelled. say the plan has the same shape, so the Seq Scan leaf on customers hands up 5 rows. what does the root hand back?

```sql
SELECT c.name, count(*) AS orders FROM orders o JOIN customers c ON c.customer_id = o.customer_id WHERE o.status = 'cancelled' GROUP BY c.name
```

<details><summary>answer</summary>

```result
name | orders
Chirag | 1
```

one row. rows shrink on the way up: the 5 customers meet 1 cancelled order in the join, and the root groups that. the tempting answer is 5, from reading the bottom line as what the plan returns.

</details>

2. a teammate pastes a plan whose root says cost=0.00..4000.00 and its only child says cost=0.00..3990.00. they call the root the slow step because it has the biggest number. what do you tell them?

<details><summary>answer</summary>

a parent cost includes its children, so the root is usually the biggest. the root adds about 10 (4000 minus 3990), the child holds the other 3990. the tempting answer is to agree, since a bigger number looks like more work, but the number is a running total up the tree.

</details>

---
prev: [300 merge join, walk two sorted lists side by side](./300-merge-join-walk-two-sorted-lists-side-by-side.md) | next: not written yet
