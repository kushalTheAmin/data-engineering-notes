# checks for notes/114-three-valued-logic-true-false-and-unknown.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda w: [r[0] for r in con.execute("SELECT name FROM customers WHERE " + w).fetchall()]
assert len(con.execute("SELECT 1 FROM customers").fetchall()) == 5
assert con.execute("SELECT city FROM customers WHERE name = 'Esha'").fetchone() == (None,)
# the three rows of the table: unknown with true, false and unknown
rows = {}
for b in ("true", "false", "NULL"):
    rows[b] = con.execute("SELECT (NULL::BOOLEAN AND %s), (NULL::BOOLEAN OR %s)" % (b, b)).fetchone()
assert rows["true"] == (None, True)
assert rows["false"] == (False, None)
assert rows["NULL"] == (None, None)
# the order of the sides does not matter
assert con.execute("SELECT (true AND NULL::BOOLEAN) IS NULL, (false AND NULL::BOOLEAN), (true OR NULL::BOOLEAN)").fetchone() == (True, False, True)
# python shortcut
assert (False and 1 / 1) is False
assert con.execute("SELECT joined_on FROM customers WHERE name = 'Esha'").fetchone()[0].isoformat() == "2026-03-15"
assert con.execute("SELECT joined_on FROM customers WHERE name = 'Disha'").fetchone()[0].isoformat() == "2026-03-02"
r = con.execute("SELECT name, city = 'Hoboken', joined_on < DATE '2026-03-01', city = 'Hoboken' AND joined_on < DATE '2026-03-01' FROM customers WHERE name IN ('Disha', 'Esha') ORDER BY customer_id").fetchall()
assert r == [("Disha", True, False, False), ("Esha", None, False, False)]
assert q("NOT (city = 'Hoboken' AND joined_on < DATE '2026-03-01')") == ["Asha", "Bhavin", "Chirag", "Disha", "Esha"]
assert len(q("NOT (city = 'Hoboken' AND joined_on < DATE '2026-03-01')")) == 5
assert q("city = 'Hoboken' OR joined_on > DATE '2026-03-15'") == ["Disha"]
assert q("city = 'Hoboken' OR joined_on >= DATE '2026-03-15'") == ["Disha", "Esha"]
assert q("NOT city = 'Hoboken'") == ["Asha", "Bhavin", "Chirag"]  # 110: the city alone drops Esha
# source: https://www.postgresql.org/docs/current/functions-logical.html
# confirmed: SQL uses a three-valued logic system with true, false and null, which represents unknown, with truth tables for AND, OR and NOT
# source: https://www.postgresql.org/docs/current/queries-table-expressions.html
# confirmed: WHERE keeps a row only when the condition is true; false or null is discarded
print("114 ok")
