# checks for notes/259-first-normal-form-one-value-per-cell.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# 5 products have 2 tags, chai has none, so 10 rows
assert q("SELECT count(*) FROM product_tags WHERE len(tags) = 2") == [(5,)]
assert q("SELECT len(tags) FROM product_tags WHERE product_id = 5") == [(0,)]
assert q("SELECT count(*) FROM (SELECT UNNEST(tags) FROM product_tags)") == [(10,)]
assert 5 * 2 + 0 == 10 and 6 * 2 == 12
# savory products are 1, 2 and 6
assert q("SELECT product_id FROM (SELECT product_id, UNNEST(tags) AS tag FROM product_tags) WHERE tag = 'savory' ORDER BY 1") == [(1,), (2,), (6,)]
# a list can hold savory twice, a table keyed on (product_id, tag) refuses the repeat
assert q("SELECT len(['savory', 'savory'])") == [(2,)]
con.execute("CREATE TABLE pt (product_id INTEGER, tag VARCHAR, PRIMARY KEY (product_id, tag))")
con.execute("INSERT INTO pt VALUES (3, 'fried')")
try:
    con.execute("INSERT INTO pt VALUES (3, 'fried')")
    raise SystemExit("repeat was accepted")
except Exception as e:
    assert "Constraint" in type(e).__name__
con.execute("INSERT INTO pt VALUES (3, 'sweet')")
# source: https://www.postgresql.org/docs/16/arrays.html
# confirmed: tip says searching for specific array elements can be a sign of database misdesign, consider a separate table with a row for each item
