# checks for notes/312-apis-a-door-built-for-programs.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
# Asha is customer 1, her orders are 101, 103, 106
assert con.execute("SELECT name FROM customers WHERE customer_id = 1").fetchone()[0] == "Asha"
assert [r[0] for r in con.execute("SELECT order_id FROM orders WHERE customer_id = 1 ORDER BY order_id").fetchall()] == [101, 103, 106]
# Esha is customer 5 and has no orders
assert con.execute("SELECT name FROM customers WHERE customer_id = 5").fetchone()[0] == "Esha"
assert con.execute("SELECT count(*) FROM orders WHERE customer_id = 5").fetchone()[0] == 0
# source: https://docs.github.com/en/rest/quickstart
# confirmed: the quickstart example is a GET to https://api.github.com/repos/octocat/Spoon-Knife/issues, the API host is api.github.com while the site is github.com
print("312 ok")
# audit: the note called an empty list with a 200 the usual choice, which no page supports. it now just says an empty list with a 200, and the shop could choose otherwise
