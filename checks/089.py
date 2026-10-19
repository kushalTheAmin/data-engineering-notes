# checks for notes/089-update-anomalies.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
# asha is customer 1 in Jersey City with orders 101, 103, 106; bhavin 102 Edison; disha 105 Hoboken
q = """SELECT o.order_id, c.name, c.city FROM orders o JOIN customers c USING (customer_id)
       WHERE o.order_id IN (101,102,103,105,106) ORDER BY 1"""
got = {r[0]: (r[1], r[2]) for r in con.execute(q).fetchall()}
assert got[101] == got[103] == got[106] == ("Asha", "Jersey City")
assert got[102] == ("Bhavin", "Edison") and got[105] == ("Disha", "Hoboken")
assert con.execute("SELECT count(*) FROM customers WHERE name = 'Asha'").fetchone()[0] == 1
# q1: update Asha's orders below 105 to Hoboken
rows = {o: v[1] for o, v in got.items() if o in (101, 103, 105, 106)}
for o in rows:
    if got[o][0] == "Asha" and o < 105:
        rows[o] = "Hoboken"
assert sum(c == "Hoboken" for c in rows.values()) == 3
assert [o for o, c in rows.items() if got[o][0] == "Asha" and c == "Jersey City"] == [106]
# q2: a trailing space breaks the match
assert "asha " != "Asha"
# source: https://en.wikipedia.org/wiki/Database_normalization
# confirmed: "to reduce data redundancy and improve data integrity"
print("089 ok")
