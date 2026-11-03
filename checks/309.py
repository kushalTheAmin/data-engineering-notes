# checks for notes/309-http-methods-get-asks-post-sends.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
# the toy server starts with the 7 real order ids
ids = [r[0] for r in con.execute("SELECT order_id FROM orders ORDER BY order_id").fetchall()]
assert ids == [101, 102, 103, 104, 105, 106, 107]
assert len(ids) == 7
# two POSTs add 108 and 109, so the last GET says 9
assert len(ids) + 2 == 9 and ids[-1] + 1 == 108 and ids[-1] + 2 == 109
# the POST body is 13 characters
assert len("customer_id=2") == 13
# Bhavin is customer 2
assert con.execute("SELECT name FROM customers WHERE customer_id = 2").fetchone()[0] == "Bhavin"
# check yourself 1: Asha has 3 orders, two POSTs that arrived make 5
asha = con.execute("SELECT count(*) FROM orders WHERE customer_id = 1").fetchone()[0]
assert asha == 3 and asha + 2 == 5
# source: https://www.rfc-editor.org/rfc/rfc9110.txt
# confirmed (section 9.2.2): PUT, DELETE and safe methods are idempotent; a client SHOULD NOT automatically retry a request with a non-idempotent method unless it knows the request is idempotent or can detect it was never applied; POST is not in the idempotent list
# confirmed (section 9.3.3): POST asks the target resource to process the enclosed representation; GET (9.3.1) requests transfer of a current representation
print("309 ok")
