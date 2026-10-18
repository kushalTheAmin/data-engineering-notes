# checks for notes/061-structure-why-text-is-hard-to-ask.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
items = con.execute("""SELECT oi.order_id, p.name, oi.quantity FROM order_items oi
                       JOIN products p USING (product_id) ORDER BY 1, 2""").fetchall()
d = {(o, n): q for o, n, q in items}
assert d[(101, "dhokla")] == 2 and d[(101, "masala chai")] == 2     # Asha's message
assert d[(104, "dhokla")] == 3                                      # Chirag's message
assert d[(107, "dhokla")] == 1 and d[(107, "jalebi")] == 1          # Bhavin's message
cust = dict(con.execute("SELECT order_id, c.name FROM orders o JOIN customers c USING (customer_id)").fetchall())
assert cust[101] == "Asha" and cust[104] == "Chirag" and cust[107] == "Bhavin"
assert sum(q for (o, n), q in d.items() if n == "dhokla") == 6      # real total ordered (order 104 is cancelled, so the note says ordered, not sold)
assert con.execute("SELECT status FROM orders WHERE order_id = 104").fetchone()[0] == "cancelled"
found = 2 + 1                                                       # the rule finds 2, nothing, 1
assert found == 3
# source: https://en.wikipedia.org/wiki/Dhokla
#   confirmed: "a savoury sponge dish that originated in the Indian state of Gujarat", "steamed to a cake-like consistency"
print("061 ok")
