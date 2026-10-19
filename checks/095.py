# checks for notes/095-composite-keys.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
import duckdb
con = shop()
assert con.execute("SELECT order_id, product_id, quantity FROM order_items WHERE order_id IN (101, 103) ORDER BY order_id, product_id").fetchall() == [(101, 1, 2), (101, 5, 2), (103, 2, 1), (103, 5, 1)]
assert con.execute("SELECT name FROM products WHERE product_id = 5").fetchone()[0] == "masala chai"
assert con.execute("SELECT count(*) FROM (SELECT order_id, product_id FROM order_items GROUP BY 1, 2 HAVING count(*) > 1)").fetchone()[0] == 0
try:
    con.execute("INSERT INTO order_items VALUES (103, 5, 9)")
    raise SystemExit("insert should fail")
except duckdb.ConstraintException as e:
    assert "violates primary key constraint" in str(e)
assert con.execute("SELECT product_id FROM order_items WHERE order_id = 106").fetchall() == [(2,)]
assert con.execute("SELECT count(*) FROM order_items WHERE order_id = 106 AND product_id = 1").fetchone()[0] == 0
assert con.execute("SELECT count(*) FROM order_items WHERE order_id <> 106 AND product_id = 1").fetchone()[0] > 0
con.execute("INSERT INTO order_items VALUES (106, 1, 1)")
# triple key accepts the duplicate pair
con.execute("CREATE TABLE t (o INTEGER, p INTEGER, q INTEGER, PRIMARY KEY (o, p, q))")
con.execute("INSERT INTO t VALUES (103, 5, 1), (103, 5, 9)")
assert con.execute("SELECT count(*) FROM t").fetchone()[0] == 2
sql = open(os.path.join(os.path.dirname(__file__), "..", "data", "shop.sql")).read()
assert "PRIMARY KEY (order_id, product_id)" in sql
assert "REFERENCES orders (order_id)" in sql and "REFERENCES products (product_id)" in sql
# source: https://www.postgresql.org/docs/current/ddl-constraints.html
# confirmed: a primary key can span several columns, written PRIMARY KEY (a, b), and then the combination must be unique
print("095 ok")
