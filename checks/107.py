# checks for notes/107-comparisons-equal-not-equal-bigger-smaller.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
prices = con.execute("SELECT name, price FROM products ORDER BY product_id").fetchall()
assert [n for n, p in prices if p >= 6] == ["dhokla", "khandvi", "kaju katli"]
assert [n for n, p in prices if p > 6] == ["khandvi", "kaju katli"]
assert dict(prices)["dhokla"] == 6
assert con.execute("SELECT name FROM products WHERE price >= 6").fetchall() == [("dhokla",), ("khandvi",), ("kaju katli",)]
assert con.execute("SELECT name FROM products WHERE price > 6").fetchall() == [("khandvi",), ("kaju katli",)]
# != is accepted as well as <>
assert con.execute("SELECT count(*) FROM products WHERE price != 6").fetchone()[0] == con.execute("SELECT count(*) FROM products WHERE price <> 6").fetchone()[0] == 5
# source: https://duckdb.org/docs/current/sql/expressions/comparison_operators
# confirmed: the table lists < > <= >=, "= or == equal" and "<> or != not equal"
# source: https://www.postgresql.org/docs/current/functions-comparison.html
# confirmed: Postgres lists <> as not equal and says != is an alias converted to <> early in parsing
assert con.execute("SELECT count(*) FROM customers WHERE city <> 'Jersey City'").fetchone()[0] == 2  # Esha (null city) fails <> too
assert con.execute("SELECT count(*) FROM customers WHERE city = 'Jersey City'").fetchone()[0] == 2
# a null column fails all six tests, so Esha (null city) is never kept
assert con.execute("SELECT count(*) FROM customers WHERE name = 'Esha' AND (city = 'a' OR city <> 'a' OR city > 'a' OR city < 'z' OR city >= 'a' OR city <= 'z')").fetchone()[0] == 0
# source: https://duckdb.org/docs/current/sql/expressions/comparison_operators
# confirmed: "Whenever either of the input arguments is NULL, the output of the comparison is NULL." and WHERE keeps only true rows (https://duckdb.org/docs/current/sql/query_syntax/where: "specifies any filters to apply to the data")
print("107 ok")
