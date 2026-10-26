# 218: key constraints, PRIMARY KEY and REFERENCES in CREATE TABLE
builds on: [087 primary key, one unique id per row](./087-primary-key.md), [093 foreign key, a column that points at another tables key](./093-foreign-key.md), [094 what a foreign key stops, rows pointing at nothing](./094-what-a-foreign-key-stops.md), [213 CREATE TABLE, naming a table and its columns](./213-create-table-naming-a-table-and-its-columns.md), [215 NOT NULL and DEFAULT, required columns and fallback values](./215-not-null-and-default-required-columns-and-fallback-values.md)
section: changing data safely, part 11, ~2 min read

you can name a column shipment_id all day, so what makes the database treat it like a key?

only you saying so, in [CREATE TABLE](./213-create-table-naming-a-table-and-its-columns.md) (the command that makes a table). PRIMARY KEY makes a column a [primary key](./087-primary-key.md) (unique in every row, never missing), and REFERENCES makes one a [foreign key](./093-foreign-key.md) (a pointer at another tables key). the shop, the imaginary gujarati snack store these notes run on, gets a shipments table twice, once with no rules and once with both. same three inserts into each, in DuckDB (the database these notes run on):

| insert (shipment_id, order_id) | no rules | with keys |
| --- | --- | --- |
| 1, 101 | stored | stored |
| 1, 102 (id 1 again) | stored | refused, duplicate key |
| 2, 999 (no such order) | stored | refused, key not in orders |

here is the no-rules table after all three:

```sql
CREATE TABLE loose (shipment_id INTEGER, order_id INTEGER, via VARCHAR);
INSERT INTO loose VALUES (1, 101, 'bike'), (1, 102, 'van'), (2, 999, 'van');
SELECT * FROM loose
```

```result
shipment_id | order_id | via
1 | 101 | bike
1 | 102 | van
2 | 999 | van
```

shipment 1 exists twice, and shipment 2 points at an [orphan](./094-what-a-foreign-key-stops.md) (a pointer matching no row). now the keyed version, with [NOT NULL](./215-not-null-and-default-required-columns-and-fallback-values.md) (refuse a missing value) on the pointer:

```sql
CREATE TABLE shipments (shipment_id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES orders (order_id), via VARCHAR);
INSERT INTO shipments VALUES (1, 101, 'bike')
```

```sql
-- fails on purpose
INSERT INTO shipments VALUES (2, 999, 'van')
```

i assumed a column called order_id was enough for the database to know it points at orders, but the name is only a label. nothing is checked until the rule is written down.

this bites in data warehouses (databases built for analysis). Snowflake, a popular one, accepts PRIMARY KEY and FOREIGN KEY on standard tables but its docs list them as not enforced, so there the keys are documentation and the code that loads the data has to do the checking.

### check yourself

1. the keyed shipments table holds shipment 1 for order 101. a second shipment, number 2, goes out for the same order 101. refused? what do these give (count(*) counts rows, count(DISTINCT order_id) counts the different order ids)?
```sql
CREATE TABLE ship2 (shipment_id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES orders (order_id));
INSERT INTO ship2 VALUES (1, 101), (2, 101);
SELECT count(*) AS shipments, count(DISTINCT order_id) AS orders FROM ship2
```
<details><summary>answer</summary>

```result
shipments | orders
2 | 1
```
accepted. only shipment_id has to be unique, order_id is a foreign key and may repeat. the tempting answer is refused, because 101 is already there.

</details>

2. this version forgot NOT NULL on the pointer. shipment 3 goes in with order_id NULL. refused? (count(order_id) counts only the rows that have a value)
```sql
CREATE TABLE ship3 (shipment_id INTEGER PRIMARY KEY, order_id INTEGER REFERENCES orders (order_id));
INSERT INTO ship3 VALUES (3, NULL);
SELECT count(*) AS rows_now, count(order_id) AS pointing FROM ship3
```
<details><summary>answer</summary>

```result
rows_now | pointing
1 | 0
```
accepted. a NULL points at nothing, so there is nothing to match, and Postgres docs say the same. the tempting answer is refused as an orphan.

</details>

---
prev: [217 CHECK, a rule every value must pass](./217-check-a-rule-every-value-must-pass.md) | next: [219 sequences, where made up ids come from](./219-sequences-where-made-up-ids-come-from.md)
