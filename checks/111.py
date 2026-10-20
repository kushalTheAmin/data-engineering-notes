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
# a list pulled from a column with a missing value does the same thing
assert q("city NOT IN (SELECT city FROM customers WHERE name IN ('Bhavin', 'Esha'))") == []
assert q("city NOT IN (SELECT city FROM customers WHERE name = 'Bhavin')") == ["Asha", "Chirag", "Disha"]
# an equal item is found, so the null does not matter: IN stays true
assert con.execute("SELECT 'Edison' IN ('Edison', NULL), 'Asha' IN ('Edison', NULL), 'Asha' NOT IN ('Edison', NULL)").fetchone() == (True, None, None)
# source: https://www.postgresql.org/docs/current/functions-comparisons.html
# confirmed: "if there are no equal right-hand values and at least one right-hand expression yields null, the result of the NOT IN construct will be null, not true as one might naively expect"
# source: https://www.postgresql.org/docs/current/functions-subquery.html
# confirmed: the same sentence for expression NOT IN (subquery), which is the column form
print("111 ok")
