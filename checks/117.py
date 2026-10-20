# checks for notes/117-order-by-sorting-by-one-or-more-columns.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
rows = con.execute("SELECT name, category, price FROM products ORDER BY category, price DESC").fetchall()
assert [r[0] for r in rows] == ["masala chai", "khandvi", "dhokla", "fafda", "kaju katli", "jalebi"]
assert len(rows) == 6
assert [r[1] for r in rows] == ["drink", "snack", "snack", "snack", "sweet", "sweet"]
assert [float(r[2]) for r in rows] == [3.0, 7.5, 6.0, 4.5, 12.0, 5.0]
assert [r[1] for r in rows] == sorted(r[1] for r in rows)
assert sum(1 for r in rows if r[1] == "snack") == 3
assert rows.index(max(rows, key=lambda r: r[2])) == 4  # kaju katli is the priciest, fifth row (index 4)
assert max(rows, key=lambda r: r[2])[0] == "kaju katli"
py = [("khandvi", "snack", 7.5), ("jalebi", "sweet", 5.0), ("dhokla", "snack", 6.0)]
assert sorted(py, key=lambda r: (r[1], -r[2])) == [("khandvi", "snack", 7.5), ("dhokla", "snack", 6.0), ("jalebi", "sweet", 5.0)]
# source: https://www.postgresql.org/docs/current/queries-order.html
# confirmed: the sort runs after the query has produced its output rows; ASC is the default; with several sort expressions, later ones sort rows that tie on earlier ones
# python compares pairs first item first, second only on a tie
assert (1, 9) < (2, 0) and (1, 2) < (1, 3)
# source: https://en.wikipedia.org/wiki/Dhokla
# confirmed: dhokla is a savoury sponge dish steamed to a cake-like consistency
# source: https://en.wikipedia.org/wiki/Kaju_katli
# confirmed: kaju katli page is categorised Indian desserts and Cashew dishes
# source: https://en.wikipedia.org/wiki/Fafda
# confirmed: fafda is rolled, flattened and deep-fried till crispy
# source: https://en.wikipedia.org/wiki/Jalebi
# confirmed: jalebi is "a common sweet snack", fried batter soaked in sugar syrup
# source: https://en.wikipedia.org/wiki/Khandvi_(food)
# confirmed: khandvi is a savory snack in Gujarati cuisine, "tightly rolled bite-sized pieces", primarily gram flour and yogurt
# source: https://en.wikipedia.org/wiki/Gram_flour
# confirmed: "Chickpea flour, common varieties include besan or gram flour"
print("117 ok")
