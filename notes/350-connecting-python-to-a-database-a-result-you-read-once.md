# 350: connecting python to a database, a result you read once
builds on: [349 merging dataframes, joins again](./349-merging-dataframes-joins-again.md), [345 a dataframe, a table in memory](./345-a-dataframe-a-table-in-memory.md), [340 reading a csv in python, row by row](./340-reading-a-csv-in-python-row-by-row.md), [103 your first query against the shop](./103-your-first-query-against-the-shop.md), [102 a database in one file, setting up DuckDB](./102-a-database-in-one-file.md), [031 null, a marker for a missing value](./031-null.md)
section: python for data work, part 26, ~2 min read

i called fetchall twice on the same query and the second call handed me an empty list. no error, nothing.

connecting python to a database is connect, execute, fetch. [102](./102-a-database-in-one-file.md) did the first two with [DuckDB](./102-a-database-in-one-file.md) (a database that runs inside your program), and fetch is how rows come out into python. here is a slice of 3 customers from the shop, the imaginary gujarati snack store these notes run on:

```python
import duckdb

con = duckdb.connect()
con.execute("CREATE TABLE customers (name VARCHAR, city VARCHAR)")
con.execute("INSERT INTO customers VALUES ('Asha', 'Jersey City'), ('Bhavin', 'Edison'), ('Esha', NULL)")

res = con.execute("SELECT name, city FROM customers ORDER BY name")
print(res.fetchone())
print(res.fetchall())
print(res.fetchall())
print(con.execute("SELECT name, city FROM customers ORDER BY name").df())
```

```output
('Asha', 'Jersey City')
[('Bhavin', 'Edison'), ('Esha', None)]
[]
     name         city
0    Asha  Jersey City
1  Bhavin       Edison
2    Esha          NaN
```

fetchone takes the next unread row, fetchall takes every row not yet read. so the first call took Asha, the second took the other two, and the third found nothing left. like the csv reader in [340](./340-reading-a-csv-in-python-row-by-row.md), the result only remembers how far you have read.

each row is a tuple, a fixed list of values, so row[1] is the city, and [103](./103-your-first-query-against-the-shop.md) showed rows coming back as tuples. Eshas missing city is None, python for [NULL](./031-null.md). asking for a [dataframe](./345-a-dataframe-a-table-in-memory.md) with .df() gives column names instead, and Eshas city turns into NaN (not a number, how pandas marks a missing value, as in [349](./349-merging-dataframes-joins-again.md)).

what got me is that an empty list looks exactly like a query that matched nothing. a helper that fetches once to log a count and again to build the report quietly reports zero.

python has a standard way for code to talk to databases, written up as PEP 249, and it says fetchall returns the remaining rows. sqlite3, built into python, behaves the same.

---
prev: [349 merging dataframes, joins again](./349-merging-dataframes-joins-again.md) | next: not written yet
