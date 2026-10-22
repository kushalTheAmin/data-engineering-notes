# checks for notes/162-right-and-full-outer-joins.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
full = q("""SELECT '"' || s.typed_name || '"', c.name FROM customers c FULL JOIN signups s ON c.name = s.typed_name ORDER BY c.name, s.typed_name""")
assert len(full) == 7
assert full[-2:] == [('"CHIRAG "', None), ('"bhavin "', None)]
# 5 customers + 4 signups - 2 matched pairs
assert q("SELECT count(*) FROM customers") == [(5,)]
assert q("SELECT count(*) FROM signups") == [(4,)]
assert q("SELECT count(*) FROM customers c JOIN signups s ON c.name = s.typed_name") == [(2,)]
assert 5 + 4 - 2 == 7
# right join with tables swapped is the same as left join
r = q("SELECT c.name, s.typed_name FROM signups s RIGHT JOIN customers c ON c.name = s.typed_name ORDER BY c.name")
l = q("SELECT c.name, s.typed_name FROM customers c LEFT JOIN signups s ON c.name = s.typed_name ORDER BY c.name")
assert r == l and len(r) == 5
# python loop in the note
customers = ["Asha", "Bhavin", "Chirag", "Disha", "Esha"]
signups = ["Asha", "bhavin ", "CHIRAG ", "Disha"]
assert signups == [x[0] for x in q("SELECT typed_name FROM signups ORDER BY signup_id")]
assert "Bhavin" != "bhavin " and "bhavin ".strip().lower() == "bhavin"
# source: https://www.postgresql.org/docs/current/queries-table-expressions.html
# confirmed: FULL OUTER JOIN adds unmatched rows from both T1 and T2; RIGHT OUTER JOIN is the converse of a left join
