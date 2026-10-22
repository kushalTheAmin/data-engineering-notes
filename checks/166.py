# checks for notes/166-joining-on-columns-that-can-be-null.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# source: https://www.postgresql.org/docs/current/functions-comparison.html
# confirmed: IS NOT DISTINCT FROM is true for two nulls and never returns null, and = yields null with a null input
assert None == None
assert q("SELECT NULL = NULL") == [(None,)] and q("SELECT NULL IS NOT DISTINCT FROM NULL") == [(True,)]
assert q("SELECT count(*) FROM customers WHERE city IS NULL") == [(1,)] and q("SELECT name FROM customers WHERE city IS NULL") == [("Esha",)]
assert q("SELECT count(*) FROM customers c JOIN delivery_zones z ON c.city = z.city") == [(4,)]
assert q("SELECT count(*) FROM customers c JOIN delivery_zones z ON c.city IS NOT DISTINCT FROM z.city") == [(5,)]
assert q("SELECT count(*) FROM orders o JOIN customers c ON o.customer_id = c.customer_id") == [(7,)]
assert q("SELECT c.name, z.zone FROM customers c LEFT JOIN delivery_zones z ON c.city = z.city WHERE c.name = 'Esha'") == [("Esha", None)]
# python loop from the note
cities = [("Asha", "Jersey City"), ("Esha", None)]
zones = [("Jersey City", "east"), (None, "no city")]
assert [(n, zn) for n, c in cities for z, zn in zones if c == z] == [("Asha", "east"), ("Esha", "no city")]
assert q("SELECT count(z.zone), count(*) FROM customers c LEFT JOIN delivery_zones z ON c.city = z.city") == [(4, 5)]
