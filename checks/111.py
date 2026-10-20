# checks for notes/111-in-matching-against-a-list.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda w: [r[0] for r in con.execute("SELECT name FROM customers WHERE " + w).fetchall()]
assert len(con.execute("SELECT 1 FROM customers").fetchall()) == 5
assert q("city IN ('Jersey City', 'Hoboken')") == ["Asha", "Chirag", "Disha"]
assert q("city = 'Jersey City' OR city = 'Hoboken'") == q("city IN ('Jersey City', 'Hoboken')")
assert q("city NOT IN ('Edison', NULL)") == []
assert q("city NOT IN ('Edison')") == ["Asha", "Chirag", "Disha"]
rows = con.execute("SELECT name, city FROM customers ORDER BY customer_id").fetchall()
assert rows == [("Asha", "Jersey City"), ("Bhavin", "Edison"), ("Chirag", "Jersey City"), ("Disha", "Hoboken"), ("Esha", None)]
assert [n for n, c in rows if c in ("Jersey City", "Hoboken")] == ["Asha", "Chirag", "Disha"]
assert con.execute("SELECT NULL = 'Jersey City'").fetchone()[0] is None
# source: https://www.postgresql.org/docs/current/functions-subquery.html
# confirmed: NOT IN gives null, not true, when no equal value is found and at least one right-hand value is null; IN with a null left side gives null
print("111 ok")
