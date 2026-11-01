# 296: the query planner, picking the cheapest plan
builds on: [295 functions on a column, why the index gets skipped](./295-functions-on-a-column-why-the-index-gets-skipped.md), [294 selectivity, when an index doesnt help](./294-selectivity-when-an-index-doesnt-help.md), [286 index, a sorted shortcut to rows](./286-index-a-sorted-shortcut-to-rows.md), [285 full table scan, reading every page](./285-full-table-scan-reading-every-page.md), [284 how Postgres keeps a table on disk, rows packed into pages](./284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md)
section: inside a database server, part 13, ~2 min read

in [294](./294-selectivity-when-an-index-doesnt-help.md) the same index on status (a sorted list of values and row addresses) got used for cancelled orders and skipped for delivered ones. nobody told Postgres which, so who decided?

the query planner is the part of Postgres, the database server these notes use, that, before running anything, lists the ways to run your query, puts a cost on each, and picks the cheapest. the winner is the plan, which the [EXPLAIN](./285-full-table-scan-reading-every-page.md) command prints.

cost is a made up number, not milliseconds, only good for comparing plans. the shop, the imaginary gujarati snack store these notes run on, as 100000 made up orders in Postgres 16: 736 [pages](./284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md), an [index](./286-index-a-sorted-shortcut-to-rows.md) on status, same as 294. EXPLAIN prints only the winner, so i got each loser by switching the other plans off with settings:

| table, condition | Seq Scan cost | Index Scan cost | planner picks |
|---|---|---|---|
| 100000 orders, cancelled | 1986.00 | 14.36 | Index Scan |
| 100000 orders, delivered | 1986.00 | 2849.71 | Seq Scan |
| the 7 real orders, cancelled | 1.09 | 8.15 | Seq Scan |

a [Seq Scan](./285-full-table-scan-reading-every-page.md) (read every page) costs 1986 for both, 736 pages plus a small charge per row, since it reads everything either way. the index route is what swings: 14.36 when 137 rows are expected, 2849.71 when 99863 are. thats a guess, 100 are really cancelled, and how it guesses is a later note.

i assumed Postgres followed a rule like use the index if there is one, but it prices both every time. look at the last row, even the one cancelled order skips the index, since 7 rows are one page and reading it beats going through the index first.

so the same query can change plan as the table grows.

### check yourself

1. the 7 real orders have an index on status. you run this, expecting the index because 1 row of 7 is selective. what comes back, and does the planner use the index?

```sql
SELECT order_id FROM orders WHERE status = 'cancelled';
```

<details><summary>answer</summary>

```result
order_id
104
```

no, Postgres 16 chose a Seq Scan, cost 1.09 against 8.15 for the index. the table is one page, so reading it all is cheaper than index then table. the tempting answer is that few rows kept means the index wins, but that only pays once pages are many.

</details>

2. on the 100000 orders a teammate switches Seq Scan off for the delivered query to force the index. what changes in the rows that come back, and in the cost? the 7 order version of the rows:

```sql
SELECT order_id FROM orders WHERE status = 'delivered' ORDER BY order_id;
```

<details><summary>answer</summary>

```result
order_id
101
102
103
105
107
```

the rows never change, only how they are found. the cost goes from 1986.00 to 2849.71, so the forced plan is the more expensive one by the planners own numbers. the tempting answer is different rows coming back, but a setting only makes a plan look worse or better, it never filters a row.

</details>

---
prev: [295 functions on a column, why the index gets skipped](./295-functions-on-a-column-why-the-index-gets-skipped.md) | next: not written yet
