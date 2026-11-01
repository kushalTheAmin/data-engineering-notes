# 295: functions on a column, why the index gets skipped
builds on: [294 selectivity, when an index doesnt help](./294-selectivity-when-an-index-doesnt-help.md), [286 index, a sorted shortcut to rows](./286-index-a-sorted-shortcut-to-rows.md), [285 full table scan, reading every page](./285-full-table-scan-reading-every-page.md), [273 binary search, finding one item in sorted data by halving](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md), [132 CAST, changing a values type](./132-cast-changing-a-values-type.md)
section: inside a database server, part 12, ~2 min read

i had an index on ordered_at, filtered on the date of it, and Postgres still read every page. 144 of 100000 rows is very selective, so selectivity ([294](./294-selectivity-when-an-index-doesnt-help.md), how few rows a condition keeps) cant be it.

an [index](./286-index-a-sorted-shortcut-to-rows.md) (a sorted list of values and row addresses) is sorted by the column as stored. wrap the column in a function in the WHERE and Postgres cant [halve](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md) that list, so it falls back to a [full scan](./285-full-table-scan-reading-every-page.md), called Seq Scan in a plan.

the shop, the imaginary gujarati snack store these notes run on, as 100000 made up orders in Postgres 16, one every 10 minutes, 144 on 1 June 2025. this copy is 736 pages (8192 byte chunks of rows), indexed on ordered_at. pages touched is page visits. [CAST](./132-cast-changing-a-values-type.md) (turns a value into another type) counts as a function:

| WHERE | plan | rows kept | pages touched |
|---|---|---|---|
| `CAST(ordered_at AS DATE) = '2025-06-01'` | Seq Scan | 144 | 736 |
| `ordered_at >= '2025-06-01' AND ordered_at < '2025-06-02'` | Index Scan, uses the index | 144 | 4 |

same rows, 736 pages against 4. on the 7 real orders:

```sql
SELECT order_id FROM orders WHERE ordered_at >= TIMESTAMP '2026-04-01' AND ordered_at < TIMESTAMP '2026-04-02' ORDER BY order_id;
```

```result
order_id
101
102
```

a date never goes backwards as the timestamp grows, but Postgres 16 doesnt reason about what a function does to order. it only knows the list is sorted by the bare column, the column alone. so you keep it bare and move the work elsewhere. the other fix is an index on the expression itself, which the Postgres docs say costs extra on every insert and some updates. [source](https://www.postgresql.org/docs/16/indexes-expressional.html)

i assumed the index cared which column i filtered on, but it cares whether the column is left alone. lower(email) = '...' is the classic one, fixed by that expression index.

### check yourself

1. a teammate says WHERE order_id + 1 = 108 is fast because order_id has an index. on the 100000 order table the same shape scanned 736 pages. what does the 7 order version return, and how do you fix it?

```sql
SELECT order_id FROM orders WHERE order_id + 1 = 108;
```

<details><summary>answer</summary>

```result
order_id
107
```

write WHERE order_id = 107. with the column bare, Postgres 16 touched 3 pages, all index. the tempting answer is that the index covers the column so any filter on it works, but the index is sorted by order_id, not by order_id + 1.

</details>

2. customers are stored as Asha, Bhavin and so on, with an index on name. `WHERE lower(name) = 'asha'` ignores it on a big table. give two fixes and when you would pick each.

<details><summary>answer</summary>

```sql
SELECT customer_id FROM customers WHERE lower(name) = 'asha';
```

```result
customer_id
1
```

compare the bare column, `WHERE name = 'Asha'`, when you know the exact stored case. or build an index on lower(name), which keeps the query as written but costs work on every insert. adding a second plain index on name is the tempting answer and changes nothing.

</details>

---
prev: [294 selectivity, when an index doesnt help](./294-selectivity-when-an-index-doesnt-help.md) | next: not written yet
