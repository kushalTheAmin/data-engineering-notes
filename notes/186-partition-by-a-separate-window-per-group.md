# 186: PARTITION BY, a separate window per group
builds on: [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md), [177 correlated subqueries](./177-correlated-subqueries-a-query-that-depends-on-the-outer-row.md), [184 window functions, a total next to every row](./184-window-functions-a-total-next-to-every-row.md), [185 OVER, the window a function looks through](./185-over-the-window-a-function-looks-through.md)
section: bigger queries, part 13, ~2 min read

masala chai is the cheapest thing in the shop, but measured against its own category its exactly average. same row, two answers.

PARTITION BY is how you pick who. it goes inside the OVER (the keyword that turns a function call into a window function) from [185](./185-over-the-window-a-function-looks-through.md) and cuts the window (the rows a function sees for the current row) into one group per value, so a row only sees its own group. the shop, the imaginary snack store these notes run on, has 3 categories: snack (dhokla, a steamed savory cake, khandvi, a rolled gram flour snack, fafda, a crisp gram flour strip), sweet (jalebi and kaju katli) and drink (masala chai, spiced tea).

```sql
SELECT name, category, price, avg(price) OVER (PARTITION BY category) AS category_avg FROM products ORDER BY product_id
```

```result
name | category | price | category_avg
dhokla | snack | 6.00 | 6.0
khandvi | snack | 7.50 | 6.0
jalebi | sweet | 5.00 | 8.5
kaju katli | sweet | 12.00 | 8.5
masala chai | drink | 3.00 | 3.0
fafda | snack | 4.50 | 6.0
```

dhokla, khandvi and fafda all see the same 6.00 because their windows are the same 3 snack rows. masala chai is alone in its category, so its window is just itself and the average is its own 3.00.

i expected PARTITION BY to need a GROUP BY next to it. there isnt one, all 6 rows come back. [GROUP BY](./143-group-by-one-group-per-value.md) with the same avg gives 3 rows:

```sql
SELECT category, avg(price) AS category_avg FROM products GROUP BY category ORDER BY category
```

```result
category | category_avg
drink | 3.0
snack | 6.0
sweet | 8.5
```

so GROUP BY shrinks the rows, PARTITION BY only shrinks what each row looks at.

the [correlated subquery](./177-correlated-subqueries-a-query-that-depends-on-the-outer-row.md) in 177 (an inner query rerun for each outer row) asked for products under their own categorys average and got fafda and jalebi. wrap this window query inside another query as its table and you get the same two.

### check yourself

1. predict the total column. the window runs after WHERE (keeps matching rows), same as in [184](./184-window-functions-a-total-next-to-every-row.md).
```sql
SELECT name, sum(price) OVER (PARTITION BY category) AS t FROM products WHERE price > 5 ORDER BY product_id
```
<details><summary>answer</summary>

```result
name | t
dhokla | 13.50
khandvi | 13.50
kaju katli | 12.00
```
fafda (4.50) and jalebi (5.00) are filtered out first, so the snack window is only 6.00 plus 7.50. the tempting answer is 18.00 for both snacks, from adding up the whole category.

</details>

2. someone writes PARTITION BY name, hoping for a per product comparison. what does price minus the average come out as?
```sql
SELECT name, price - avg(price) OVER (PARTITION BY name) AS d FROM products ORDER BY product_id
```
<details><summary>answer</summary>

```result
name | d
dhokla | 0.0
khandvi | 0.0
jalebi | 0.0
kaju katli | 0.0
masala chai | 0.0
fafda | 0.0
```
every name is its own group, so every window is one row and the average is the price itself. the tempting answer is the same numbers as OVER () in 185, from thinking any PARTITION BY still averages the whole shop.

</details>

---
prev: [185 OVER, the window a function looks through](./185-over-the-window-a-function-looks-through.md) | next: [187 ROW_NUMBER, numbering rows in order](./187-row-number-numbering-rows-in-order.md)
