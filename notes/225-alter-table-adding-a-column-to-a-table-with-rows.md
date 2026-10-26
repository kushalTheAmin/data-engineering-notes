# 225: ALTER TABLE, adding a column to a table that already has rows
builds on: [213 CREATE TABLE, naming a table and its columns](./213-create-table-naming-a-table-and-its-columns.md), [215 NOT NULL and DEFAULT, required columns and fallback values](./215-not-null-and-default-required-columns-and-fallback-values.md), [031 null, a marker meaning there is no value](./031-null.md)
section: changing data safely, part 18, ~2 min read

the shop wants a vegan flag on its menu, but the table already has rows. what do you think those old rows hold in a column that didnt exist when they were written?

ALTER TABLE ... ADD COLUMN adds a new column to a table that already exists, keeping every row. the shop, the imaginary gujarati snack store these notes run on, gets a menu copied from the three products under 6 (a slice: fafda, jalebi, masala chai). this runs in DuckDB, and Postgres takes the same ADD COLUMN.

```sql
CREATE TABLE menu AS SELECT name, price FROM products WHERE price < 6;
ALTER TABLE menu ADD COLUMN vegan BOOLEAN;
SELECT * FROM menu ORDER BY name
```

```result
name | price | vegan
fafda | 4.50 | NULL
jalebi | 5.00 | NULL
masala chai | 3.00 | NULL
```

every old row got [NULL](./031-null.md) (no value). the database cant guess, so it says nothing. add a [DEFAULT](./215-not-null-and-default-required-columns-and-fallback-values.md) (the fallback value) and the old rows get it too:

```sql
ALTER TABLE menu ADD COLUMN in_stock BOOLEAN DEFAULT true;
SELECT * FROM menu ORDER BY name
```

```result
name | price | vegan | in_stock
fafda | 4.50 | NULL | true
jalebi | 5.00 | NULL | true
masala chai | 3.00 | NULL | true
```

in 215 a default only filled a column an insert left out. here it also fills the rows already sitting there. and the name must be new:

```sql
-- fails on purpose
ALTER TABLE menu ADD COLUMN vegan VARCHAR
```

that is the gap i left in [213](./213-create-table-naming-a-table-and-its-columns.md): IF NOT EXISTS on a CREATE never adds a column, ALTER does.

i assumed every old row would have to be rewritten before the column could exist. in Postgres a fixed default is kept once in the metadata (the notes a table keeps about itself), and the docs say the ALTER is very fast even on large tables. a default that changes per row, like clock_timestamp(), does rewrite the whole table.

---
prev: [224 upsert, insert or update in one statement](./224-upsert-insert-or-update-in-one-statement.md) | next: [226 DROP and TRUNCATE, emptying a table vs removing it](./226-drop-and-truncate-emptying-a-table-vs-removing-it.md)
