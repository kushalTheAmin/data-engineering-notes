# 193: top N per group
builds on: [175 subquery in FROM](./175-subquery-in-from.md), [186 PARTITION BY, a separate window per group](./186-partition-by-a-separate-window-per-group.md), [187 ROW_NUMBER, numbering rows in order](./187-row-number-numbering-rows-in-order.md)
section: bigger queries, part 20, ~2 min read

want the 2 priciest products in every category? my first move was to put row_number() right in the WHERE, and the database just said no.

top N per group means: split the rows into groups, rank each group, keep only the first N of each. the shop, the imaginary snack store these notes run on, has 3 categories: snack (dhokla 6.00, khandvi 7.50, fafda 4.50), sweet (jalebi 5.00, kaju katli 12.00) and drink (masala chai 3.00). a window function (a calculation that keeps every row) like [ROW_NUMBER](./187-row-number-numbering-rows-in-order.md) (numbers rows 1, 2, 3) runs after WHERE (keeps matching rows), so WHERE cant see the number yet:

```sql
-- fails on purpose
SELECT name FROM products WHERE row_number() OVER (PARTITION BY category ORDER BY price DESC) <= 2
```

the fix is a [subquery in FROM](./175-subquery-in-from.md) (an inner SELECT the outer one reads like a table). number the rows inside, filter on the number outside. [PARTITION BY](./186-partition-by-a-separate-window-per-group.md) (one window per value) restarts the count in each category:

```sql
SELECT name, category, price FROM (SELECT name, category, price, row_number() OVER (PARTITION BY category ORDER BY price DESC) AS rn FROM products) AS t WHERE rn <= 2 ORDER BY category, price DESC
```

```result
name | category | price
masala chai | drink | 3.00
khandvi | snack | 7.50
dhokla | snack | 6.00
kaju katli | sweet | 12.00
jalebi | sweet | 5.00
```

5 of the 6 products: fafda was 3rd of the snacks so it got cut. masala chai is alone in drinks, and asking for 2 just gives you 1, no error and no padding. change the 2 to a 1 and you get the priciest product per category.

i assumed top N needed its own feature, but its just two ideas stacked, and it runs in Postgres too.

this is the shape behind "latest order per customer". if prices can tie at the cut, add a second sort column, or which row survives isnt promised.

### check yourself

1. a teammate drops PARTITION BY category from the inner query and keeps rn <= 2. how many rows come back, and which?
```sql
SELECT name, price FROM (SELECT name, price, row_number() OVER (ORDER BY price DESC) AS rn FROM products) AS t WHERE rn <= 2 ORDER BY price DESC
```
<details><summary>answer</summary>

```result
name | price
kaju katli | 12.00
khandvi | 7.50
```
with no PARTITION BY the whole table is one window, so you get the 2 priciest products overall. the tempting answer is still 5 rows, from thinking the 2 means per category by itself.

</details>

2. flip the sort to ascending and keep only rn = 1. which products come back?
```sql
SELECT name FROM (SELECT name, row_number() OVER (PARTITION BY category ORDER BY price) AS rn FROM products) AS t WHERE rn = 1 ORDER BY name
```
<details><summary>answer</summary>

```result
name
fafda
jalebi
masala chai
```
ascending puts the cheapest first in each category, and fafda (4.50) beats dhokla (6.00) and khandvi. the tempting answer is dhokla, the first snack row in the table.

</details>

---
prev: [192 LAG and LEAD, looking at the row before](./192-lag-and-lead-looking-at-the-row-before.md) | next: not written yet
