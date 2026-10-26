# 224: upsert, insert or update in one statement
builds on: [220 INSERT, adding rows and matching values to columns](./220-insert-adding-rows-and-matching-values-to-columns.md), [222 UPDATE, changing rows and why the WHERE matters](./222-update-changing-rows-and-why-the-where-matters.md), [218 key constraints, PRIMARY KEY and REFERENCES in CREATE TABLE](./218-key-constraints-primary-key-and-references-in-create-table.md), [221 INSERT from a SELECT, copying rows from a query](./221-insert-from-a-select-copying-rows-from-a-query.md)
section: changing data safely, part 17, ~2 min read

a price list lands: jalebi is now 5.50, and imarti (a swirly fried sweet) is brand new. INSERT would fail on jalebi and UPDATE would do nothing for imarti, so which do you run?

neither. an upsert is an [INSERT](./220-insert-adding-rows-and-matching-values-to-columns.md) (adds rows) that updates the existing row instead when the key is already there. the shop, the imaginary gujarati snack store these notes run on, gets a menu table whose name is a [PRIMARY KEY](./218-key-constraints-primary-key-and-references-in-create-table.md) (no value may repeat). in DuckDB, where ORDER BY sorts the rows:

| incoming | name already there? | what happens |
| --- | --- | --- |
| jalebi, 5.50 | yes | that row is updated |
| imarti, 6.00 | no | a new row is added |

```sql
CREATE TABLE menu (name VARCHAR PRIMARY KEY, price DECIMAL(6, 2));
INSERT INTO menu SELECT name, price FROM products
```

```sql
-- fails on purpose
INSERT INTO menu VALUES ('jalebi', 5.50)
```

```sql
INSERT INTO menu VALUES ('jalebi', 5.50), ('imarti', 6.00)
ON CONFLICT (name) DO UPDATE SET price = EXCLUDED.price;
SELECT * FROM menu ORDER BY name
```

```result
name | price
dhokla | 6.00
fafda | 4.50
imarti | 6.00
jalebi | 5.50
kaju katli | 12.00
khandvi | 7.50
masala chai | 3.00
```

ON CONFLICT (name) says which key to watch. DO UPDATE SET is an [UPDATE](./222-update-changing-rows-and-why-the-where-matters.md) on the row that collided, and EXCLUDED is the row i tried to insert, so EXCLUDED.price is 5.50. DO NOTHING instead just skips the repeat.

i expected a python style check, is it there, then one branch or the other, but the database does both in one statement. run it twice and you get the same 7 rows, where the copy in [221](./221-insert-from-a-select-copying-rows-from-a-query.md) doubled.

so what: loading jobs retry, and an upsert makes a retry harmless. Postgres docs say ON CONFLICT DO UPDATE gives one of insert or update even with many writers at once. it only works because the key exists, so no key, no upsert.

### check yourself

1. a typo: the supplier sends dhokla at 6.50 and "chai", but the shop calls it masala chai. count(*) counts rows, so how many does menu2 have after this?

```sql
CREATE TABLE menu2 (name VARCHAR PRIMARY KEY, price DECIMAL(6, 2));
INSERT INTO menu2 SELECT name, price FROM products;
INSERT INTO menu2 VALUES ('dhokla', 6.50), ('chai', 3.00)
ON CONFLICT (name) DO UPDATE SET price = EXCLUDED.price;
SELECT count(*) AS rows_now FROM menu2
```

<details><summary>answer</summary>

```result
rows_now
7
```

dhokla matches and is updated, but "chai" is not "masala chai", so it is a new row. the tempting answer is 6, assuming the database knows what you meant. the key only matches exact values.

</details>

2. the same upsert is aimed at a copy made without any key. update, add a second jalebi, or error?

<details><summary>answer</summary>

```sql
-- fails on purpose
CREATE TABLE loose AS SELECT name, price FROM products;
INSERT INTO loose VALUES ('jalebi', 5.50)
ON CONFLICT (name) DO UPDATE SET price = EXCLUDED.price
```

it errors, since nothing in loose can say a conflict happened. the tempting answer is a second jalebi, which is what a plain INSERT would do.

</details>

---
prev: [223 DELETE, removing rows and what still points at them](./223-delete-removing-rows-and-what-still-points-at-them.md) | next: not written yet
