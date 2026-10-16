# checks for notes/023-true-and-false-the-boolean.md
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop
con = shop()
rows = con.execute("SELECT order_id, status, status = 'delivered' AS delivered FROM orders").fetchall()
assert len(rows) == 7
assert [r[2] for r in rows] == [True, True, True, False, True, False, True]
assert sum(r[2] for r in rows) == 5
flags = [True, True, True, False, True, False, True]
assert sum(flags) == 5 and True == 1 and False == 0
# one bit holds two states, a byte is 8 bits
assert 2 ** 1 == 2 and 8 == 8
# source: https://www.postgresql.org/docs/current/datatype-boolean.html
#   confirmed: boolean uses 1 byte; input accepts true/yes/on/1 and false/no/off/0
print("023 ok")
