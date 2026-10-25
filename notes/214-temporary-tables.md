# 214: temporary tables, a table that lives as long as your session
builds on: [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [211 a database server, Postgres where most app data lives](./211-a-database-server-postgres-where-most-app-data-lives.md), [212 connections and sessions, one conversation with the database](./212-connections-and-sessions-one-conversation-with-the-database.md), [213 CREATE TABLE, naming a table and its columns](./213-create-table-naming-a-table-and-its-columns.md)
section: changing data safely, part 7, ~2 min read

i made a scratch copy of the shop products, then SELECT * FROM products came back with 3 rows instead of 6. nothing got deleted, so what happened?

a temporary table is a scratch table that deletes itself. write TEMP between CREATE and TABLE ([213](./213-create-table-naming-a-table-and-its-columns.md), the command that makes a new table, a grid of rows) and it belongs to one [session](./212-connections-and-sessions-one-conversation-with-the-database.md) (what one open connection to the database keeps). by default it is dropped, meaning deleted, when that session ends. the shop is the imaginary gujarati snack store these notes run on, here on a [Postgres](./211-a-database-server-postgres-where-most-app-data-lives.md) server (a database program many apps connect to), with Asha and Bhavin as two apps:

```text
step  Ashas connection                       Bhavins connection
1     connect                                connect
2     CREATE TEMP TABLE cheap AS
        SELECT * FROM products
        WHERE price < 6;
3     SELECT count(*) FROM cheap;  ->  3     SELECT count(*) FROM cheap;
                                             ->  ERROR: relation "cheap" does not exist
4     disconnect
5     connect again
6     SELECT count(*) FROM cheap;
        ->  ERROR: relation "cheap" does not exist
```

count(*) counts rows: 3 is jalebi, masala chai and fafda, where [WHERE](./106-where-keeping-only-the-rows-that-match.md) price < 6 holds. relation is Postgres for table (also views and indexes). i thought a temp table was a normal table, but it acts like a python variable.

a plain CREATE TABLE products errors, the name is taken. with TEMP it doesnt, since temp tables live apart, so products now means the temp one. in DuckDB, a database inside a script:

```sql
CREATE TEMP TABLE products AS SELECT * FROM products WHERE price < 6;
-- ORDER BY sorts the rows
SELECT name, price FROM products ORDER BY price
```

```result
name | price
masala chai | 3.00
fafda | 4.50
jalebi | 5.00
```

the real table is hidden. Postgres looks in temp tables first too. the real one needs its full name: shop.products for a file shop.duckdb, memory.products if in memory, public.products in Postgres, where public is a schema (a folder of tables).

so what: behind a pooler like the one in 212, the next statement may run on another connection, where your temp table doesnt exist.

---
prev: [213 CREATE TABLE, naming a table and its columns](./213-create-table-naming-a-table-and-its-columns.md) | next: [215 NOT NULL and DEFAULT, required columns and fallback values](./215-not-null-and-default-required-columns-and-fallback-values.md)
