# checks for notes/001-data-is-facts-and-numbers.md
# every number and computable fact in the note is asserted here. every other
# factual claim has a source line for a page that was opened and confirmed.
import sys, os, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop

con = shop()
# the shop: five customers, six products
assert con.execute("SELECT COUNT(*) FROM customers").fetchone()[0] == 5
assert con.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 6
# one real order: Asha ordered 2 dhokla on april 1 2026 at 9:15
row = con.execute("""
    SELECT c.name, p.name, oi.quantity, o.ordered_at
    FROM orders o JOIN customers c USING (customer_id)
    JOIN order_items oi USING (order_id) JOIN products p USING (product_id)
    WHERE o.order_id = 101 AND p.name = 'dhokla'""").fetchone()
assert row == ("Asha", "dhokla", 2, datetime.datetime(2026, 4, 1, 9, 15))
# letters become numbers
assert [ord(c) for c in "Asha"] == [65, 115, 104, 97]
assert [ord(c) for c in "dhokla"] == [100, 104, 111, 107, 108, 97]
# 97 could be the letter a or just ninety seven
assert chr(97) == "a"
# april 1 2026, 9:15 UTC as seconds since the start of 1970 UTC
assert int(datetime.datetime(2026, 4, 1, 9, 15, tzinfo=datetime.timezone.utc).timestamp()) == 1775034900
# source: https://en.wikipedia.org/wiki/Unix_time
#   counts seconds since 00:00:00 UTC on 1 January 1970; used by linux and
#   macOS (Unix-like systems) and by javascript Date (milliseconds)
# source: https://en.wikipedia.org/wiki/Mojibake
#   garbled text comes from decoding with an unintended encoding
print("001 ok")
