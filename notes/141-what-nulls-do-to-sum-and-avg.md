# 141: what NULLs do to SUM and AVG
builds on: [031 null, a marker for a missing value](./031-null.md), [032 null is not zero and not empty text](./032-null-is-not-zero-or-empty-text.md), [116 COALESCE, a fallback when a value is NULL](./116-coalesce-a-fallback-when-a-value-is-null.md), [137 aggregate functions, many rows in, one value out](./137-aggregate-functions-many-rows-in-one-value-out.md), [138 COUNT star vs COUNT of a column](./138-count-star-vs-count-of-a-column.md), [140 SUM and AVG, adding up and averaging](./140-sum-and-avg-adding-up-and-averaging.md)
section: summarizing data, part 5, ~2 min read

when sum or avg meets a row with no value, does it add a zero, count the row, or just look away?

it looks away. a [null](./031-null.md) (a missing value) is not added and not counted, the skip count(column) made in [138](./138-count-star-vs-count-of-a-column.md). that is why avg divides by count(column) (rows with a value), not by count(*) (all rows). in [116](./116-coalesce-a-fallback-when-a-value-is-null.md) a COALESCE (a fallback value for nulls) turned an average of 4.0 into 2.4, this is the rule underneath. the loop by hand, on order_ratings, the ratings table of the shop, the imaginary snack store these notes use:

| order_id | stars | total after | counted after |
|---|---|---|---|
| 101 | 5 | 5 | 1 |
| 102 | 4 | 9 | 2 |
| 103 | NULL | 9 | 2 |
| 105 | 3 | 12 | 3 |
| 107 | NULL | 12 | 3 |

the null rows change nothing. the total ends at 12, the count at 3, and [avg](./140-sum-and-avg-adding-up-and-averaging.md) (the total over the count) is 12 over 3. DuckDB, the database these notes run, agrees:

```sql
SELECT sum(stars) AS total, count(stars) AS counted, count(*) AS rows_in, avg(stars) AS avg_stars, sum(stars) * 1.0 / count(*) AS sum_over_rows FROM order_ratings
```

```result
total | counted | rows_in | avg_stars | sum_over_rows
12 | 3 | 5 | 4.0 | 2.4
```

i assumed a missing rating would sit in the average as a quiet zero, but the row just isnt in the vote. so avg(stars) is not sum(stars) / count(*). writing it by hand gives 2.4, the wrecked number from the zero filled column from [032](./032-null-is-not-zero-or-empty-text.md).

now only the unrated orders:

```sql
SELECT sum(stars) AS total, avg(stars) AS avg_stars, count(*) AS rows_in FROM order_ratings WHERE stars IS NULL
```

```result
total | avg_stars | rows_in
NULL | NULL | 2
```

2 rows went in, nothing got added, so the answer is NULL, not 0. same as the empty sum in [137](./137-aggregate-functions-many-rows-in-one-value-out.md). the Postgres docs, a server database, define avg and sum over the non-null input values, so this isnt a DuckDB quirk.

so what: an average over an optional field only counts the people who filled it in. if you care about the rows that skipped it, ask count(*) minus count(column).

### check yourself

1. predict all three, without running it.
```sql
SELECT sum(stars) AS s, avg(stars) AS a, sum(stars) * 1.0 / count(*) AS r FROM order_ratings WHERE order_id >= 103
```
<details><summary>answer</summary>

```result
s | a | r
3 | 3.0 | 1.0
```
the rows are 103 (null), 105 (3) and 107 (null). only the 3 is added and counted, so avg is 3.0. r divides by all 3 rows, so 1.0. the tempting answer for a is 1.0, from dividing by every row.

</details>

2. a teammate says avg(stars) is wrong because it ignores the 2 unrated orders, and wants sum(stars) / count(*). the owner asked "how happy are people who rated?". who is right?
<details><summary>answer</summary>

avg(stars) is right, 4.0 for the 3 people who rated. sum over count(*) gives 2.4, which treats silence as a zero star rating. the tempting reply is the teammate, because count(*) feels like the honest count of orders.

</details>

---
prev: [140 SUM and AVG, adding up and averaging](./140-sum-and-avg-adding-up-and-averaging.md) | next: not written yet
