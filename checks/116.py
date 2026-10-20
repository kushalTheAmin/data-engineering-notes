# checks for notes/116-coalesce-a-fallback-when-a-value-is-null.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
def coalesce(*values):
    for v in values:
        if v is not None:
            return v
    return None
cities = [r[0] for r in con.execute("SELECT city FROM customers ORDER BY customer_id").fetchall()]
assert cities == ["Jersey City", "Edison", "Jersey City", "Hoboken", None]
assert len(cities) == 5
assert [coalesce(c, "unknown") for c in cities] == ["Jersey City", "Edison", "Jersey City", "Hoboken", "unknown"]
assert coalesce(None, None) is None
assert coalesce(None, None, "c") == "c"
assert con.execute("SELECT COALESCE(city, 'unknown') FROM customers WHERE customer_id = 5").fetchone()[0] == "unknown"
assert con.execute("SELECT city FROM customers WHERE customer_id = 5").fetchone()[0] is None
r = con.execute("SELECT avg(stars), avg(COALESCE(stars, 0)) FROM order_ratings").fetchone()
assert r == (4.0, 2.4)
st = [x[0] for x in con.execute("SELECT stars FROM order_ratings").fetchall()]
assert len(st) == 5 and st.count(None) == 2
assert sum(s for s in st if s is not None) == 12
assert 12 / 3 == 4.0 and 12 / 5 == 2.4
# source: https://www.postgresql.org/docs/current/functions-conditional.html
# confirmed: COALESCE returns the first non-null argument, null only if all are null; often used to substitute a default for null when data is retrieved for display; "This SQL-standard function"
print("116 ok")
