# 105: SELECT star, every column, and why you rarely want it
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [103 your first query against the shop](./103-your-first-query-against-the-shop.md), [104 SELECT and FROM, picking columns](./104-select-and-from-picking-columns.md)
section: asking questions with SQL, part 5, ~2 min read

some code built a label for each product, and it printed "dhokla (snack)" one day and "dhokla (6.00)" the next. nobody touched the code, and the only suspect is one star.

SELECT * means every column of the table, in the order the table has them. it is a shortcut for the column list [104](./104-select-and-from-picking-columns.md) had you name. the shop, the imaginary gujarati snack store these notes run on, has a products [table](./079-a-table-rows-are-records-columns-are-fields.md) with product_id, name, category and price, so right now SELECT * FROM products is the same as naming all four. dhokla is a steamed savory cake. below is a one-row stand-in copy of products (the real one is left alone), and label code run before and after someone drops the category column with ALTER TABLE:

```python
import duckdb

con = duckdb.connect()
con.execute("CREATE TABLE products (product_id INTEGER, name VARCHAR, category VARCHAR, price DECIMAL(6, 2))")
con.execute("INSERT INTO products VALUES (1, 'dhokla', 'snack', 6.00)")

def label(row):
    return row[1] + " (" + str(row[2]) + ")"  # name, then category

print(label(con.execute("SELECT * FROM products").fetchone()))
con.execute("ALTER TABLE products DROP COLUMN category")
print(label(con.execute("SELECT * FROM products").fetchone()))
try:
    con.execute("SELECT name, category FROM products")
except duckdb.BinderException:
    print("error: no column category")
```

```output
dhokla (snack)
dhokla (6.00)
error: no column category
```

fetchone hands back one row as a tuple (a fixed list), and row[2] means the third item (python counts from 0), whatever it is today. after the drop the third item is the price, so the code keeps running and quietly says the wrong thing, no error. naming the columns gives an error instead, which at least makes someone look.

i expected the broken version to be the one that crashes, and it was the one that looked fine.

so star is for you, peeking at a table you just met. anything you save and run again, like a script, should list its columns, which also means it only carries what it needs.

---
prev: [104 SELECT and FROM, picking columns](./104-select-and-from-picking-columns.md) | next: not written yet
