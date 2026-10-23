# 177: correlated subqueries, a query that depends on the outer row
builds on: [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [140 SUM and AVG, adding up and averaging](./140-sum-and-avg-adding-up-and-averaging.md), [158 table aliases, short nicknames for tables](./158-table-aliases-short-nicknames-for-tables.md), [176 scalar subqueries, one value inside a query](./176-scalar-subqueries-one-value-inside-a-query.md)
section: bigger queries, part 4, ~2 min read

which products are cheaper than the average of their own category? [176](./176-scalar-subqueries-one-value-inside-a-query.md) compared against one shop-wide average, but a jalebi should be judged against sweets, not against everything.

a correlated subquery is a scalar subquery (an inner query that returns one value) that uses a column of the outer row, so it has to be asked again for every outer row. the shop is the imaginary gujarati snack store these notes run on, and each of its 6 products gets its own inner question:

| outer row | inner question | answer | price < answer? |
|---|---|---|---|
| dhokla 6.00 | avg price of snack | 6.00 | no, equal |
| khandvi 7.50 | avg price of snack | 6.00 | no |
| jalebi 5.00 | avg price of sweet | 8.50 | yes |
| kaju katli 12.00 | avg price of sweet | 8.50 | no |
| masala chai 3.00 | avg price of drink | 3.00 | no, equal |
| fafda 4.50 | avg price of snack | 6.00 | yes |

```sql
SELECT name, price FROM products p WHERE price < (SELECT avg(price) FROM products WHERE category = p.category) ORDER BY price
```

```result
name | price
fafda | 4.50
jalebi | 5.00
```

the nickname p ([table alias](./158-table-aliases-short-nicknames-for-tables.md), a short name valid for one query) is what makes it work. inside the parentheses, plain category means the inner products, and p.category means the row the outer query is on right now. it is a loop inside a loop: for each product, average the products whose category matches.

i assumed the inner query was a fixed thing that ran once, like in 176, but here it changes with every row. the shop-wide version of this question returns 4 products, this one returns 2.

the database is allowed to find a faster plan than a literal loop as long as the answer is the same, but if a correlated query on a big table crawls for you, this is the first shape i would suspect.

### check yourself

1. change < to >= in the query above. how many rows come back, and does fafda stay in?
<details><summary>answer</summary>

```sql
SELECT name, price FROM products p WHERE price >= (SELECT avg(price) FROM products WHERE category = p.category) ORDER BY price
```

```result
name | price
masala chai | 3.00
dhokla | 6.00
khandvi | 7.50
kaju katli | 12.00
```
4 rows, and fafda drops out, along with jalebi. >= is the opposite of <, so it keeps the ties, dhokla and masala chai, plus everything above the average. the tempting answer is 2 or 3, from thinking >= only adds ties to the old result.

</details>

2. someone forgets the p. and writes the inner filter as category = category. error or rows?
```sql
SELECT name, price FROM products p WHERE price < (SELECT avg(price) FROM products WHERE category = category) ORDER BY price
```
<details><summary>answer</summary>

```result
name | price
masala chai | 3.00
fafda | 4.50
jalebi | 5.00
dhokla | 6.00
```
no error. plain category means the inner table both times, so it compares a column to itself, always true, and the inner query is the shop-wide average 6.33 again. the tempting answer is an error, but the query is valid, it just stopped being correlated.

</details>

---
prev: [176 scalar subqueries, one value inside a query](./176-scalar-subqueries-one-value-inside-a-query.md) | next: not written yet
