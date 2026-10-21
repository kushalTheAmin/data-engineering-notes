# 131: integer division, when 7 / 2 gives 3
builds on: [015 integer sizes, 8, 16, 32 and 64 bit numbers](./015-integer-sizes.md), [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [122 computed columns and AS](./122-computed-columns-and-as.md), [130 NULLIF and dividing by zero](./130-nullif-and-dividing-by-zero.md)
section: asking questions with SQL, part 31, ~2 min read

what is 7 / 2? Postgres says 3 and DuckDB says 3.5, same question. in the shop, order 104 has 3 dhokla to split between 2 people, so which database you ask decides if you get 1 or 1.5 each.

integer division is dividing two [integers](./015-integer-sizes.md) (whole numbers) and keeping only the whole part of the answer. python has it too, the // operator, and 3 // 2 is 1. in [130](./130-nullif-and-dividing-by-zero.md) i divided in DuckDB without thinking about this, so here is the other side of it.

the shop, the imaginary gujarati snack store these notes run on, has an order_items [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows). a slice, orders 104 and 105, with two [computed columns](./122-computed-columns-and-as.md) (calculations in SELECT):

```sql
SELECT order_id, product_id, quantity, quantity / 2 AS slash, quantity // 2 AS double_slash FROM order_items WHERE order_id IN (104, 105) ORDER BY order_id, product_id
```

```result
order_id | product_id | quantity | slash | double_slash
104 | 1 | 3 | 1.5 | 1
105 | 3 | 2 | 1.0 | 1
105 | 4 | 2 | 1.0 | 1
105 | 5 | 1 | 0.5 | 0
```

in DuckDB, / always gives a decimal answer, even for two integers, and // is the one that drops the fraction. so 1 // 2 is 0, the half a masala chai just vanishes.

i assumed every database treats / the same way, and Postgres doesnt. there, / on two integers is integer division, so it follows the DuckDB // column:

```text
-- Postgres, not DuckDB
SELECT 3 / 2;     -- 1
SELECT 3 / 2.0;   -- 1.5
```

make either side a decimal and you get the fraction back. it also cuts toward zero, so (-5) / 2 is -2, not -3.

this is a real classic bug. a rate like cancelled / placed from [130](./130-nullif-and-dividing-by-zero.md) comes out as 0 in Postgres for any day where fewer orders were cancelled than placed, and nothing errors. when i port a query between databases, this is the first division i check.

### check yourself

1. order 104 is 3 dhokla. without running it, what does this return in DuckDB?

```sql
SELECT quantity // 2 * 2 AS even_part FROM order_items WHERE order_id = 104
```
<details><summary>answer</summary>

```result
even_part
2
```

3 // 2 drops to 1, then times 2 gives 2. the tempting answer is 3, from thinking the 2s cancel out, but they cant once the fraction has been thrown away in between.

</details>

2. in Postgres, april 4 has cancelled = 1 and placed = 2 in two integer columns. what does cancelled / placed return, and what is one fix?
<details><summary>answer</summary>

0, because both sides are integers so the 0.5 is cut off. the tempting answer is 0.5. a fix is making one side a decimal, for example 1.0 * cancelled / placed.

</details>

---
prev: [130 NULLIF and dividing by zero](./130-nullif-and-dividing-by-zero.md) | next: not written yet
