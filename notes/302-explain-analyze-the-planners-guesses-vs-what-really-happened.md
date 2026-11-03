# 302: EXPLAIN ANALYZE, the planners guesses vs what really happened
builds on: [301 reading EXPLAIN, the plan as a tree](./301-reading-explain-the-plan-as-a-tree.md), [299 hash join, build a hash table then look up each row](./299-hash-join-build-a-hash-table-then-look-up-each-row.md), [297 statistics, how the planner guesses row counts](./297-statistics-how-the-planner-guesses-row-counts.md), [228 commit and rollback, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md), [285 full table scan, reading every page](./285-full-table-scan-reading-every-page.md)
section: inside a database server, part 19, ~2 min read

Postgres, the database server these notes use, plans a query before running it and guesses how many rows each step handles. the plan in [301](./301-reading-explain-the-plan-as-a-tree.md) guessed 97 cancelled orders, and i just believed it. how do you check a guess like that without counting by hand?

EXPLAIN ANALYZE is the [EXPLAIN](./285-full-table-scan-reading-every-page.md) command (it prints how Postgres runs a query) with one change: Postgres actually runs the query, then prints what really happened next to each guess ([docs](https://www.postgresql.org/docs/16/using-explain.html)).

the shop, the imaginary gujarati snack store these notes run on, as 100000 made up orders in Postgres 16, same cancelled-orders-per-customer query as 301. a fresh [ANALYZE](./297-statistics-how-the-planner-guesses-row-counts.md) (the command that re-samples a table, a different thing from the option here) sampled differently, so the guess is 90 this time. the second pair on each line is the new part:

```text
-- Postgres 16
EXPLAIN ANALYZE SELECT c.name, count(*) ... (same query as 301)

 HashAggregate  (cost=118.76..118.81 rows=5 ...) (actual time=0.622..0.625 rows=1 ...)   <- guessed 5, got 1
   ->  Hash Join  (cost=1.41..118.31 rows=90 ...) (actual time=0.051..0.600 rows=100 ...) <- guessed 90, got 100
         ->  Index Scan using orders100k_status_idx on orders100k o
                    (cost=0.29..116.76 rows=90 ...) (actual time=0.019..0.549 rows=100 ...) <- guessed 90, got 100
         ->  Hash  (cost=1.05..1.05 rows=5 ...) (actual time=0.017..0.017 rows=5 ...)    <- guessed 5, got 5
               ->  Seq Scan on customers c
                    (cost=0.00..1.05 rows=5 ...) (actual time=0.004..0.005 rows=5 ...)  <- guessed 5, got 5
 Execution Time: 0.709 ms
```

actual time is real milliseconds, start..total, and like cost a parent includes its children. cost is a made up score, so the two arent comparable. the docs say to look first at whether the guessed rows= is close to the actual rows=. the 90 against 100 is a near miss. the root missed more: 5 against 1, because all 100 cancelled orders in my made up table are Ashas.

i figured EXPLAIN ANALYZE was EXPLAIN with a stopwatch added. it isnt. it runs the query, so an UPDATE or DELETE inside it really changes your data. to look safely, wrap it in BEGIN ... ROLLBACK ([228](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md)), which throws the changes away.

### check yourself

1. on the 7 real shop orders you run EXPLAIN ANALYZE on an UPDATE, outside any BEGIN, just to read the plan, then count. how many orders are cancelled?

```sql
EXPLAIN ANALYZE UPDATE orders SET status = 'cancelled' WHERE customer_id = 1;
SELECT count(*) AS cancelled FROM orders WHERE status = 'cancelled'
```

<details><summary>answer</summary>

```result
cancelled
4
```

4, Chirags order 104 plus Ashas three. ANALYZE executes the statement. the tempting answer is 1, from thinking EXPLAIN only prints.

</details>

2. a teammate says a plan is fine because its cost is low. one scan line reads rows=2 and actual rows=2000. what do you suspect, and what do you try first?

<details><summary>answer</summary>

often stale [statistics](./297-statistics-how-the-planner-guesses-row-counts.md) (the saved summary guesses come from), or lumpy data. the plan was built for 2 rows, so the plan may suit 2 rows and not 2000. try ANALYZE on the table, then compare again. the tempting answer is to trust the low cost, but cost is only as good as the row guess under it.

</details>

---
prev: [301 reading EXPLAIN, the plan as a tree](./301-reading-explain-the-plan-as-a-tree.md) | next: [303 the buffer pool, keeping hot pages in memory](./303-the-buffer-pool-keeping-hot-pages-in-memory.md)
