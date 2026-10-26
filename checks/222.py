# checks for notes/222-update-changing-rows-and-why-the-where-matters.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
from decimal import Decimal
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT count(*) FROM orders") == [(7,)]
con.execute("UPDATE orders SET status = 'cancelled' WHERE order_id = 106")
assert q("SELECT order_id, status FROM orders WHERE order_id >= 105 ORDER BY order_id") == [(105, "delivered"), (106, "cancelled"), (107, "delivered")]
con.execute("UPDATE orders SET status = 'cancelled'")
assert q("SELECT count(*) FROM orders WHERE status = 'cancelled'") == [(7,)]
# a WHERE that matches nothing changes 0 rows and raises no error
assert q("UPDATE orders SET status = 'x' WHERE order_id = 160") == [(0,)]
# question 1: price + 1 twice adds 2
con = shop()
for _ in range(2):
    con.execute("UPDATE products SET price = price + 1 WHERE category = 'sweet'")
assert q("SELECT name, price FROM products WHERE category = 'sweet' ORDER BY product_id") == [("jalebi", Decimal("7.00")), ("kaju katli", Decimal("14.00"))]
# question 2: second run changes 0 rows
con = shop()
assert q("SELECT count(*) FROM products WHERE category = 'sweet'") == [(2,)]
assert q("UPDATE products SET category = 'sweet' WHERE category = 'drink'") == [(1,)]
assert q("UPDATE products SET category = 'sweet' WHERE category = 'drink'") == [(0,)]
assert q("SELECT count(*) FROM products WHERE category = 'sweet'") == [(3,)]
# source: https://www.postgresql.org/docs/current/sql-update.html
#   confirmed (opened this run): "If count is 0, no rows were updated by the query (this is not considered an error)"; "The expression can use the old values of this and other columns in the table."
# source: https://dev.mysql.com/doc/refman/8.4/en/mysql-command-options.html
#   confirmed (opened this run): --safe-updates (also --i-am-a-dummy): UPDATE and DELETE statements that do not use a key in the WHERE clause or a LIMIT clause produce an error
# the note says the option refuses an UPDATE unless the WHERE uses a key or there is a LIMIT: matches the quote above
