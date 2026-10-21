# checks for notes/134-the-order-sql-really-runs-in.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT count(*) FROM products") == [(6,)]
assert [r[0] for r in q("SELECT name FROM products WHERE category = 'snack' ORDER BY product_id")] == ["dhokla", "khandvi", "fafda"]
assert [float(r[0]) for r in q("SELECT price - 1 FROM products WHERE category = 'snack' ORDER BY product_id")] == [5.0, 6.5, 3.5]
assert [r[0] for r in q("SELECT name FROM products WHERE category = 'snack' ORDER BY price - 1")] == ["fafda", "dhokla", "khandvi"]
assert [r[0] for r in q("SELECT name, price - 1 AS sale_price FROM products WHERE category = 'snack' ORDER BY sale_price LIMIT 2")] == ["fafda", "dhokla"]
assert q("SELECT order_id FROM orders WHERE status = 'delivered' ORDER BY ordered_at DESC LIMIT 2") == [(107,), (105,)]
assert [r[0] for r in q("SELECT order_id FROM (SELECT * FROM orders ORDER BY ordered_at DESC LIMIT 2) WHERE status = 'delivered'")] == [107]
assert q("SELECT name FROM products ORDER BY 0 - price LIMIT 1") == [("kaju katli",)]
assert q("SELECT name, 0 - price AS price FROM products ORDER BY price LIMIT 1")[0][0] == "kaju katli"
# source: https://www.postgresql.org/docs/current/sql-select.html
# confirmed: output column name usable in ORDER BY and GROUP BY "but not in the WHERE or HAVING clauses"; ORDER BY prefers the output name on a clash
# source: https://www.postgresql.org/docs/current/queries-order.html
# confirmed: a sort expression can be the label of an output column
# source: https://www.postgresql.org/docs/current/sql-select.html
# confirmed: the processing steps run FROM, WHERE, then the output (SELECT) expressions, then ORDER BY ("the returned rows are sorted"), then LIMIT
# source: https://www.postgresql.org/docs/current/tutorial-arch.html
# confirmed: "PostgreSQL uses a client/server model"
# source: https://en.wikipedia.org/wiki/Dhokla
# confirmed: dhokla is "a savoury sponge dish" made with a batter "steamed to a cake-like consistency", the batter mixes rice with Bengal gram, a variety of chickpea
# source: https://en.wikipedia.org/wiki/Khandvi_(food)
# confirmed: khandvi has "tightly rolled bite-sized pieces" and is "primarily made of gram flour and yogurt"
# source: https://en.wikipedia.org/wiki/Fafda
# confirmed: fafda is a snack of the Gujarat region
print("134 ok")
