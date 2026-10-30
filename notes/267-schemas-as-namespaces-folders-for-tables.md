# 267: schemas as namespaces, folders for tables
builds on: [214 temporary tables, a table that lives as long as your session](./214-temporary-tables.md), [213 CREATE TABLE, naming a table and its columns](./213-create-table-naming-a-table-and-its-columns.md), [075 schema, the agreement about shape](./075-schema.md), [182 UNION and UNION ALL, stacking two queries](./182-union-and-union-all.md), [138 count star vs count of a column](./138-count-star-vs-count-of-a-column.md), [102 a database in one file, setting up DuckDB](./102-a-database-in-one-file.md), [211 a database server, Postgres where most app data lives](./211-a-database-server-postgres-where-most-app-data-lives.md)
section: designing tables, part 14, ~2 min read

the same query, SELECT count(*) FROM orders, can say 7 for one person and 2 for another, in one database. nobody touched a row, so what differs?

a schema here is a named folder of tables (grids of rows) inside a database, so a full name is schema.table and two tables can both be called orders in different folders. new meaning: in [075](./075-schema.md) a schema was an agreement on which fields a record must have, and [214](./214-temporary-tables.md) only mentioned public in passing.

the shop, the imaginary gujarati snack store these notes run on, keeps its tables in a folder called main (in [Postgres](./211-a-database-server-postgres-where-most-app-data-lives.md) it is public). i add an archive folder with the first two orders, using [CREATE TABLE](./213-create-table-naming-a-table-and-its-columns.md). this is [DuckDB](./102-a-database-in-one-file.md), and [count(*)](./138-count-star-vs-count-of-a-column.md) counts rows, and [UNION ALL](./182-union-and-union-all.md) stacks results:

```sql
CREATE SCHEMA archive;
CREATE TABLE archive.orders AS SELECT * FROM orders WHERE order_id < 103;
SELECT 'main.orders' AS full_name, count(*) AS n FROM main.orders
UNION ALL SELECT 'archive.orders', count(*) FROM archive.orders
UNION ALL SELECT 'orders', count(*) FROM orders
```

```result
full_name | n
main.orders | 7
archive.orders | 2
orders | 7
```

the bare name (orders, no folder) went to main, the default current folder. USE moves it:

```sql
USE archive;
SELECT count(*) AS n FROM orders
```

```result
n
2
```

same words, different table, no error. Postgres has no USE, it sets a search path, a list of folders checked in order, first match wins. its default is "$user", public.

the Postgres docs give the reasons: many users sharing one database, grouping tables, and apps keeping their names out of yours. a folder is no wall though, you can reach any schema you have permission for.

i assumed a table name was just the name of the table, but its only a name inside a folder, so a bare orders depends on where you are standing.

---
prev: [266 soft deletes, marking a row gone instead of removing it](./266-soft-deletes-marking-a-row-gone-instead-of-removing-it.md) | next: [268 capstone, modeling product reviews for the shop](./268-capstone-modeling-product-reviews-for-the-shop.md)
