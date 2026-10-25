# 213: CREATE TABLE, naming a table and its columns
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [080 every column holds one type](./080-every-column-holds-one-type.md), [102 a database in one file, setting up DuckDB](./102-a-database-in-one-file.md), [211 a database server, Postgres where most app data lives](./211-a-database-server-postgres-where-most-app-data-lives.md)
section: changing data safely, part 6, ~2 min read

every table i have queried so far was already there. what does it take to make a new one?

CREATE TABLE is the SQL (the language for asking a database) command that makes a new, empty [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows with the same columns). you give it a name, then each column with its [type](./080-every-column-holds-one-type.md) (the kind of value allowed). the shop, the imaginary gujarati snack store these notes run on, wants a wishlist: who saved which product, and when. INTEGER is a whole number, VARCHAR text, DATE a calendar day. this runs in [DuckDB](./102-a-database-in-one-file.md) (a database inside your script), and [Postgres](./211-a-database-server-postgres-where-most-app-data-lives.md) accepts this CREATE, whose docs say it makes "a new, initially empty table".

the second line lists the columns the database stored (DuckDB output; Postgres writes types in lowercase).

```sql
CREATE TABLE wishlist (customer_id INTEGER, product_id INTEGER, added_on DATE);
SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'wishlist' ORDER BY ordinal_position
```

```result
column_name | data_type
customer_id | INTEGER
product_id | INTEGER
added_on | DATE
```

the table exists with zero rows. run the CREATE again and it errors, the name is taken. IF NOT EXISTS skips instead, and that surprised me. the shop already has products, so i tried creating it again with one different column:

```sql
CREATE TABLE IF NOT EXISTS products (note VARCHAR);
SELECT column_name FROM information_schema.columns WHERE table_name = 'products' ORDER BY ordinal_position
```

```result
column_name
product_id
name
category
price
```

no error here (Postgres prints a notice), and no note column. the Postgres docs say there is no guarantee the existing table is anything like the one you asked for. i assumed it meant make sure this exists as written, but it only checks the name.

so a column added later to a table-building script never reaches a table that already exists. changing one after the fact is its own command, in a later note.

---
prev: [212 connections and sessions, one conversation with the database](./212-connections-and-sessions-one-conversation-with-the-database.md) | next: [214 temporary tables, a table that lives as long as your session](./214-temporary-tables.md)
