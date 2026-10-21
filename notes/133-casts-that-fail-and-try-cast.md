# 133: casts that fail, and TRY_CAST
builds on: [031 null, a marker for a missing value](./031-null.md), [114 three valued logic](./114-three-valued-logic-true-false-and-unknown.md), [132 CAST, changing a values type](./132-cast-changing-a-values-type.md)
section: asking questions with SQL, part 33, ~2 min read

what does CAST do when the text isnt a number at all? it doesnt return something weird, it blows up the whole query.

TRY_CAST(value AS type) is [CAST](./132-cast-changing-a-values-type.md) (change a values type) that returns [null](./031-null.md), the missing-value marker, when the value cant be converted. DuckDB has it, Postgres, a server database, doesnt.

the shop, the imaginary gujarati snack store these notes run on, got a supplier price list typed by hand, so every price is text. jalebi says n/a, and kaju katli says 12,00, a comma as the decimal mark. the whole list is 5 rows.

```sql
-- fails on purpose
SELECT CAST(price_text AS DECIMAL(6, 2)) FROM price_export
```

DECIMAL(6, 2) means a number with at most 6 digits, 2 of them after the point. one bad value and DuckDB, the database these notes run queries in, stops with a conversion error. no rows at all, not even the good ones. now TRY_CAST:

```sql
SELECT name, price_text, TRY_CAST(price_text AS DECIMAL(6, 2)) AS price FROM price_export ORDER BY product_id
```

```result
name | price_text | price
dhokla | 6.00 | 6.00
khandvi | 7.50 | 7.50
jalebi | n/a | NULL
kaju katli | 12,00 | NULL
masala chai | 3.00 | 3.00
```

i expected a failed cast to skip the row. it keeps the row and the number comes back null. and 12,00 fails too, a comma isnt a decimal point to DuckDB.

that quiet null is the catch. check how many came through:

```sql
SELECT count(*) AS rows_in, count(TRY_CAST(price_text AS DECIMAL(6, 2))) AS parsed, avg(TRY_CAST(price_text AS DECIMAL(6, 2))) AS avg_price FROM price_export
```

```result
rows_in | parsed | avg_price
5 | 3 | 5.5
```

count skips nulls, so parsed is 3. 5.5 looks fine, but its the average of 3 prices and nothing warned you about the other 2. after a TRY_CAST, compare rows in with rows parsed before you trust the number.

### check yourself

1. without running it, how many rows come back, and which ones?

```sql
SELECT name FROM price_export WHERE TRY_CAST(price_text AS DECIMAL(6, 2)) > 5 ORDER BY product_id
```
<details><summary>answer</summary>

```result
name
dhokla
khandvi
```

2 rows. kaju katli costs 12 in real life, but its text is 12,00, so it casts to null and the comparison comes out [unknown](./114-three-valued-logic-true-false-and-unknown.md) (neither true nor false), and WHERE only keeps true rows. the tempting answer is 3, from reading 12,00 as twelve.

</details>

2. a value is the text '12.5'. you TRY_CAST it to INTEGER. is that null, since 12.5 isnt a whole number?

```sql
SELECT TRY_CAST('12.5' AS INTEGER) AS a, TRY_CAST('twelve' AS INTEGER) AS b
```
<details><summary>answer</summary>

```result
a | b
13 | NULL
```

not null, a is 13. DuckDB reads 12.5 as a number and rounds it, the way [132](./132-cast-changing-a-values-type.md) rounded 7.50 to 8. null means the text wouldnt convert, like twelve, or the number didnt fit the type.

</details>

---
prev: [132 CAST, changing a values type](./132-cast-changing-a-values-type.md) | next: [134 the order SQL really runs in](./134-the-order-sql-really-runs-in.md)
