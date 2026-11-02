# 297: statistics, how the planner guesses row counts
builds on: [296 the query planner, picking the cheapest plan](./296-the-query-planner-picking-the-cheapest-plan.md), [294 selectivity, when an index doesnt help](./294-selectivity-when-an-index-doesnt-help.md)
section: inside a database server, part 14, ~2 min read

in [296](./296-the-query-planner-picking-the-cheapest-plan.md) the query planner, the part of Postgres that picks how to run a query, expected 137 cancelled orders, a status an order can have, when 100 were real. it never counted them first, so where did a number like that come from?

statistics are a small summary Postgres, a database server, keeps about each column. the ANALYZE command fills them in by reading a random sample of rows on a big table, not all. for a column it saves the most common values and the share of rows each one has, the [selectivity](./294-selectivity-when-an-index-doesnt-help.md) (share of rows a condition keeps).

the shop, the imaginary gujarati snack store these notes run on, as 100000 made up orders, 100 of them cancelled. the second line of output is the saved shares, 99.9% delivered and about 0.08% cancelled:

```text
-- Postgres 16
ANALYZE orders100k;
SELECT most_common_vals, most_common_freqs FROM pg_stats
WHERE tablename = 'orders100k' AND attname = 'status';

 most_common_vals      | most_common_freqs
 {delivered,cancelled} | {0.9992333,0.00076666666}
```

for a saved value the guess is that share times the table size. that first run sampled 30000 rows and 23 were cancelled (23 / 30000 is the 0.00076666); i then ran it five times in all, each on a fresh sample:

```python
for hits in [23, 32, 21, 30, 33]:
    share = hits / 30000
    print(f"{hits} of 30000 -> {share:.7f} -> expects {round(share * 100000)} rows")
```

```output
23 of 30000 -> 0.0007667 -> expects 77 rows
32 of 30000 -> 0.0010667 -> expects 107 rows
21 of 30000 -> 0.0007000 -> expects 70 rows
30 of 30000 -> 0.0010000 -> expects 100 rows
33 of 30000 -> 0.0011000 -> expects 110 rows
```

the real answer is 100 every time. i assumed the planner counted the table before choosing, but it only multiplies a share it saved earlier, and the share comes from a sample. the docs say autovacuum, the background cleaner, reruns ANALYZE once a table has changed enough, so if you see an odd plan after loading lots of new rows, suspect stale guesses.

next up is what the planner does with these guesses.

---
prev: [296 the query planner, picking the cheapest plan](./296-the-query-planner-picking-the-cheapest-plan.md) | next: not written yet
