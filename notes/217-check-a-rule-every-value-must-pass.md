# 217: CHECK, a rule every value must pass
builds on: [031 null, a marker meaning there is no value](./031-null.md), [213 CREATE TABLE, naming a table and its columns](./213-create-table-naming-a-table-and-its-columns.md), [215 NOT NULL and DEFAULT, required columns and fallback values](./215-not-null-and-default-required-columns-and-fallback-values.md), [216 UNIQUE, no two rows may share a value](./216-unique-no-two-rows-may-share-a-value.md)
section: changing data safely, part 10, ~2 min read

the shop products table says price can never be missing. but can a price of -7.50 get in? nothing so far says no.

CHECK is a rule, usually on one column, with a true or false test inside it, and the database refuses any row where the test comes out false. you write it in [CREATE TABLE](./213-create-table-naming-a-table-and-its-columns.md) (the command that makes a table), next to [NOT NULL](./215-not-null-and-default-required-columns-and-fallback-values.md) (refuse a missing value) and [UNIQUE](./216-unique-no-two-rows-may-share-a-value.md) (refuse a repeated value). the shop, the imaginary gujarati snack store these notes run on, gets a price list with CHECK (price > 0). here is what happens to five prices:

| price tried | test price > 0 | row |
| --- | --- | --- |
| 6.00 | true | stored |
| 5.00 | true | stored |
| 0 | false | refused |
| -7.50 | false | refused |
| NULL | unknown | stored |

the same thing in DuckDB, the database these notes run on (no NOT NULL on price, on purpose):

```sql
CREATE TABLE price_list (name VARCHAR NOT NULL, price DECIMAL(6, 2) CHECK (price > 0));
INSERT INTO price_list VALUES ('dhokla', 6.00), ('jalebi', 5.00), ('fafda', NULL);
SELECT * FROM price_list
```

```result
name | price
dhokla | 6.00
jalebi | 5.00
fafda | NULL
```

```sql
-- fails on purpose
INSERT INTO price_list VALUES ('khandvi', -7.50)
```

that one dies with CHECK constraint failed, and 0 would die too, because the test says above zero, not zero or more.

the bottom row is the part i didnt expect. i kept reading CHECK as reject anything bad, but a test on a [NULL](./031-null.md) (no value) isnt false, its unknown, and the database only refuses a false. Postgres, a popular server database, documents the same. so a price that must exist and be positive needs both rules: NOT NULL CHECK (price > 0).

your app code probably checks prices too, but a script that skips it still hits this rule.

### check yourself

1. a stock table has `quantity INTEGER CHECK (quantity >= 0)`. you insert dhokla with 0 and jalebi with NULL. does either get refused, and what do count(*) and count(quantity) give (the second counts only rows that have a value)?
```sql
CREATE TABLE stock (product VARCHAR, quantity INTEGER CHECK (quantity >= 0));
INSERT INTO stock VALUES ('dhokla', 0), ('jalebi', NULL);
SELECT count(*) AS rows_now, count(quantity) AS counted FROM stock
```
<details><summary>answer</summary>

```result
rows_now | counted
2 | 1
```
neither is refused. 0 passes because the test says zero or more, and NULL gives unknown. the tempting answer is that NULL gets refused, or that 0 does.

</details>

2. say the orders table had been made with CHECK (status IN ('pending', 'delivered')). the 7 orders hold 5 delivered, 1 pending and 1 cancelled. which would the rule have refused?
```sql
SELECT order_id, status FROM orders WHERE NOT (status IN ('pending', 'delivered'))
```
<details><summary>answer</summary>

```result
order_id | status
104 | cancelled
```
only order 104. the rule is a claim about every row, and cancelled is a real status the list forgot. the tempting answer is none, because pending and delivered are the common ones.

</details>

---
prev: [216 UNIQUE, no two rows may share a value](./216-unique-no-two-rows-may-share-a-value.md) | next: not written yet
