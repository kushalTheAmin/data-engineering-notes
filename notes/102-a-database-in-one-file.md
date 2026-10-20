# 102: a database in one file, setting up DuckDB
builds on: [036 memory vs disk, one forgets and one remembers](./036-memory-vs-disk.md), [039 a file is a named list of bytes](./039-a-file-is-a-named-list-of-bytes.md), [086 client and server, you ask, the database answers](./086-client-and-server.md), [101 SQL, you describe the result, the database figures out how](./101-sql-you-describe-the-result.md)
section: asking questions with SQL, part 2, ~2 min read

where does a database actually live? i pictured a server humming in a back room, and with DuckDB it is one file sitting next to your script.

DuckDB is a database you install like any python library (`pip install duckdb`), and it runs inside your own program, so there is no [server](./086-client-and-server.md) to start. a connection is an open line from your program to the database. you connect to a path, and DuckDB opens that [file](./039-a-file-is-a-named-list-of-bytes.md), or creates it if it isnt there. the shop, the imaginary gujarati snack store, gets a tiny slice of customers here, just name and city:

```python
import duckdb, os

con = duckdb.connect("shop.duckdb")
con.execute("CREATE TABLE customers (name VARCHAR, city VARCHAR)")
con.execute("INSERT INTO customers VALUES ('Asha', 'Jersey City'), ('Bhavin', 'Edison')")
con.close()

print(os.path.exists("shop.duckdb"))

con = duckdb.connect("shop.duckdb")
print(con.execute("SELECT * FROM customers").fetchall())
```

```output
True
[('Asha', 'Jersey City'), ('Bhavin', 'Edison')]
```

the first connection made the file, wrote two rows and closed. in the SQL, CREATE TABLE makes an empty table (VARCHAR means text), INSERT INTO adds rows, and SELECT * reads back every column. the second connection is a brand new one, and the rows are still there, because they were saved on [disk](./036-memory-vs-disk.md) and not left in memory (the working space that forgets at power off).

the gotcha: connect with no path, or with ":memory:", and DuckDB keeps everything in memory, so it all vanishes when the program ends. also, only one running program at a time may write to a file.

i expected a sealed special thing, but it is a file like any other, and you can copy it to a friend. SQLite, another database, works the same way, a single file. the next note puts the real shop into one of these and asks it something.

---
prev: [101 SQL, you describe the result, the database figures out how](./101-sql-you-describe-the-result.md) | next: [103 your first query against the shop](./103-your-first-query-against-the-shop.md)
