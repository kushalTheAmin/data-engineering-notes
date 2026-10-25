# 215: NOT NULL and DEFAULT, required columns and fallback values
builds on: [031 null, a marker meaning there is no value](./031-null.md), [032 null is not zero or empty text](./032-null-is-not-zero-or-empty-text.md), [087 primary key](./087-primary-key.md), [116 COALESCE, a fallback when a value is null](./116-coalesce-a-fallback-when-a-value-is-null.md), [213 CREATE TABLE, naming a table and its columns](./213-create-table-naming-a-table-and-its-columns.md)
section: changing data safely, part 8, ~2 min read

Esha has no city in the shop customers table, but no customer anywhere has no name. same table, so who decided that?

NOT NULL is a rule on a column: the database refuses any row where that column is [NULL](./031-null.md) (no value). DEFAULT is the value it fills in when an insert leaves the column out. you write both inside [CREATE TABLE](./213-create-table-naming-a-table-and-its-columns.md) (the command that makes a table), and the [primary key](./087-primary-key.md) already banned NULL this way. the shop, the imaginary gujarati snack store these notes run on, gets a cart. INSERT INTO adds a row (a later note covers it). this runs in DuckDB:

```sql
CREATE TABLE cart (customer_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL DEFAULT 1);
INSERT INTO cart (customer_id, product_id) VALUES (1, 1);
INSERT INTO cart VALUES (2, 3, 4);
SELECT * FROM cart
```

```result
customer_id | product_id | quantity
1 | 1 | 1
2 | 3 | 4
```

the first insert named two columns, so quantity got its default, 1. now two that break the rules:

```sql
-- fails on purpose
INSERT INTO cart (customer_id, product_id) VALUES (NULL, 3)
```

```sql
-- fails on purpose
INSERT INTO cart VALUES (3, 2, NULL)
```

both fail with a NOT NULL error. the second is the one i didnt expect: quantity has a default of 1, but a default only fills a column you leave out. typing NULL is a value you chose, so the rule refuses it.

unlike [COALESCE](./116-coalesce-a-fallback-when-a-value-is-null.md) (first value that is not null), which patches output when you read, DEFAULT stores the fallback when you write. the rule lives in the database, so a script that skips your react form or .NET validation still gets refused.

### check yourself

1. a table has `status VARCHAR DEFAULT 'packed'` and no NOT NULL. parcel 1 is inserted with status written as NULL, parcel 2 leaves status out. what does each row hold?
```sql
CREATE TABLE parcel (parcel_id INTEGER, status VARCHAR DEFAULT 'packed');
INSERT INTO parcel VALUES (1, NULL);
INSERT INTO parcel (parcel_id) VALUES (2);
SELECT parcel_id, status FROM parcel ORDER BY parcel_id
```
<details><summary>answer</summary>


```result
parcel_id | status
1 | NULL
2 | packed
```
parcel 1 keeps NULL, parcel 2 gets packed. the default only fires for a column left out, and with no NOT NULL the typed NULL is accepted. the tempting answer is packed for both.

</details>

2. say the shop city column were `city VARCHAR NOT NULL DEFAULT 'unknown'` and Esha is inserted with no city. how many rows does WHERE city IS NULL find?
```sql
CREATE TABLE people (name VARCHAR NOT NULL, city VARCHAR NOT NULL DEFAULT 'unknown');
INSERT INTO people (name) VALUES ('Esha');
SELECT count(*) AS nulls FROM people WHERE city IS NULL
```
<details><summary>answer</summary>


```result
nulls
0
```
Esha is stored with the text unknown, a [placeholder value](./032-null-is-not-zero-or-empty-text.md) (a made up value standing in for missing), so no NULL exists. the tempting answer is 1, but a default fills the cell, it doesnt leave it empty.

</details>

---
prev: [214 temporary tables, a table that lives as long as your session](./214-temporary-tables.md) | next: not written yet
