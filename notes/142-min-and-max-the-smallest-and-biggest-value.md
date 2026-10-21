# 142: MIN and MAX, the smallest and biggest value
builds on: [031 null, a marker for a missing value](./031-null.md), [117 ORDER BY, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md), [120 LIMIT and OFFSET, paging through rows](./120-limit-and-offset-paging-through-rows.md), [137 aggregate functions, many rows in, one value out](./137-aggregate-functions-many-rows-in-one-value-out.md), [141 what NULLs do to SUM and AVG](./141-what-nulls-do-to-sum-and-avg.md)
section: summarizing data, part 6, ~2 min read

SQL will hand you the highest price in one word. but can it hand you the product that has that price?

min and max are [aggregate functions](./137-aggregate-functions-many-rows-in-one-value-out.md) (many rows in, one value out) that return the smallest and the biggest value in a column. in python it is a loop keeping a best so far. they work on anything that can be put in order, so numbers, text (first and last alphabetically) and dates (earliest and latest). on products, the table of the shop, the imaginary snack store these notes use:

```sql
SELECT min(price) AS cheapest, max(price) AS priciest, min(name) AS first_name, max(name) AS last_name FROM products
```

```result
cheapest | priciest | first_name | last_name
3.00 | 12.00 | dhokla | masala chai
```

3.00 belongs to masala chai (spiced tea) and 12.00 to kaju katli (a cashew sweet), but the result doesnt say so. i assumed max(price) would carry its row along, and it only returns the value. first_name and last_name are a separate question, the alphabet, so dhokla (a steamed savory cake) comes first even though its not the cheapest.

to get the product, sort and keep one row, the [ORDER BY](./117-order-by-sorting-by-one-or-more-columns.md) plus [LIMIT](./120-limit-and-offset-paging-through-rows.md) pair:

```sql
SELECT name, price FROM products ORDER BY price DESC LIMIT 1
```

```result
name | price
kaju katli | 12.00
```

like sum and avg in [141](./141-what-nulls-do-to-sum-and-avg.md), min and max skip [nulls](./031-null.md) (missing values). min(stars) over the 5 ratings is 3, not NULL, and with only nulls in, the answer is NULL. the Postgres docs, a server database, say the same, min and max work on the non-null input values.

so what: max over a timestamp column, like max(ordered_at) on orders, is the quick way to ask when the newest row landed. here it is 2026-04-09 13:45:00.

---
prev: [141 what NULLs do to SUM and AVG](./141-what-nulls-do-to-sum-and-avg.md) | next: not written yet
