# 149: median, the middle value after sorting
builds on: [101 SQL, you describe the result](./101-sql-you-describe-the-result.md), [135 one language, many dialects](./135-one-language-many-dialects.md), [137 aggregate functions, many rows in, one value out](./137-aggregate-functions-many-rows-in-one-value-out.md), [140 SUM and AVG, adding up and averaging](./140-sum-and-avg-adding-up-and-averaging.md), [141 what NULLs do to SUM and AVG](./141-what-nulls-do-to-sum-and-avg.md), [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md)
section: summarizing data, part 13, ~2 min read

the average price in the shop is 6.33, but 4 of the 6 products cost less than that. so is 6.33 really a typical price?

the median is the middle value once you sort the column. [avg](./140-sum-and-avg-adding-up-and-averaging.md) (total divided by count) feels every value, the median cares only about position. in python it is a sort and a pick, here on the 6 prices of the shop, the imaginary gujarati snack store these notes run on:

```python
prices = sorted([6.00, 7.50, 5.00, 12.00, 3.00, 4.50])
print(prices)
mid = len(prices) // 2
print((prices[mid - 1] + prices[mid]) / 2)
```

```output
[3.0, 4.5, 5.0, 6.0, 7.5, 12.0]
5.5
```

that pick fits an even count only. 6 values have no single middle, so you average the two in the middle, 5.0 and 6.0. i figured the middle of an even list would just pick one, and it quietly makes up a number. in [SQL](./101-sql-you-describe-the-result.md) (the language for asking a database for rows) it is one word, an [aggregate](./137-aggregate-functions-many-rows-in-one-value-out.md) (many rows in, one value out):

```sql
SELECT median(price) AS middle, avg(price) AS average FROM products
```

```result
middle | average
5.50 | 6.333333333333333
```

per [category](./143-group-by-one-group-per-value.md) (one row per value):

```sql
SELECT category, median(price) AS middle FROM products GROUP BY category ORDER BY category
```

```result
category | middle
drink | 3.00
snack | 6.00
sweet | 8.50
```

snack has 3 products, an odd count, so the median is a real price: dhokla (a steamed savory cake) at 6.00. sweet has 2, 5.00 and 12.00, so 8.50, which nothing costs.

so what: imagine kaju katli (a cashew sweet) cost 120.00, and avg jumps to 24.33 while the median stays 5.50. when a few huge values would skew an average, the median is the number to look at.

one dialect note ([135](./135-one-language-many-dialects.md), each database has its own spelling): DuckDB has a one-word median, as do some other databases, but Postgres, a server database, has none and spells it this longer way, where 0.5 means halfway through the sorted values:

```text
-- Postgres
SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY price) FROM products
```

### check yourself

1. [nulls](./141-what-nulls-do-to-sum-and-avg.md) (missing values) are skipped by sum and avg. without running it, what does median do with them here? order_ratings holds 5 ratings. stars is 5, 4, null, 3, null, and stars_zero_filled stores 0 for the unrated ones.
```sql
SELECT median(stars) AS with_nulls, median(stars_zero_filled) AS zero_filled FROM order_ratings
```
<details><summary>answer</summary>

```result
with_nulls | zero_filled
4.0 | 3.0
```
median skips nulls too, so stars votes on 5, 4, 3 and the middle is 4. the zero-filled column votes on 0, 0, 3, 4, 5 and the middle is 3. the tempting answer is 4 for both, but a 0 is a value and it moves the middle.

</details>

2. what does this python print, and does it match the 5.50 above?
```python
prices = sorted([6.00, 7.50, 5.00, 12.00, 3.00, 4.50])
print(prices[len(prices) // 2])
```
<details><summary>answer</summary>

```output
6.0
```
index 3 is the upper of the two middle values, so it prints 6.0 and skips the averaging. with an even count the median needs both middles, 5.0 and 6.0. the tempting answer is 5.5, from assuming any middle pick gives the median.

</details>

---
prev: [148 conditional aggregation, counting several things in one pass](./148-conditional-aggregation-counting-several-things-in-one-pass.md) | next: [150 percentiles, the medians cousins](./150-percentiles-the-medians-cousins.md)
