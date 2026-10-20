# checks for notes/118-no-order-by-no-promised-order.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
rows = con.execute("SELECT name, category FROM products").fetchall()
assert len(rows) == 6
assert [r[0] for r in rows] == ["dhokla", "khandvi", "jalebi", "kaju katli", "masala chai", "fafda"]
assert [r[1] for r in rows] == ["snack", "snack", "sweet", "sweet", "drink", "snack"]
py = ["dhokla", "khandvi", "jalebi", "kaju katli", "masala chai", "fafda"]
assert list(reversed(py)) == ["fafda", "masala chai", "kaju katli", "jalebi", "khandvi", "dhokla"]
assert sorted(py) == sorted(reversed(py))
assert py != list(reversed(py))
# 3 snacks tie on category
assert sum(1 for r in rows if r[1] == "snack") == 3
q = con.execute("SELECT name FROM products ORDER BY category, name").fetchall()
assert [r[0] for r in q] == ["masala chai", "dhokla", "fafda", "khandvi", "jalebi", "kaju katli"]
snacks = [r for r in con.execute("SELECT name, product_id FROM products WHERE category = 'snack' ORDER BY product_id").fetchall()]
assert [r[0] for r in snacks] == ["dhokla", "khandvi", "fafda"]
# postgres is a server database: https://www.postgresql.org/docs/current/tutorial-arch.html ("PostgreSQL uses a client/server model")
# source: https://www.postgresql.org/docs/current/queries-order.html
# confirmed: "If sorting is not chosen, the rows will be returned in an unspecified order. The actual order in that case will depend on the scan and join plan types and the order on disk, but it must not be relied on."
# source: https://duckdb.org/docs/current/sql/dialect/order_preservation
# confirmed: "For many operations, DuckDB preserves the order of rows"; FROM with a single table, SELECT and WHERE "guarantee that the original row order is preserved"
# source: https://www.postgresql.org/docs/current/sql-select.html
# confirmed: "If ORDER BY is not given, the rows are returned in whatever order the system finds fastest to produce."
# source: https://en.wikipedia.org/wiki/Dhokla
# confirmed: dhokla is a savoury sponge dish steamed to a cake-like consistency
# source: https://en.wikipedia.org/wiki/Kaju_katli
# confirmed: kaju katli is an Indian dessert made from cashews
# source: https://en.wikipedia.org/wiki/Fafda
# confirmed: fafda is a chickpea flour snack, fried till crispy
# source: https://en.wikipedia.org/wiki/Gram_flour
# confirmed: chickpea flour, common varieties include besan or gram flour (khandvi and fafda glosses)
# jalebi (syrupy sweet) gloss as used in notes 103/104/117
print("118 ok")
