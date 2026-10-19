# checks for notes/097-junction-tables.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
assert con.execute("SELECT order_id, product_id, quantity FROM order_items WHERE product_id = 1 OR order_id = 101 ORDER BY order_id, product_id").fetchall() == [(101, 1, 2), (101, 5, 2), (104, 1, 3), (107, 1, 1)]
assert con.execute("SELECT name FROM products WHERE product_id = 1").fetchone()[0] == "dhokla"
assert con.execute("SELECT name FROM products WHERE product_id = 4").fetchone()[0] == "kaju katli"
assert con.execute("SELECT name FROM products WHERE product_id = 2").fetchone()[0] == "khandvi"
assert con.execute("SELECT count(*) FROM order_items WHERE product_id = 1").fetchone()[0] == 3
assert con.execute("SELECT count(*) FROM order_items WHERE order_id = 101").fetchone()[0] == 2
assert con.execute("SELECT count(*) FROM order_items WHERE order_id = 106").fetchone()[0] == 1
assert con.execute("SELECT product_id FROM order_items WHERE order_id = 106").fetchall() == [(2,)]
con.execute("INSERT INTO order_items VALUES (106, 4, 2)")
assert con.execute("SELECT count(*) FROM order_items WHERE order_id = 106").fetchone()[0] == 2
assert con.execute("SELECT quantity FROM order_items WHERE order_id = 104 AND product_id = 1").fetchone()[0] == 3
# source: https://docs.djangoproject.com/en/5.1/topics/db/models/
# confirmed: "Django's automatically generated many-to-many tables include such a constraint" (a UniqueConstraint on the from and to fields)
print("097 ok")
