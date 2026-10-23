# 176: scalar subqueries, one value inside a query
builds on: [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [114 three valued logic, true, false and unknown](./114-three-valued-logic-true-false-and-unknown.md), [140 SUM and AVG, adding up and averaging](./140-sum-and-avg-adding-up-and-averaging.md), [174 subquery in WHERE](./174-subquery-in-where.md), [175 subquery in FROM](./175-subquery-in-from.md)
section: bigger queries, part 3, ~2 min read

which products cost more than the average product? [140](./140-sum-and-avg-adding-up-and-averaging.md) found the average price, 6.33, but WHERE price > 6.33 means typing a number i had to compute first.

a scalar subquery is a [subquery](./174-subquery-in-where.md) (a SELECT in parentheses inside another query) that returns one row and one column (zero rows is the one exception, below), so the outer query uses it as a plain value. 174 handed IN a list and [175](./175-subquery-in-from.md) handed FROM a table, this one hands a comparison a single number. in python it is a variable:

```python
products = [("dhokla", 6.00), ("khandvi", 7.50), ("jalebi", 5.00), ("kaju katli", 12.00), ("masala chai", 3.00), ("fafda", 4.50)]
avg_price = sum(p for _, p in products) / len(products)
print(avg_price)
print([n for n, p in products if p > avg_price])
```

```output
6.333333333333333
['khandvi', 'kaju katli']
```

the shop is the imaginary gujarati snack store these notes run on, and its 6 products are that list. in SQL the inner query goes right where the variable would be:

```sql
SELECT name, price FROM products WHERE price > (SELECT avg(price) FROM products) ORDER BY price
```

```result
name | price
khandvi | 7.50
kaju katli | 12.00
```

the inner query runs once and becomes 6.333..., then [WHERE](./106-where-keeping-only-the-rows-that-match.md) tests every product against it. i expected the average to need saving somewhere first, but it just sits in the parentheses like a number i typed.

the catch is the word "exactly". two sweets exist, jalebi at 5.00 and kaju katli at 12.00, so this has two values to compare against:

```sql
-- fails on purpose
SELECT name FROM products WHERE price > (SELECT price FROM products WHERE category = 'sweet')
```

DuckDB (what these notes run in) errors here, and Postgres (a server database) does too. but zero rows is not an error: the value just becomes NULL (a missing value), the comparison is [unknown](./114-three-valued-logic-true-false-and-unknown.md) for every row, and you get an empty result with no warning. a typo in the inner filter looks like "nothing matched".

### check yourself

1. the shop has 6 products. how many cost less than the average?
```sql
SELECT name FROM products WHERE price < (SELECT avg(price) FROM products) ORDER BY price
```
<details><summary>answer</summary>

```result
name
masala chai
fafda
jalebi
dhokla
```
4, because the average is 6.33 and only khandvi and kaju katli are above it. the tempting answer is 3, from assuming an average splits the list in half. one big price (12.00) pulls it up.

</details>

2. you type category = 'frozen' in the inner filter of the sweet query above. error or rows?
```sql
SELECT name FROM products WHERE price > (SELECT price FROM products WHERE category = 'frozen')
```
<details><summary>answer</summary>

```result
name
```
no rows and no error. the inner query returns nothing, so the value is NULL and every comparison is unknown. the tempting answer is an error, from thinking an empty inner result is the same as too many rows.

</details>

---
prev: [175 subquery in FROM](./175-subquery-in-from.md) | next: not written yet
