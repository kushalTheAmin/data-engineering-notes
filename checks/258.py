# checks for notes/258-functional-dependency-when-one-column-decides-another.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# Jersey City is customers 1 and 3
assert q("SELECT customer_id FROM customers WHERE city = 'Jersey City' ORDER BY 1") == [(1,), (3,)]
assert q("SELECT count(*) FROM customers") == [(5,)] and q("SELECT count(DISTINCT name) FROM customers") == [(5,)]
# snack prices 6.00, 7.50, 4.50
assert q("SELECT count(DISTINCT price) FROM products WHERE category = 'snack'") == [(3,)]
assert q("SELECT count(*) FROM products WHERE category = 'drink'") == [(1,)]
# source: https://www.postgresql.org/docs/16/sql-select.html
# confirmed: ungrouped columns are allowed when functionally dependent on the grouped columns, which exists if the grouped columns are the primary key of the table containing them
