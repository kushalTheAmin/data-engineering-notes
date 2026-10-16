# 022: exact decimal types
builds on: [015 integer sizes, 8, 16, 32 and 64 bit numbers](./015-integer-sizes.md), [019 floating point, digits plus where the point sits](./019-floating-point.md), [020 why 0.1 + 0.2 is not exactly 0.3](./020-why-0-1-plus-0-2-is-not-0-3.md), [021 storing money as whole cents](./021-storing-money-as-whole-cents.md)
section: data at the atom level, part 22, ~2 min read

in [020](./020-why-0-1-plus-0-2-is-not-0-3.md) a check said 4 of the 6 shop products pass 0.1 + 0.2 = 0.3. what if the price column wasnt a [float](./019-floating-point.md), digits plus a sliding point, at all?

it isnt. the shop, the imaginary gujarati snack store these notes run on, declares price as DECIMAL(6, 2): an exact type that keeps decimal digits, at most 6 digits in total, 2 of them after the point. same trick as [whole cents](./021-storing-money-as-whole-cents.md), but the database moves the point for you. here is the 020 test run both ways on the shop products:

```sql
SELECT name, price, price::DOUBLE + 0.1 + 0.2 = price::DOUBLE + 0.3 AS as_double, price + 0.1 + 0.2 = price + 0.3 AS as_decimal FROM products;
```

```result
name | price | as_double | as_decimal
dhokla | 6.00 | true | true
khandvi | 7.50 | true | true
jalebi | 5.00 | true | true
kaju katli | 12.00 | false | true
masala chai | 3.00 | false | true
fafda | 4.50 | true | true
```

as_double is note 020s 4 out of 6. as_decimal is 6 out of 6. i assumed there had to be a catch, but inside, DuckDB (the database these notes use) just keeps price as a plain [integer](./015-integer-sizes.md), 600 for 6.00, and remembers the scale is 2.

the 6 is the precision and the 2 is the scale, so DECIMAL(6, 2) tops out at 9999.99 and 12345.67 is an error. extra digits on the right get rounded instead. multiplying grows the scale, and it stays exact:

```sql
SELECT price * 0.15 AS discount FROM products WHERE name = 'khandvi';
```

```result
discount
1.1250
```

that is the 112.5 cents from 021, held exactly. you still pick a rounding rule when it goes back to 2 places. Postgres calls this type NUMERIC and recommends it for money, but says its slower than integers or floats: https://www.postgresql.org/docs/current/datatype-numeric.html

### check yourself

1. someone creates a column DECIMAL(6, 2) and inserts 12345.67 for a bulk order total. what happens, and why?
<details><summary>answer</summary>

it errors. 6 digits total with 2 after the point leaves 4 before it, so the top is 9999.99, and 12345.67 needs 5. the tempting answer is that it stores the value with the extra digit, but a fixed precision is a promise, so the database refuses. widen it, say DECIMAL(8, 2).

</details>

2. what do these two products give, rounded back to 2 places? the tempting answer is to chop the extra digits, as 021 did with //.
```sql
SELECT name, (price * 0.15)::DECIMAL(6, 2) AS discount FROM products WHERE name IN ('khandvi', 'fafda');
```
<details><summary>answer</summary>

```result
name | discount
khandvi | 1.13
fafda | 0.68
```

the exact values are 1.1250 and 0.6750, and the cast rounds the tie up. chopping would give 1.12 and 0.67. which rule is right is still your business to choose, the type only does one of them for you.

</details>

---
prev: [021 storing money as whole cents](./021-storing-money-as-whole-cents.md) | next: not written yet
