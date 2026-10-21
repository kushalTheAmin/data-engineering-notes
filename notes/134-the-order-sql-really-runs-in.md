# 134: the order SQL really runs in
builds on: [104 SELECT and FROM, picking columns](./104-select-and-from-picking-columns.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [117 ORDER BY, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md), [120 LIMIT and OFFSET, paging through rows](./120-limit-and-offset-paging-through-rows.md), [122 computed columns and AS](./122-computed-columns-and-as.md)
section: asking questions with SQL, part 34, ~2 min read

why can ORDER BY use a name you made with AS, when Postgres refuses the same name in WHERE? i assumed SQL runs top to bottom as you write it, so SELECT goes first.

it doesnt. a query runs its clauses in a fixed logical order, FROM, WHERE, SELECT, ORDER BY, LIMIT, whatever order you type them in (the database may shuffle the real steps, the answer stays the same). here is a query on the products of the shop, the imaginary gujarati snack store these notes run on, (dhokla and khandvi are steamed and rolled chickpea snacks, fafda a crunchy one), and what is left after each clause:

| step | clause | rows left | what is there |
|---|---|---|---|
| 1 | FROM products | 6 | all six products |
| 2 | WHERE category = 'snack' | 3 | dhokla, khandvi, fafda |
| 3 | SELECT name, price - 1 AS sale_price | 3 | sale_price exists now: 5.00, 6.50, 3.50 |
| 4 | ORDER BY sale_price | 3 | fafda, dhokla, khandvi |
| 5 | LIMIT 2 | 2 | fafda, dhokla |

```sql
SELECT name, price - 1 AS sale_price FROM products WHERE category = 'snack' ORDER BY sale_price LIMIT 2
```

```result
name | sale_price
fafda | 3.50
dhokla | 5.00
```

[FROM](./104-select-and-from-picking-columns.md) names the table, [WHERE](./106-where-keeping-only-the-rows-that-match.md) drops rows, [SELECT](./104-select-and-from-picking-columns.md) picks and builds columns, [ORDER BY](./117-order-by-sorting-by-one-or-more-columns.md) sorts, [LIMIT](./120-limit-and-offset-paging-through-rows.md) cuts. at step 2 sale_price doesnt exist yet, which is why the docs of Postgres, a server database, say an [AS name](./122-computed-columns-and-as.md) works in ORDER BY but not in WHERE (there you write the expression out again). DuckDB is friendlier, as 122 said, so dont count on it elsewhere.

i expected SELECT to be first, and its third. LIMIT being last matters too: cutting 2 rows before sorting would sort whatever 2 survived, not the cheapest 2.

### check yourself

1. a teammate says LIMIT 2 grabs the 2 newest orders first, and WHERE then filters those. so they expect this to return 1 row. how many rows come back, and which?

```sql
SELECT order_id FROM orders WHERE status = 'delivered' ORDER BY ordered_at DESC LIMIT 2
```
<details><summary>answer</summary>

```result
order_id
107
105
```

2 rows. WHERE drops 106 (pending) and 104 (cancelled) first, then ORDER BY sorts, then LIMIT cuts. their order would keep 107 and 106, then lose 106, leaving 1 row.

</details>

2. which product comes back, and why not masala chai, the cheapest?

```sql
SELECT name, 0 - price AS price FROM products ORDER BY price LIMIT 1
```
<details><summary>answer</summary>

```result
name | price
kaju katli | -12.00
```

SELECT runs before ORDER BY, so the sort sees the new price column, the negative one, and -12.00 is the smallest. the tempting answer is masala chai, from sorting the real prices. the Postgres docs pick the new name here too.

</details>

---
prev: [133 casts that fail, and TRY_CAST](./133-casts-that-fail-and-try-cast.md) | next: [135 one language, many dialects](./135-one-language-many-dialects.md)
