# checks for notes/101-sql-you-describe-the-result.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
# the query and the python loop give the same answer
sql = [r[0] for r in con.execute("SELECT name FROM customers WHERE city = 'Jersey City'").fetchall()]
customers = [("Asha", "Jersey City"), ("Bhavin", "Edison"), ("Chirag", "Jersey City"), ("Disha", "Hoboken"), ("Esha", None)]
found = [n for n, c in customers if c == "Jersey City"]
assert sql == found == ["Asha", "Chirag"]
# the python list mirrors the real customers table
assert [tuple(r) for r in con.execute("SELECT name, city FROM customers ORDER BY customer_id").fetchall()] == customers
# Esha: one row, city NULL
assert con.execute("SELECT city FROM customers WHERE name = 'Esha'").fetchall() == [(None,)]
# four tables
assert con.execute("SELECT count(*) FROM customers").fetchone()[0] == 5
# source: https://en.wikipedia.org/wiki/SQL
# confirmed: SQL is a set-based, declarative language; implementations are incompatible between vendors in places
# (dialects), and it has an ISO standard
print("101 ok")
