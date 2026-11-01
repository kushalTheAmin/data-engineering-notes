# 294: selectivity, when an index doesnt help
builds on: [293 what indexes cost, slower writes and more disk](./293-what-indexes-cost-slower-writes-and-more-disk.md), [286 index, a sorted shortcut to rows](./286-index-a-sorted-shortcut-to-rows.md), [285 full table scan, reading every page](./285-full-table-scan-reading-every-page.md), [284 how Postgres keeps a table on disk, rows packed into pages](./284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md)
section: inside a database server, part 11, ~2 min read

i put an index on status and Postgres used it for cancelled orders but skipped it for delivered ones, same column, same index. [293](./293-what-indexes-cost-slower-writes-and-more-disk.md) said an index costs disk and slower writes, so what if it never gets used?

selectivity is the share of a tables rows that a condition keeps. a condition that keeps few rows is selective, and thats the kind an [index](./286-index-a-sorted-shortcut-to-rows.md) (a sorted list of values and row addresses) actually helps.

the shop, the imaginary gujarati snack store these notes run on, here as 100000 made up orders in Postgres 16, a database server, with an index on status. this copy is 736 [pages](./284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md), 8192 byte chunks of rows. 100 orders are cancelled, the rest delivered. pages touched counts every page visit in the Buffers line of EXPLAIN, from [285](./285-full-table-scan-reading-every-page.md):

| query | rows kept | plan | pages touched |
|---|---|---|---|
| `status = 'cancelled'` | 100 (0.1%) | Index Scan | 102 |
| `status = 'delivered'` | 99900 (99.9%) | Seq Scan | 736 |
| delivered, Seq Scan switched off | 99900 (99.9%) | Index Scan | 823 |

102 is 2 index pages plus 100 table pages, one trip per cancelled order, and those 100 sat on 100 different pages. for delivered, Postgres chose Seq Scan (read every page in order), and when i switched Seq Scan off with a setting it used the index and touched 823 page visits, more than the scan, since it hopped through the index and the table instead of reading straight through. so the scan really was cheaper.

the same idea on the 7 real orders:

```python
statuses = ["delivered", "delivered", "delivered", "cancelled", "delivered", "pending", "delivered"]
for value in sorted(set(statuses)):
    kept = statuses.count(value)
    print(f"{value}: {kept} of {len(statuses)}, {round(100 * kept / len(statuses))}%")
```

```output
cancelled: 1 of 7, 14%
delivered: 5 of 7, 71%
pending: 1 of 7, 14%
```

i assumed a column was either worth indexing or not, but the same index wins for cancelled and loses for delivered. selectivity belongs to the value you ask for.

### check yourself

1. a teammate indexes an is_active column where 99.8% of 100000 rows are true. `WHERE is_active = true` ignores the index and they file a bug. whats going on, and which query on that column could use it?

<details><summary>answer</summary>

no bug. true keeps about 99800 rows, so scanning is cheaper, same as delivered above. `WHERE is_active = false` keeps about 200 rows and can use the index. the tempting answer is a stale or broken index, but the plan depends on the value asked for, not the column.

</details>

2. the 7 real orders have the status mix below. a second table of 100000 orders in that same mix has pending keeping about 14% of rows, scattered through the table. do you expect it to touch about 14% of its 725 pages?

```sql
SELECT status, count(*) AS orders FROM orders GROUP BY status ORDER BY status;
```

<details><summary>answer</summary>

```result
status | orders
cancelled | 1
delivered | 5
pending | 1
```

no. on Postgres 16 the 14286 pending rows were spread over nearly every page, so Postgres chose a bitmap scan (list the pages first, then read them) and it touched 739 pages (14 index, 725 table), more than the whole table has. a share of rows is not a share of pages. the tempting answer is about 104 pages.

</details>

---
prev: [293 what indexes cost, slower writes and more disk](./293-what-indexes-cost-slower-writes-and-more-disk.md) | next: [295 functions on a column, why the index gets skipped](./295-functions-on-a-column-why-the-index-gets-skipped.md)
