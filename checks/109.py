# checks for notes/109-parentheses-and-runs-before-or.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda t, w: [r[0] for r in con.execute("SELECT name FROM " + t + " WHERE " + w).fetchall()]
a = q("products", "category = 'snack' OR category = 'sweet' AND price < 6")
b = q("products", "(category = 'snack' OR category = 'sweet') AND price < 6")
assert a == ["dhokla", "khandvi", "jalebi", "fafda"] and len(a) == 4
assert b == ["jalebi", "fafda"] and len(b) == 2
# khandvi is 7.50 and dhokla 6.00, both snacks, both in the first result
prices = dict(con.execute("SELECT name, price FROM products").fetchall())
assert float(prices["khandvi"]) == 7.5 and float(prices["dhokla"]) == 6.0
assert q("products", "category = 'snack' OR (category = 'sweet' AND price < 6)") == a
assert q("products", "category = 'drink' OR category = 'sweet' AND price > 10") == ["kaju katli", "masala chai"]
assert float(prices["kaju katli"]) == 12.0 and float(prices["masala chai"]) == 3.0
w = "city = 'Jersey City' OR city = 'Edison' AND joined_on < DATE '2026-02-01'"
assert q("customers", w) == ["Asha", "Bhavin", "Chirag"]
assert q("customers", "(city = 'Jersey City' OR city = 'Edison') AND joined_on < DATE '2026-02-01'") == ["Asha", "Bhavin"]
# python has the same rule: and binds tighter than or
for x, y, z in [(True, False, False), (True, True, False), (False, True, True), (False, False, True)]:
    assert (x or y and z) == (x or (y and z))
# source: https://www.postgresql.org/docs/current/sql-syntax-lexical.html
# confirmed: operator table lists NOT, then AND, then OR; precedence is hard-wired into the parser (the docs word for fixed); add parentheses for other grouping
print("109 ok")
