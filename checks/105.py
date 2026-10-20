# checks for notes/105-select-star-every-column.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
import duckdb
con = shop()
cols = [r[0] for r in con.execute("DESCRIBE products").fetchall()]
assert cols == ["product_id", "name", "category", "price"] and len(cols) == 4
# star is the same as naming every column in table order
assert con.execute("SELECT * FROM products").fetchall() == con.execute("SELECT product_id, name, category, price FROM products").fetchall()
assert con.execute("SELECT name, category FROM products WHERE product_id = 1").fetchone() == ("dhokla", "snack")
# the label code: index 2 is the third item
c = duckdb.connect()
c.execute("CREATE TABLE products (product_id INTEGER, name VARCHAR, category VARCHAR, price DECIMAL(6, 2))")
c.execute("INSERT INTO products VALUES (1, 'dhokla', 'snack', 6.00)")
row = c.execute("SELECT * FROM products").fetchone()
assert isinstance(row, tuple) and row[2] == "snack"
c.execute("ALTER TABLE products DROP COLUMN category")
row = c.execute("SELECT * FROM products").fetchone()
assert str(row[2]) == "6.00" and len(row) == 3
try:
    c.execute("SELECT name, category FROM products")
    raise SystemExit("should fail")
except duckdb.BinderException:
    pass
# source: https://duckdb.org/docs/current/sql/statements/alter_table.html
# confirmed: ALTER TABLE ... DROP COLUMN removes a column from a table
# source: https://duckdb.org/docs/current/sql/expressions/star.html
# confirmed: "The * expression can be used in a SELECT statement to select all columns that are projected in the FROM clause."
# source: https://www.postgresql.org/docs/current/ddl-basics.html
# confirmed: "The number and order of the columns is fixed, and each column has a name." (the order itself is asserted above)
# source: https://en.wikipedia.org/wiki/Dhokla
# confirmed: "a savoury sponge dish" made from a fermented batter that is steamed to a cake-like consistency
print("105 ok")
