# 101: SQL, you describe the result, the database figures out how
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [082 a database, a program that guards your data](./082-a-database-guards-the-data.md), [086 client and server, you ask, the database answers](./086-client-and-server.md), [100 capstone, the whole shop as four connected tables](./100-capstone-the-whole-shop-as-four-connected-tables.md)
section: asking questions with SQL, part 1, ~2 min read

which customers live in Jersey City? in python you would write a loop, and i kept looking for the loop in the SQL version, and there isnt one.

SQL is the language you send to a [database](./082-a-database-guards-the-data.md) to ask for rows, and one request is called a query. you describe the result you want, and the database works out the steps. the shop, the imaginary gujarati snack store, ended [the last section](./100-capstone-the-whole-shop-as-four-connected-tables.md) as four tables, and this is the first question put to one of them:

```sql
SELECT name FROM customers WHERE city = 'Jersey City'
```

```result
name
Asha
Chirag
```

that is the whole request: the column name (a named field every row has), from the customers [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows), only where the city matches. now the same answer the way you already write code, with the steps spelled out:

```python
customers = [
    {"name": "Asha", "city": "Jersey City"},
    {"name": "Bhavin", "city": "Edison"},
    {"name": "Chirag", "city": "Jersey City"},
    {"name": "Disha", "city": "Hoboken"},
    {"name": "Esha", "city": None},
]
found = []
for row in customers:
    if row["city"] == "Jersey City":
        found.append(row["name"])
print(found)
```

```output
['Asha', 'Chirag']
```

the python says how: top down, check each row, keep a list. the SQL never says where to start. because you only described the result, the database is free to use a shortcut on a bigger table, like a lookup it keeps on the side, as long as the same rows come out (their order isnt promised). on these 5 rows it probably just reads them all.

SQL also changes rows, but asking comes first. you send the query as text from a [client](./086-client-and-server.md) (the asking side) and rows come back. Postgres, MySQL, SQLite and DuckDB are all databases that take SQL, each with its own dialect in places. the notes use DuckDB, which runs inside your own program, no separate server.

### check yourself

1. a teammate says the query above reads the customers top to bottom, like the loop. can you tell that from the query alone?
<details><summary>answer</summary>

no. the query only states the result, so the database picks the steps, and on a bigger table might skip rows. only the result is promised. the tempting answer is yes, from reading it like the loop.

</details>

2. Esha has no city, a missing value that SQL calls NULL, like None in python. predict this:

```sql
SELECT city FROM customers WHERE name = 'Esha'
```
<details><summary>answer</summary>

```result
city
NULL
```

one row, holding a NULL. the row exists, only its city is missing. the tempting answer is no rows, from reading a missing city as nothing to return.

</details>

---
prev: [100 capstone, the whole shop as four connected tables](./100-capstone-the-whole-shop-as-four-connected-tables.md) | next: [102 a database in one file, setting up DuckDB](./102-a-database-in-one-file.md)
