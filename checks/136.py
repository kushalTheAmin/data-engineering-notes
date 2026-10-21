# checks for notes/136-capstone-one-query-traced-clause-by-clause.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT count(*) FROM products") == [(6,)]
where = "category IN ('snack', 'sweet') AND price >= 5"
assert q(f"SELECT count(*) FROM products WHERE {where}") == [(4,)]
assert [r[0] for r in q(f"SELECT name FROM products WHERE {where} ORDER BY product_id")] == ["dhokla", "khandvi", "jalebi", "kaju katli"]
assert [r[0] for r in q("SELECT name FROM products WHERE NOT (category IN ('snack', 'sweet') AND price >= 5) ORDER BY product_id")] == ["masala chai", "fafda"]
assert [(r[0], float(r[1]), r[2]) for r in q("SELECT name, price - 1 AS sale_price, CASE WHEN price < 5 THEN 'cheap' WHEN price < 8 THEN 'regular' ELSE 'treat' END AS tier FROM products WHERE category IN ('snack', 'sweet') AND price >= 5 ORDER BY sale_price DESC LIMIT 3")] == [("kaju katli", 11.0, "treat"), ("khandvi", 6.5, "regular"), ("dhokla", 5.0, "regular")]
assert [r[0] for r in q("SELECT name FROM products WHERE category = 'snack' OR category = 'sweet' AND price >= 10 ORDER BY price")] == ["fafda", "dhokla", "khandvi", "kaju katli"]
assert [r[0] for r in q("SELECT name FROM products WHERE category = 'snack' OR category = 'sweet' AND price >= 10 ORDER BY price LIMIT 2")] == ["fafda", "dhokla"]
assert [r[0] for r in q("SELECT name FROM products WHERE (category = 'snack' OR category = 'sweet') AND price >= 10")] == ["kaju katli"]
assert [r[0] for r in q("SELECT name FROM products WHERE price - 1 > 5 ORDER BY product_id")] == ["khandvi", "kaju katli"]
assert q("SELECT name, category, price FROM products ORDER BY product_id")[3] == ("kaju katli", "sweet", 12)
# source: https://www.postgresql.org/docs/current/sql-select.html
# confirmed: an output column name can be used in ORDER BY "but not in the WHERE or HAVING clauses"; processing order FROM, WHERE, output expressions, ORDER BY, LIMIT
# source: https://www.postgresql.org/docs/current/tutorial-arch.html
# confirmed: "PostgreSQL uses a client/server model"
# source: https://en.wikipedia.org/wiki/Fafda
# confirmed: fafda is a snack of the Gujarat region
# source: https://en.wikipedia.org/wiki/Jalebi
# confirmed: jalebi is fried batter "soaked in sugar syrup"
# source: https://en.wikipedia.org/wiki/Kaju_katli
# confirmed: kaju katli is "an Indian dessert" and "Kaju means cashew"
# source: https://en.wikipedia.org/wiki/Dhokla
# confirmed: dhokla is made with a batter "steamed to a cake-like consistency", the batter mixes rice with Bengal gram, a variety of chickpea
# source: https://en.wikipedia.org/wiki/Khandvi_(food)
# confirmed: khandvi has "tightly rolled bite-sized pieces" and is "primarily made of gram flour and yogurt"
# source: https://en.wikipedia.org/wiki/Fafda
# confirmed: fafda is made of "gram flour, oil, carom seeds" and "deep-fried till they turn crispy"
print("136 ok")
