# 103: your first query against the shop
builds on: [022 exact decimal types](./022-exact-decimal-types.md), [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [101 SQL, you describe the result, the database figures out how](./101-sql-you-describe-the-result.md), [102 a database in one file, setting up DuckDB](./102-a-database-in-one-file.md)
section: asking questions with SQL, part 3, ~2 min read

a database file with nothing in it is a sad thing, so how does the shop get inside? it turned out to be one line of python, and then you can ask it something.

the shop, the imaginary gujarati snack store these notes run on, lives in data/shop.sql, a plain text file of [SQL](./101-sql-you-describe-the-result.md) (the language databases take) that builds its tables and fills them. you read that text and hand it to a [DuckDB](./102-a-database-in-one-file.md) connection (an open line from your program to the database):

```python
import duckdb

con = duckdb.connect("shop.duckdb")
con.execute(open("shop.sql").read())
```

now the first [query](./101-sql-you-describe-the-result.md) (one request naming the result you want), against the products [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows):

```sql
SELECT name, price FROM products
```

```result
name | price
dhokla | 6.00
khandvi | 7.50
jalebi | 5.00
kaju katli | 12.00
masala chai | 3.00
fafda | 4.50
```

six rows, one per product, two columns. dhokla is a steamed savory cake, khandvi a rolled gram flour snack, and fafda a crunchy chickpea strip. in python, `con.execute(...).fetchall()` hands these back as a list of tuples, and the price arrives as `Decimal('6.00')`, not 6.0, because the column is an [exact decimal](./022-exact-decimal-types.md) (digits kept exactly, no float rounding).

the gotcha: run that load line a second time on the same file and it errors with "Table customers already exists", because the first run saved everything. load once, after that just connect.

a database dump from Postgres works the same way by default: a text file of SQL commands that rebuilds the database when you feed it back in. i expected loading data to need some special import tool, and it is just running a text file.

---
prev: [102 a database in one file, setting up DuckDB](./102-a-database-in-one-file.md) | next: [104 SELECT and FROM, picking columns](./104-select-and-from-picking-columns.md)
