# 138: COUNT star vs COUNT of a column
builds on: [031 null, a marker for a missing value](./031-null.md), [032 null is not zero and not empty text](./032-null-is-not-zero-or-empty-text.md), [115 IS NULL and IS NOT NULL](./115-is-null-and-is-not-null.md), [137 aggregate functions, many rows in, one value out](./137-aggregate-functions-many-rows-in-one-value-out.md)
section: summarizing data, part 2, ~2 min read

how many of the shop delivered orders got a rating? depends which count you type, one says 5 and another says 3.

in [137](./137-aggregate-functions-many-rows-in-one-value-out.md) count(*) counted rows. count(column) is the same loop with one extra line, skip the row when that column is [null](./031-null.md) (a missing value). in python that is `if v is not None: n += 1`, and count(*) has no if.

the shop, the imaginary gujarati snack store these notes run on, keeps ratings in order_ratings, built in [032](./032-null-is-not-zero-or-empty-text.md). stars is null when nobody rated, stars_zero_filled stores 0 instead:

```sql
SELECT count(*) AS rows_in, count(stars) AS rated, count(stars_zero_filled) AS zero_filled FROM order_ratings
```

```result
rows_in | rated | zero_filled
5 | 3 | 5
```

same 5 rows, three answers. stars_zero_filled has no nulls to skip, so its count claims all 5 orders were rated. thats the 0 trap from 032 again, just in a count this time.

now only the rows where [stars IS NULL](./115-is-null-and-is-not-null.md) (the test for a missing value):

```sql
SELECT count(*) AS rows_in, count(stars) AS rated FROM order_ratings WHERE stars IS NULL
```

```result
rows_in | rated
2 | 0
```

i figured counting only nulls would give NULL, like sum did on no rows in 137. but count never returns null, it gives 0.

so what: count(*) minus count(column) is how many values are missing, a cheap check people run on a fresh table. Postgres docs define them the same way, count(*) counts input rows and count of a column counts rows where the value is not null. the next one is about counting different values, not rows.

### check yourself

1. predict all three numbers. the WHERE keeps the ratings for orders 105 and 107.
```sql
SELECT count(*) AS n, count(stars) AS c, count(stars_zero_filled) AS z FROM order_ratings WHERE order_id >= 105
```
<details><summary>answer</summary>

```result
n | c | z
2 | 1 | 2
```
order 107 has null stars, so only 105 counts for c. z counts both, because 0 is a value. the tempting answer is 2 for c, from reading a null as just another rating.

</details>

2. the owner wants the share of delivered orders that were rated, as a percent. someone wrote count(stars_zero_filled) * 100.0 / count(*). what does it return, and what should it be?
```sql
SELECT count(stars) * 100.0 / count(*) AS pct_rated FROM order_ratings
```
<details><summary>answer</summary>

```result
pct_rated
60.0
```
the broken one returns 100.0, since both counts are 5. the fixed one is 3 out of 5, so 60.0. the tempting answer is that they match, because both columns look like ratings.

</details>

---
prev: [137 aggregate functions, many rows in, one value out](./137-aggregate-functions-many-rows-in-one-value-out.md) | next: not written yet
