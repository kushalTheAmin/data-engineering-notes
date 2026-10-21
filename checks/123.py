# checks for notes/123-case-when-if-and-else-inside-a-query.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
from decimal import Decimal
con = shop()
q = lambda s: con.execute(s).fetchall()
prods = q("SELECT name, price FROM products ORDER BY product_id")
def tier(p):
    if p < 5:
        return "cheap"
    elif p < 8:
        return "regular"
    else:
        return "treat"
assert q("SELECT name, price, CASE WHEN price < 5 THEN 'cheap' WHEN price < 8 THEN 'regular' ELSE 'treat' END AS tier FROM products ORDER BY product_id") == [(n, p, tier(p)) for n, p in prods]
assert tier(Decimal("5.00")) == "regular"
assert [r[1] for r in q("SELECT name, CASE WHEN price < 5 THEN 'cheap' END AS tier FROM products ORDER BY product_id")] == [None, None, None, None, "cheap", "cheap"]
assert q("SELECT name, CASE WHEN price < 8 THEN 'regular' WHEN price < 5 THEN 'cheap' ELSE 'treat' END AS tier FROM products WHERE name IN ('masala chai', 'fafda') ORDER BY product_id") == [("masala chai", "regular"), ("fafda", "regular")]
assert q("SELECT name, CASE WHEN city = 'Jersey City' THEN 'local' ELSE 'far' END AS area FROM customers WHERE name IN ('Bhavin', 'Esha') ORDER BY customer_id") == [("Bhavin", "far"), ("Esha", "far")]
assert q("SELECT city = 'Jersey City' FROM customers WHERE name = 'Esha'") == [(None,)]
# source: https://www.postgresql.org/docs/current/functions-conditional.html
# confirmed: CASE is similar to if/else; the first true condition wins and the rest is not processed; with no ELSE and no true condition the result is null
# source: https://www.postgresql.org/docs/current/features-sql-standard.html
# confirmed: the list of SQL standard features Postgres supports has "F261 Core CASE expression" with "F261-02 Core Searched CASE", so CASE WHEN is standard SQL
