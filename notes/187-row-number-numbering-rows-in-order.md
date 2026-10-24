# 187: ROW_NUMBER, numbering rows in order
builds on: [117 ORDER BY, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md), [184 window functions, a total next to every row](./184-window-functions-a-total-next-to-every-row.md), [185 OVER, the window a function looks through](./185-over-the-window-a-function-looks-through.md), [186 PARTITION BY, a separate window per group](./186-partition-by-a-separate-window-per-group.md)
section: bigger queries, part 14, ~2 min read

dhokla is the first row of the products table, so why does it come out numbered 3?

ROW_NUMBER() is a [window function](./184-window-functions-a-total-next-to-every-row.md) (a calculation that keeps every row) that hands out 1, 2, 3 and so on. you put an [ORDER BY](./117-order-by-sorting-by-one-or-more-columns.md) (sort rows by a column) inside the [OVER](./185-over-the-window-a-function-looks-through.md) to say what order to count in. the shop, the imaginary snack store these notes run on, has 6 products (dhokla, a steamed savory cake, khandvi, a rolled gram flour snack, jalebi and kaju katli, sweets, masala chai, spiced tea, fafda, a crisp gram flour strip). number them from priciest down:

```sql
SELECT name, price, row_number() OVER (ORDER BY price DESC) AS rn FROM products ORDER BY product_id
```

```result
name | price | rn
dhokla | 6.00 | 3
khandvi | 7.50 | 2
jalebi | 5.00 | 4
kaju katli | 12.00 | 1
masala chai | 3.00 | 6
fafda | 4.50 | 5
```

the rows come out in product_id order, but each one carries its place in the price ranking. kaju katli costs the most so it is 1, dhokla is third. i kept reading rn as a position in the output, and its not, its a label that was stuck on while the window did its own sort. add ORDER BY rn on the outside if you want the rows lined up.

a catch: if two rows tie, the Postgres docs say tied rows are numbered in an unspecified order. shop prices are all different so nothing ties here, but add a second sort column whenever they could, or nothing promises the same numbers twice.

### check yourself

1. predict rn. [PARTITION BY](./186-partition-by-a-separate-window-per-group.md) (one window per value) restarts the count in every category.
```sql
SELECT name, row_number() OVER (PARTITION BY category ORDER BY price DESC) AS rn FROM products ORDER BY product_id
```
<details><summary>answer</summary>

```result
name | rn
dhokla | 2
khandvi | 1
jalebi | 2
kaju katli | 1
masala chai | 1
fafda | 3
```
each category counts from 1 on its own, and fafda is the cheapest of 3 snacks. the tempting answer is 1 to 6 down the column, from forgetting the count restarts.

</details>

2. in order_items, 5 rows have quantity 2. with only ORDER BY quantity DESC, can you say which gets number 2? what one change makes it certain?
```sql
SELECT order_id, product_id FROM (SELECT order_id, product_id, row_number() OVER (ORDER BY quantity DESC, product_id) AS rn FROM order_items) AS t WHERE rn = 2
```
<details><summary>answer</summary>

```result
order_id | product_id
101 | 1
```
no. one row has quantity 3 and takes number 1, then 5 rows tie for numbers 2 to 6, so any could be 2. adding product_id as a tiebreaker settles it. the tempting answer is the first one stored in the table, which only holds until the order changes.

</details>

---
prev: [186 PARTITION BY, a separate window per group](./186-partition-by-a-separate-window-per-group.md) | next: [188 RANK vs DENSE_RANK, what ties do](./188-rank-vs-dense-rank-what-ties-do.md)
