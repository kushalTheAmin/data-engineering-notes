# checks for notes/090-insert-and-delete-anomalies.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = """SELECT o.order_id, c.name, c.city FROM orders o JOIN customers c USING (customer_id) ORDER BY 1"""
rows = con.execute(q).fetchall()
assert len(rows) == 7
assert rows == [(101,"Asha","Jersey City"),(102,"Bhavin","Edison"),(103,"Asha","Jersey City"),
                (104,"Chirag","Jersey City"),(105,"Disha","Hoboken"),(106,"Asha","Jersey City"),
                (107,"Bhavin","Edison")]
# esha is a customer with no order
assert con.execute("SELECT count(*) FROM customers WHERE name='Esha'").fetchone()[0] == 1
assert con.execute("SELECT count(*) FROM orders WHERE customer_id=5").fetchone()[0] == 0
assert "Esha" not in {r[1] for r in rows}
assert str(con.execute("SELECT joined_on FROM customers WHERE name='Esha'").fetchone()[0]) == '2026-03-15'  # joined in March
# chirag has exactly one order, 104, cancelled
assert con.execute("SELECT order_id, status FROM orders WHERE customer_id=3").fetchall() == [(104,"cancelled")]
assert con.execute("SELECT count(*) FROM customers").fetchone()[0] == 5
after = {r[1] for r in rows if r[0] != 104}
assert sorted(after) == ["Asha","Bhavin","Disha"]
# source: https://en.wikipedia.org/wiki/Database_normalization
# confirmed: captions describe insertion anomaly ("details cannot be recorded" until assigned a course) and deletion anomaly (information lost when no courses)
print("090 ok")
