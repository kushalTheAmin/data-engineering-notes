# 184: window functions, a total next to every row
builds on: [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [140 sum and avg, adding up and averaging](./140-sum-and-avg-adding-up-and-averaging.md), [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md), [175 subquery in FROM](./175-subquery-in-from.md)
section: bigger queries, part 11, ~2 min read

how do you show every product next to the total of all prices? [GROUP BY](./143-group-by-one-group-per-value.md) (one row per different value) gave me the total and threw the product rows away, and i needed both on one line.

a window function is an aggregate that doesnt collapse anything. every row keeps itself and also gets the aggregate answer beside it. you write it by putting OVER () after the aggregate. the empty parentheses mean the window is every row, a later note opens them up. this is the shop, the imaginary gujarati snack store these notes run on, and its 6 products (dhokla, a steamed savory cake, khandvi, a rolled gram flour snack, jalebi and kaju katli, sweets, masala chai, spiced tea, fafda, a crisp gram flour strip). in python it is two steps, total first, then a loop that hands the total to every row:

```python
prices = {"dhokla": 6.0, "khandvi": 7.5, "jalebi": 5.0, "kaju katli": 12.0, "masala chai": 3.0, "fafda": 4.5}
total = sum(prices.values())
for name, price in prices.items():
    print(name, price, total)
```

```output
dhokla 6.0 38.0
khandvi 7.5 38.0
jalebi 5.0 38.0
kaju katli 12.0 38.0
masala chai 3.0 38.0
fafda 4.5 38.0
```

and in SQL, [sum](./140-sum-and-avg-adding-up-and-averaging.md) (adds up a column) with OVER ():

```sql
SELECT name, price, sum(price) OVER () AS total FROM products ORDER BY product_id
```

```result
name | price | total
dhokla | 6.00 | 38.00
khandvi | 7.50 | 38.00
jalebi | 5.00 | 38.00
kaju katli | 12.00 | 38.00
masala chai | 3.00 | 38.00
fafda | 4.50 | 38.00
```

6 rows in, 6 rows out. plain sum(price) would have given 1 row. the thing that surprised me is when it runs: after [WHERE](./106-where-keeping-only-the-rows-that-match.md) has already thrown rows out, so the window only adds up the survivors. Postgres docs say the same, a filtered out row is never seen by a window function.

a row next to its total is how percent of total reports get built, one divide away.

### check yourself

1. the average price is 6.33. which products are above it? the inner query keeps every row, so a [subquery in FROM](./175-subquery-in-from.md) lets the outer WHERE use the average.
```sql
SELECT name FROM (SELECT name, price, avg(price) OVER () AS a FROM products) AS t WHERE price > a ORDER BY name
```
<details><summary>answer</summary>

```result
name
kaju katli
khandvi
```
dhokla costs 6.00, under 6.33, so it stays out. the tempting answer includes dhokla, from treating 6 as about average.

</details>

2. predict the total column when WHERE only lets snacks through.
```sql
SELECT name, sum(price) OVER () AS total FROM products WHERE category = 'snack' ORDER BY product_id
```
<details><summary>answer</summary>

```result
name | total
dhokla | 18.00
khandvi | 18.00
fafda | 18.00
```
6 plus 7.5 plus 4.5 is 18. the window runs after WHERE, so it only sees the 3 snacks. the tempting answer is 38.00, from thinking OVER () always means the whole table.

</details>

---
prev: [183 INTERSECT and EXCEPT](./183-intersect-and-except.md) | next: not written yet
