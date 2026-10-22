# 163: joining three tables
builds on: [097 junction tables, the table in the middle](./097-junction-tables.md), [156 inner join traced by hand](./156-inner-join-traced-by-hand.md), [157 ON, how a join decides which rows match](./157-on-how-a-join-decides-which-rows-match.md), [158 table aliases, short nicknames for tables](./158-table-aliases-short-nicknames-for-tables.md), [159 left join, keep every row from the left table](./159-left-join-keep-every-row-from-the-left-table.md)
section: combining tables with joins, part 9, ~2 min read

order 101 has two rows in order_items, product_id 1 and 5. which products is that? the product names live in a third table.

joining three tables is two joins in a row. the first join makes a table of paired rows, and the second join treats that result as its [left table](./159-left-join-keep-every-row-from-the-left-table.md) (the one written before JOIN) and pairs it with the third. the shop (the imaginary gujarati snack store these notes run on) has order_items, the [junction table](./097-junction-tables.md) (one row per order and product pair), and products, which holds the names. with [aliases](./158-table-aliases-short-nicknames-for-tables.md), for orders 101 and 106:

```sql
SELECT o.order_id, o.status, p.name, oi.quantity FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id WHERE o.order_id IN (101, 106) ORDER BY o.order_id, p.name
```

```result
order_id | status | name | quantity
101 | delivered | dhokla | 2
101 | delivered | masala chai | 2
106 | pending | khandvi | 2
```

first row: order 101 pairs with its order_items row (101, 1, 2), so the pair now carries product_id 1. that pair then meets the products row with product_id 1, dhokla (a steamed savory cake). i expected a special three way match, and its two ordinary [inner joins](./156-inner-join-traced-by-hand.md) (keep only matching pairs), one after the other.

what bit me is that each [ON](./157-on-how-a-join-decides-which-rows-match.md) (the match test) can only name tables already joined, plus the one it joins. swap the last two joins and keep the old ON lines:

```sql
-- fails on purpose
SELECT o.order_id, p.name FROM orders o JOIN products p ON oi.product_id = p.product_id JOIN order_items oi ON o.order_id = oi.order_id
```

DuckDB, the database these notes run in, says "oi" was not found, since it isnt joined yet at that ON. fix the ONs for the new order and the inner join rows come out the same.

run the chain on all 7 orders and you get 13 rows, one per row of order_items, 6 more than orders has. the next one is about why.

---
prev: [162 right and full outer joins](./162-right-and-full-outer-joins.md) | next: not written yet
