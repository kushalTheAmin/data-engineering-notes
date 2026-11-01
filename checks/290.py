# checks for notes/290-composite-indexes-sorted-by-the-first-column-then-the-second.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
a = q("SELECT customer_id, order_id FROM orders ORDER BY customer_id, ordered_at")
assert [o for c, o in a if c == 1] == [101, 103, 106]
assert [o for c, o in a] == [101, 103, 106, 102, 107, 104, 105]
b = q("SELECT customer_id, order_id FROM orders ORDER BY ordered_at, customer_id")
assert [o for c, o in b] == [101, 102, 103, 104, 105, 106, 107]
assert [c for c, o in b] == [1, 2, 1, 3, 4, 1, 2]
assert q("SELECT count(DISTINCT ordered_at), count(*) FROM orders") == [(7, 7)]
assert q("SELECT status, customer_id FROM orders ORDER BY status, customer_id LIMIT 3") == [("cancelled", 3), ("delivered", 1), ("delivered", 1)]
assert q("SELECT city, name FROM customers WHERE city IS NOT NULL ORDER BY city, name") == [("Edison", "Bhavin"), ("Hoboken", "Disha"), ("Jersey City", "Asha"), ("Jersey City", "Chirag")]
# 3 entries for Asha, 7 orders
assert q("SELECT count(*) FROM orders WHERE customer_id = 1") == [(3,)]
# source: https://www.postgresql.org/docs/16/indexes-multicolumn.html
# confirmed: page titled Multicolumn Indexes; a scan runs from the first entry with a=5 and b=42 up through the last entry with a=5 (opened this run)
# audit: the city query drops Esha (customer 5) because her city is missing; the answer now says so
assert q("SELECT customer_id FROM customers WHERE city IS NULL") == [(5,)]
