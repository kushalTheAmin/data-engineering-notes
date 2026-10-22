# 150: percentiles, the medians cousins
builds on: [149 median, the middle value after sorting](./149-median-the-middle-value-after-sorting.md), [137 aggregate functions, many rows in, one value out](./137-aggregate-functions-many-rows-in-one-value-out.md), [135 one language, many dialects](./135-one-language-many-dialects.md), [101 SQL, you describe the result](./101-sql-you-describe-the-result.md)
section: summarizing data, part 14, ~2 min read

kaju katli (a cashew sweet) costs 12.00, the most in the shop, so what price sits 90% of the way up the sorted prices? by blending the neighbors its not 12.00, and its not any price on the menu.

a percentile is the value some fraction of the way through a sorted column (here, all the prices in order). the [median](./149-median-the-middle-value-after-sorting.md) (the middle of the sorted values) is just the 0.5 one, and the 90th percentile is 0.9. in python, on the 6 prices of the shop, the imaginary gujarati snack store these notes run on:

```python
prices = sorted([6.00, 7.50, 5.00, 12.00, 3.00, 4.50])
pos = 0.9 * (len(prices) - 1)
low = int(pos)
print(pos)
print(prices[low] + (pos - low) * (prices[low + 1] - prices[low]))
```

```output
4.5
9.75
```

6 sorted values have positions 0 to 5, so 0.9 of the way is position 4.5. that lands halfway between 7.5 and 12.0, and halfway is 9.75. in [SQL](./101-sql-you-describe-the-result.md) (the language for asking a database for rows) it is an [aggregate](./137-aggregate-functions-many-rows-in-one-value-out.md) (many rows in, one value out):

```sql
SELECT quantile_cont(price, 0.5) AS p50, quantile_cont(price, 0.9) AS p90, quantile_disc(price, 0.9) AS p90_real FROM products
```

```result
p50 | p90 | p90_real
5.50 | 9.75 | 12.00
```

p50 is the median again. i kept reading 90th percentile as 90% of the biggest value, which would be 10.80, but the 90% is about position in the sorted list. like an even-count median, it can be a price nobody charges. in DuckDB (what these notes run in), quantile_cont (continuous) blends neighbors, quantile_disc (discrete) picks a real value, here 12.00.

so what: if you only watch the average you miss the slow ones. the Google SRE book has a section on worrying about the slowest requests, and says most requests being near the mean is "hopeful thinking".

[Postgres](./135-one-language-many-dialects.md) (a server database) spells it like this:

```text
-- Postgres
SELECT percentile_cont(0.9) WITHIN GROUP (ORDER BY price) FROM products
```

### check yourself

1. no running it. the snack category holds dhokla 6.00, khandvi 7.50 and fafda 4.50. what does this return?
```sql
SELECT category, quantile_cont(price, 0.9) AS p90 FROM products WHERE category = 'snack' GROUP BY category
```
<details><summary>answer</summary>

```result
category | p90
snack | 7.20
```
sorted that is 4.50, 6.00, 7.50 at positions 0, 1, 2. 0.9 of the way is position 1.8, which is 6.00 plus 0.8 of the gap to 7.50, so 7.20. the tempting answer is 7.50, from thinking the 90th percentile is the top value of a small list.

</details>

2. a column holds the numbers 1 to 10. what is the 90th percentile with quantile_cont, and why is 9 the wrong answer?
<details><summary>answer</summary>

9.1. 10 values sit at positions 0 to 9, so 0.9 is position 8.1, which is the value 9 (position 8) plus 0.1 of the step to 10. 9 is wrong because it is the 9th value, and the 90th percentile is a fraction of the way through the positions, not a count of values.

</details>

---
prev: [149 median, the middle value after sorting](./149-median-the-middle-value-after-sorting.md) | next: [151 pivoting, turning rows into columns](./151-pivoting-turning-rows-into-columns.md)
