# checks for notes/112-between-ranges-that-include-both-ends.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda t, w, c="name": [r[0] for r in con.execute(f"SELECT {c} FROM {t} WHERE " + w).fetchall()]
assert len(con.execute("SELECT 1 FROM products").fetchall()) == 6
assert q("products", "price BETWEEN 4.50 AND 6.00") == ["dhokla", "jalebi", "fafda"]
assert q("products", "price BETWEEN 4.50 AND 6.00") == q("products", "price >= 4.50 AND price <= 6.00")
prices = dict(con.execute("SELECT name, price FROM products").fetchall())
assert str(prices["dhokla"]) == "6.00" and str(prices["fafda"]) == "4.50"
assert q("products", "price NOT BETWEEN 4.50 AND 6.00") == ["khandvi", "kaju katli", "masala chai"]
assert len(q("products", "price NOT BETWEEN 4.50 AND 6.00")) == 3
assert q("orders", "ordered_at BETWEEN '2026-04-01' AND '2026-04-03'", "order_id") == [101, 102]
assert q("orders", "ordered_at >= '2026-04-01' AND ordered_at < '2026-04-04'", "order_id") == [101, 102, 103]
assert str(con.execute("SELECT ordered_at FROM orders WHERE order_id = 103").fetchone()[0]) == "2026-04-03 12:05:00"
assert q("customers", "joined_on BETWEEN DATE '2026-02-11' AND DATE '2026-03-02'") == ["Chirag", "Disha"]
assert list(range(1, 3)) == [1, 2]
# source: https://www.postgresql.org/docs/current/functions-comparison.html
# confirmed: a BETWEEN b AND c is equivalent to a >= b AND a <= c, so both ends are included; NOT BETWEEN is the negation
# source: https://duckdb.org/docs/current/sql/expressions/comparison_operators
# confirmed: DuckDB supports BETWEEN and NOT BETWEEN with the same meaning
assert con.execute("SELECT TIMESTAMP '2026-04-03' = TIMESTAMP '2026-04-03 00:00:00', (SELECT ordered_at FROM orders WHERE order_id = 103) > TIMESTAMP '2026-04-03'").fetchone() == (True, True)
# same fact as note 027 (a date compared to a timestamp becomes midnight); no docs page states it in words, so the assert above is the proof
assert q("products", "price BETWEEN 6.00 AND 4.50") == []
# source: https://www.postgresql.org/docs/current/functions-comparison.html
# confirmed: BETWEEN does not swap the ends, so a low end above the high end gives an empty range (the low end goes first)
# source: https://en.wikipedia.org/wiki/Fafda
# confirmed: "a popular Indian snack native to the western state of Gujarat", made from gram flour and deep-fried till crispy
print("112 ok")
