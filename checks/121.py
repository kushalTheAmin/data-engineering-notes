# checks for notes/121-distinct-removing-duplicate-rows.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
cats = [r[0] for r in q("SELECT category FROM products")]
assert len(cats) == 6 and cats.count("snack") == 3
assert [r[0] for r in q("SELECT DISTINCT category FROM products ORDER BY category")] == ["drink", "snack", "sweet"]
pairs = q("SELECT customer_id, status FROM orders ORDER BY customer_id, status")
assert len(pairs) == 7
d = q("SELECT DISTINCT customer_id, status FROM orders ORDER BY customer_id, status")
assert len(d) == 5
assert len({r[0] for r in d}) == 4
assert d == sorted(set(pairs))
assert [r for r in d if r[0] == 1] == [(1, "delivered"), (1, "pending")]
assert q("SELECT NULL = NULL")[0][0] is None
assert len(q("SELECT DISTINCT x FROM (VALUES (NULL), (NULL)) t(x)")) == 1
# source: https://www.postgresql.org/docs/current/sql-select.html
# confirmed: SELECT DISTINCT removes all duplicate rows from the result; without ORDER BY rows come back in whatever order the system finds fastest to produce
assert len(set(cats)) == 3  # 6 category values, only 3 categories
# source: https://www.postgresql.org/docs/current/tutorial-arch.html
# confirmed: "In database jargon, PostgreSQL uses a client/server model."
