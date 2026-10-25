# 204: arrays and UNNEST, lists inside a cell
builds on: [071 exploding lists into many rows](./071-exploding-lists-into-many-rows.md), [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md), [175 subquery in FROM](./175-subquery-in-from.md)
section: bigger queries, part 31, ~2 min read

how many shop products are tagged savory, when every product keeps all its tags in one cell?

an array is a list of values stored in one cell, which DuckDB writes in square brackets. Postgres (a database) calls it an array, DuckDB calls the variable length kind a list. UNNEST is [exploding](./071-exploding-lists-into-many-rows.md) (one row per list item) done inside a query. the shop, the imaginary gujarati snack store these notes run on, has a new product_tags table. here is a slice, then the same rows unnested:

| product_id | tags |
|---|---|
| 1 (dhokla, a steamed savory cake) | [steamed, savory] |
| 4 (kaju katli, a cashew sweet) | [sweet, festive] |
| 5 (masala chai) | [] |

```sql
SELECT product_id, UNNEST(tags) AS tag FROM product_tags WHERE product_id IN (1, 4, 5) ORDER BY product_id, tag
```

```result
product_id | tag
1 | savory
1 | steamed
4 | festive
4 | sweet
```

WHERE ... IN keeps only those 3 products and ORDER BY sorts the rows. each tag got its own row and product_id got copied onto both, same as 071 copying the order fields. masala chai is gone. i assumed an empty list would leave one row with a missing tag, but DuckDB says an empty list unnests to zero rows, the same hole 071 found in the python loop.

now the tags are plain rows, so the old tools work. a [subquery in FROM](./175-subquery-in-from.md) (an inner SELECT read like a table) feeds a [GROUP BY](./143-group-by-one-group-per-value.md) (one bucket per value):

```sql
SELECT tag, count(*) AS products FROM (SELECT UNNEST(tags) AS tag FROM product_tags) GROUP BY tag ORDER BY products DESC, tag
```

```result
tag | products
savory | 3
fried | 2
sweet | 2
festive | 1
rolled | 1
steamed | 1
```

savory is 3. the counts add up to 10 tags, but only 5 of the shops 6 products show up behind them, since chai has none. so a tag count can never tell you which products are untagged, you need the original table for that.

Postgres has the same unnest function on its arrays, so this habit carries over.

---
prev: [203 recursive CTEs, following a chain of rows](./203-recursive-ctes-following-a-chain-of-rows.md) | next: [205 querying JSON inside a column](./205-querying-json-inside-a-column.md)
