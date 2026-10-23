# checks for notes/181-views-a-saved-query-with-a-name.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT count(*) FROM orders") == [(7,)]
assert q("SELECT count(*) FROM orders WHERE status = 'delivered'") == [(5,)]
con.execute("CREATE VIEW delivered_orders AS SELECT * FROM orders WHERE status = 'delivered'")
assert q("SELECT count(*) FROM delivered_orders") == [(5,)]
assert q("SELECT customer_id, status FROM orders WHERE order_id = 106") == [(1, 'pending')]
con.execute("UPDATE orders SET status = 'delivered' WHERE order_id = 106")
assert q("SELECT count(*) FROM delivered_orders") == [(6,)]
# check yourself 1
con.execute("UPDATE orders SET status = 'cancelled' WHERE order_id = 107")
assert q("SELECT count(*) FROM delivered_orders") == [(5,)]
# check yourself 2
con.execute("CREATE VIEW cheap AS SELECT * FROM products WHERE price < 6")
assert q("SELECT count(*) FROM cheap") == [(3,)]
con.execute("UPDATE products SET price = 5.00 WHERE name = 'dhokla'")
assert q("SELECT count(*) FROM cheap") == [(4,)]
# source: https://www.postgresql.org/docs/current/sql-createview.html
# confirmed: the view is not physically materialized, the query is run every time the view is referenced
# source: https://www.postgresql.org/docs/current/rules-materializedviews.html
# confirmed: materialized views persist the results in a table-like form, so Postgres has both kinds
# source: https://www.postgresql.org/docs/current/sql-dropview.html
# confirmed: "DROP VIEW drops an existing view."
# source: https://www.postgresql.org/docs/current/sql-update.html
# confirmed: "UPDATE changes the values of the specified columns in all rows that satisfy the condition."
