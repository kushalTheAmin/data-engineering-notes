# checks for notes/255-entities-and-attributes.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT city, count(*) FROM customers GROUP BY city ORDER BY city") == [('Edison', 1), ('Hoboken', 1), ('Jersey City', 2), (None, 1)]
# Asha (1) and Chirag (3) share Jersey City; Esha (5) has no city
assert q("SELECT customer_id FROM customers WHERE city = 'Jersey City' ORDER BY 1") == [(1,), (3,)]
assert q("SELECT name FROM customers WHERE city IS NULL") == [('Esha',)]
assert [r[0] for r in q("SELECT column_name FROM information_schema.columns WHERE table_name = 'customers' ORDER BY ordinal_position")] == ['customer_id', 'name', 'city', 'joined_on']
