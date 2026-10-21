# checks for notes/131-integer-division-when-7-divided-by-2-gives-3.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
r = con.execute("SELECT 7 / 2, 7 // 2").fetchone()
assert r == (3.5, 3)
assert 3 // 2 == 1 and 3 / 2 == 1.5
rows = con.execute("SELECT order_id, product_id, quantity, quantity / 2, quantity // 2 FROM order_items WHERE order_id IN (104, 105) ORDER BY order_id, product_id").fetchall()
assert rows == [(104, 1, 3, 1.5, 1), (105, 3, 2, 1.0, 1), (105, 4, 2, 1.0, 1), (105, 5, 1, 0.5, 0)]
# order 104 is 3 dhokla (product 1)
assert con.execute("SELECT name FROM products WHERE product_id = 1").fetchone()[0] == "dhokla"
assert con.execute("SELECT 1 // 2").fetchone()[0] == 0
# truncation toward zero for negatives, same as postgres
assert con.execute("SELECT (-5) // 2").fetchone()[0] == -2
# a rate of 1 cancelled out of 2 placed
assert 1 // 2 == 0 and 1 / 2 == 0.5
assert con.execute("SELECT 3 / 2.0").fetchone()[0] == 1.5
# source: https://www.postgresql.org/docs/current/functions-math.html
# confirmed: for integral types, division truncates the result towards zero; 5 / 2 gives 2, (-5) / 2 gives -2, 5.0 / 2 gives 2.5
# source: https://duckdb.org/docs/current/sql/functions/numeric.html
# confirmed: when both operands are integers, / performs floating point division (5 / 2 = 2.5) while // performs integer division (5 // 2 = 2)
assert 3 // 2 * 2 == 2 and 1.0 * 1 / 2 == 0.5
print("131 ok")
