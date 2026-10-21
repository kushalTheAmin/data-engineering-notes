# 143: GROUP BY, one group per value
builds on: [031 null, a marker for a missing value](./031-null.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [117 ORDER BY, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md), [137 aggregate functions, many rows in, one value out](./137-aggregate-functions-many-rows-in-one-value-out.md), [139 COUNT DISTINCT, counting different values](./139-count-distinct-counting-different-values.md)
section: summarizing data, part 7, ~2 min read

every aggregate so far squashed the whole table into one row. what if the owner wants one answer per category, not one for everything?

that is GROUP BY. it puts rows into one group per different value in a column, then runs the [aggregate](./137-aggregate-functions-many-rows-in-one-value-out.md) (many rows in, one value out) on each group, so you get one row per group. in python it is a loop that fills a dictionary of lists, then a count and an average over each list. here are all 6 products of the shop, the imaginary gujarati snack store these notes run on, as name, category, price:

```python
products = [("dhokla", "snack", 6.00), ("khandvi", "snack", 7.50), ("jalebi", "sweet", 5.00),
            ("kaju katli", "sweet", 12.00), ("masala chai", "drink", 3.00), ("fafda", "snack", 4.50)]
groups = {}
for name, category, price in products:
    groups.setdefault(category, []).append(price)
for category in sorted(groups):
    prices = groups[category]
    print(category, len(prices), sum(prices) / len(prices))
```

```output
drink 1 3.0
snack 3 6.0
sweet 2 8.5
```

the same in SQL:

```sql
SELECT category, count(*) AS n, avg(price) AS avg_price FROM products GROUP BY category ORDER BY category
```

```result
category | n | avg_price
drink | 1 | 3.0
snack | 3 | 6.0
sweet | 2 | 8.5
```

6 rows went in, 3 came out, one per different category. i expected GROUP BY to be new machinery, but its the dictionary of lists i already write in python.

[WHERE](./106-where-keeping-only-the-rows-that-match.md) (keeping matching rows) runs before the grouping, so only the kept rows land in groups. groups come back in no promised order, so add [ORDER BY](./117-order-by-sorting-by-one-or-more-columns.md) when order matters.

now a column with a [null](./031-null.md) (a missing value), the city of the 5 shop customers:

```sql
SELECT city, count(*) AS n FROM customers GROUP BY city ORDER BY city
```

```result
city | n
Edison | 1
Hoboken | 1
Jersey City | 2
NULL | 1
```

Esha has no city, and here that missing city gets its own group. count distinct (counting different values) skipped nulls in [139](./139-count-distinct-counting-different-values.md), GROUP BY keeps them.

so what: revenue per day, orders per customer, most reports are this shape. the next one groups by two columns at once.

### check yourself

1. without running it, how many rows come back?
```sql
SELECT category, count(*) AS n FROM products WHERE price > 5 GROUP BY category ORDER BY category
```
<details><summary>answer</summary>

```result
category | n
snack | 2
sweet | 1
```
2 rows. WHERE drops masala chai, fafda and jalebi (5.00 is not over 5) first, so drink never reaches the grouping, and an empty group never appears. the tempting answer is 3, from assuming every category always shows up.

</details>

2. order_ratings has 5 rows, stars being 5, 4, NULL, 3, NULL. count(stars) counts only the rows where stars is not null. predict the null row, both its n and its c.
```sql
SELECT stars, count(*) AS n, count(stars) AS c FROM order_ratings GROUP BY stars ORDER BY stars
```
<details><summary>answer</summary>

```result
stars | n | c
3 | 1 | 1
4 | 1 | 1
5 | 1 | 1
NULL | 2 | 0
```
the 2 unrated orders form one group, so n is 2, but count(stars) skips nulls so c is 0. the tempting answers are no null row at all, or c equal to n, from reading count(stars) as counting rows.

</details>

---
prev: [142 MIN and MAX, the smallest and biggest value](./142-min-and-max-the-smallest-and-biggest-value.md) | next: not written yet
