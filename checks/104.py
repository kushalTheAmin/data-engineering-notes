# checks for notes/104-select-and-from-picking-columns.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
from decimal import Decimal
con = shop()
# the slice shown: first 3 rows, 4 columns
cols = [r[0] for r in con.execute("DESCRIBE products").fetchall()]
assert cols == ["product_id", "name", "category", "price"]
assert con.execute("SELECT * FROM products ORDER BY product_id LIMIT 3").fetchall() == [
    (1, "dhokla", "snack", Decimal("6.00")), (2, "khandvi", "snack", Decimal("7.50")), (3, "jalebi", "sweet", Decimal("5.00"))]
# flipped order, all six rows
res = con.execute("SELECT price, name FROM products").fetchall()
assert len(res) == 6 and res[0] == (Decimal("6.00"), "dhokla")
# category: one result row per table row, snack three times
cats = [r[0] for r in con.execute("SELECT category FROM products").fetchall()]
assert cats == ["snack", "snack", "sweet", "sweet", "drink", "snack"]
assert len(cats) == 6 and cats.count("snack") == 3
# python shape: new dict per row with only the listed keys, in that order
rows = [dict(zip(cols, r)) for r in con.execute("SELECT * FROM products").fetchall()]
out = [{k: r[k] for k in ("price", "name")} for r in rows]
assert list(out[0]) == ["price", "name"] and "category" not in out[0]
# SELECT DISTINCT and WHERE can drop rows, so only the plain column list never does
assert len(con.execute("SELECT DISTINCT category FROM products").fetchall()) == 3
assert len(con.execute("SELECT category FROM products WHERE category = 'snack'").fetchall()) == 3
# source: https://en.wikipedia.org/wiki/Fafda
# confirmed: native to Gujarat; "gram flour" dough, deep-fried till crispy; the page never says strip
# source: https://en.wikipedia.org/wiki/Gram_flour
# confirmed: "Chickpea flour, common varieties include besan or gram flour."
# source: https://en.wikipedia.org/wiki/Khandvi_(food)
# confirmed: a savory snack of Gujarati cuisine, tightly rolled bite-sized pieces, primarily made of gram flour and yogurt
# source: https://en.wikipedia.org/wiki/Jalebi
# confirmed: batter deep-fried in pretzel or circular shapes, then soaked in sugar syrup
# source: https://en.wikipedia.org/wiki/Kaju_katli
# confirmed: an Indian dessert; kaju means cashew
# source: https://en.wikipedia.org/wiki/Masala_chai
# confirmed: flavoured Indian tea (spiced tea redirects to this page)
print("104 ok")
