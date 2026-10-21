# 140: SUM and AVG, adding up and averaging
builds on: [019 floating point](./019-floating-point.md), [022 exact decimal types](./022-exact-decimal-types.md), [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [101 SQL, you describe the result](./101-sql-you-describe-the-result.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [137 aggregate functions, many rows in, one value out](./137-aggregate-functions-many-rows-in-one-value-out.md), [139 COUNT DISTINCT, counting different values](./139-count-distinct-counting-different-values.md)
section: summarizing data, part 4, ~2 min read

whats the average price of a product in the shop, and does any product actually cost that?

sum adds up the values in a column, and avg is that total divided by how many values were added. both are [aggregate functions](./137-aggregate-functions-many-rows-in-one-value-out.md) (many rows in, one value out), like count in [139](./139-count-distinct-counting-different-values.md). in python it is a loop with a running total and a counter, here on the 6 prices of the shop, the imaginary snack store these notes use:

```python
prices = [6.00, 7.50, 5.00, 12.00, 3.00, 4.50]
total = 0
count = 0
for p in prices:
    total += p
    count += 1
print(total, count, total / count)
```

```output
38.0 6 6.333333333333333
```

the same in [SQL](./101-sql-you-describe-the-result.md) (the language for asking a database for rows). products is a [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows) and price is one of its columns. AS just names the result column:

```sql
SELECT sum(price) AS total, avg(price) AS average, count(*) AS n FROM products
```

```result
total | average | n
38.00 | 6.333333333333333 | 6
```

no product costs 6.33. dhokla, a steamed savory cake, is 6.00, khandvi 7.50. i assumed avg was its own special operation, but its just the sum over how many values got added, so kaju katli at 12.00 drags it up.

38.00 versus 38.0 is not a bug. price is an [exact decimal](./022-exact-decimal-types.md) (digits kept exactly), so the sum keeps its two decimals. avg comes back as a [float](./019-floating-point.md) (a binary approximation) in DuckDB, the database these notes use. 38 over 6 never ends in decimal either.

[WHERE](./106-where-keeping-only-the-rows-that-match.md) (keep matching rows) runs first, so only rows whose category column says snack get added up:

```sql
SELECT sum(price) AS total, avg(price) AS average, count(*) AS n FROM products WHERE category = 'snack'
```

```result
total | average | n
18.00 | 6.0 | 3
```

this time 6.0 is exactly the price of dhokla, so sometimes avg hits a real row. so what: avg hides outliers like that 12.00, so when you see one, look at the rows behind it.

---
prev: [139 COUNT DISTINCT, counting different values](./139-count-distinct-counting-different-values.md) | next: [141 what NULLs do to SUM and AVG](./141-what-nulls-do-to-sum-and-avg.md)
