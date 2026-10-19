# checks for notes/091-splitting-into-tables.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
assert con.execute("SELECT customer_id, name, city FROM customers ORDER BY 1").fetchall() == [
    (1,"Asha","Jersey City"),(2,"Bhavin","Edison"),(3,"Chirag","Jersey City"),(4,"Disha","Hoboken"),(5,"Esha",None)]
o = dict(con.execute("SELECT order_id, customer_id FROM orders").fetchall())
assert len(o) == 7
assert [(k, o[k]) for k in (101,103,104,106)] == [(101,1),(103,1),(104,3),(106,1)]
assert sorted(k for k,v in o.items() if v == 1) == [101,103,106]
# wide table: one city per order row
assert con.execute("SELECT count(c.city) FROM orders o JOIN customers c USING (customer_id)").fetchone()[0] == 7
# split: one city per customer that has one
assert con.execute("SELECT count(city) FROM customers").fetchone()[0] == 4
assert con.execute("SELECT count(*) FROM customers").fetchone()[0] == 5
assert 5 not in o.values()
assert [k for k,v in o.items() if v == 3] == [104]
print("091 ok")
