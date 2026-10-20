# checks for notes/108-and-or-combining-two-tests.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
rows = con.execute("SELECT name, category, price FROM products ORDER BY product_id").fetchall()
assert len(rows) == 6
table = {}
for n, cat, p in rows:
    a, b = cat == "snack", p < 6
    table[n] = (a, b, a and b, a or b)
assert table == {
    "dhokla": (True, False, False, True),
    "khandvi": (True, False, False, True),
    "jalebi": (False, True, False, True),
    "kaju katli": (False, False, False, False),
    "masala chai": (False, True, False, True),
    "fafda": (True, True, True, True),
}
q = lambda w: [r[0] for r in con.execute("SELECT name FROM products WHERE " + w).fetchall()]
assert q("category = 'snack' AND price < 6") == ["fafda"]
assert q("category = 'snack' OR price < 6") == ["dhokla", "khandvi", "jalebi", "masala chai", "fafda"]
assert len(q("category = 'snack' OR price < 6")) == 5
assert q("category = 'snack' AND category = 'sweet'") == []
assert q("category = 'snack' OR category = 'sweet'") == ["dhokla", "khandvi", "jalebi", "kaju katli", "fafda"]
# source: https://duckdb.org/docs/current/sql/expressions/logical_operators
# confirmed: AND is true only if both operands are true, OR if at least one is
# source: https://en.wikipedia.org/wiki/Dhokla
# confirmed: "a savoury sponge dish", "fermented batter that is steamed to a cake-like consistency"
# source: https://en.wikipedia.org/wiki/Kaju_katli
# confirmed: "Kaju katli (lit. 'Cashew slice') is an Indian dessert"
print("108 ok")
