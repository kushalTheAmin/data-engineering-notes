# 188: RANK vs DENSE_RANK, what ties do
builds on: [117 ORDER BY, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md), [175 subquery in FROM](./175-subquery-in-from.md), [184 window functions, a total next to every row](./184-window-functions-a-total-next-to-every-row.md), [185 OVER, the window a function looks through](./185-over-the-window-a-function-looks-through.md), [187 ROW_NUMBER, numbering rows in order](./187-row-number-numbering-rows-in-order.md)
section: bigger queries, part 15, ~2 min read

two rows tie for first. is the next row second or third?

RANK() and DENSE_RANK() are [window functions](./184-window-functions-a-total-next-to-every-row.md) (calculations that keep every row) that number rows like [ROW_NUMBER](./187-row-number-numbering-rows-in-order.md) (counts 1, 2, 3 in the OVER order), except tied rows get the same number. they only disagree about what comes after the tie. the shop, the imaginary snack store these notes run on, has order_items, one row per product on an order. a slice, orders 102 and 105, biggest quantity first:

```sql
SELECT order_id, product_id, quantity, rank() OVER (ORDER BY quantity DESC) AS rk, dense_rank() OVER (ORDER BY quantity DESC) AS dr FROM order_items WHERE order_id IN (102, 105) ORDER BY quantity DESC, order_id, product_id
```

```result
order_id | product_id | quantity | rk | dr
105 | 3 | 2 | 1 | 1
105 | 4 | 2 | 1 | 1
102 | 3 | 1 | 3 | 2
102 | 4 | 1 | 3 | 2
105 | 5 | 1 | 3 | 2
```

both quantity 2 rows are 1 in both columns. then quantity 1 shows up. RANK counts the rows ahead of you, 2 of them, so you are third and number 2 never appears. DENSE_RANK counts distinct values ahead, so you are second. the Postgres docs say the same thing differently: RANK is the ROW_NUMBER of the first tied row, which here is 3.

i expected the two to disagree about the tie itself, but the difference only shows up one row later.

this bites on top N. top N means keeping the first N ranks. put the ranking inside a [subquery in FROM](./175-subquery-in-from.md) (an inner SELECT the outer one reads as a table) and keep rk <= 2: you get 2 rows. keep dr <= 2 and you get all 5. neither is wrong, so pick on purpose: ROW_NUMBER gives exactly N rows but breaks ties by luck.

### check yourself

1. this keeps dr <= 2 over the same slice. how many rows come back?
```sql
SELECT order_id, product_id FROM (SELECT order_id, product_id, dense_rank() OVER (ORDER BY quantity DESC) AS dr FROM order_items WHERE order_id IN (102, 105)) AS t WHERE dr <= 2 ORDER BY order_id, product_id
```
<details><summary>answer</summary>

```result
order_id | product_id
102 | 3
102 | 4
105 | 3
105 | 4
105 | 5
```
5, because the slice has only 2 distinct quantities and every row has dr 1 or 2. the tempting answer is 2, from reading <= 2 as two rows.

</details>

2. all 13 order_items rows: 1 has quantity 3, 5 have quantity 2, 7 have quantity 1. predict rk for each quantity.
```sql
SELECT DISTINCT quantity, rank() OVER (ORDER BY quantity DESC) AS rk FROM order_items ORDER BY quantity DESC
```
<details><summary>answer</summary>

```result
quantity | rk
3 | 1
2 | 2
1 | 7
```
quantity 1 has 1 + 5 = 6 rows ahead of it, so it is 7th. the tempting answer is 3, which is what DENSE_RANK would give.

</details>

---
prev: [187 ROW_NUMBER, numbering rows in order](./187-row-number-numbering-rows-in-order.md) | next: not written yet
