# checks for notes/142-min-and-max-the-smallest-and-biggest-value.md
import os, sys
from decimal import Decimal
from datetime import datetime
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT min(price), max(price), min(name), max(name) FROM products") == [(Decimal("3.00"), Decimal("12.00"), "dhokla", "masala chai")]
assert q("SELECT name FROM products WHERE price = 3.00") == [("masala chai",)]
assert q("SELECT name FROM products WHERE price = 12.00") == [("kaju katli",)]
assert q("SELECT name, price FROM products ORDER BY price DESC LIMIT 1") == [("kaju katli", Decimal("12.00"))]
assert q("SELECT price FROM products WHERE name = 'dhokla'") != [(Decimal("3.00"),)]
assert q("SELECT count(*) FROM order_ratings") == [(5,)]
assert q("SELECT min(stars), max(stars) FROM order_ratings") == [(3, 5)]
assert q("SELECT min(stars), max(stars) FROM order_ratings WHERE stars IS NULL") == [(None, None)]
assert q("SELECT max(ordered_at) FROM orders") == [(datetime(2026, 4, 9, 13, 45),)]
# python loop shape: best so far
best = None
for p in [6.0, 7.5, 5.0, 12.0, 3.0, 4.5]:
    if best is None or p > best:
        best = p
assert best == 12.0
# source: https://www.postgresql.org/docs/current/functions-aggregate.html
# confirmed: max "Computes the maximum of the non-null input values", min likewise, available for numeric, string and date/time types
# source: https://en.wikipedia.org/wiki/Kaju_katli
# confirmed: kaju katli is "an Indian dessert" and "Kaju means cashew"
# source: https://en.wikipedia.org/wiki/Dhokla
# confirmed: dhokla is "steamed to a cake-like consistency"
# source: https://en.wikipedia.org/wiki/Masala_chai
# confirmed: flavoured Indian tea (spiced tea redirects to this page)
