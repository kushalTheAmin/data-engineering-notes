# checks for notes/120-limit-and-offset-paging-through-rows.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert [r[0] for r in q("SELECT name FROM products ORDER BY price DESC LIMIT 2")] == ["kaju katli", "khandvi"]
assert [r[0] for r in q("SELECT name FROM products ORDER BY price DESC LIMIT 2 OFFSET 2")] == ["dhokla", "jalebi"]
assert [r[0] for r in q("SELECT name FROM products ORDER BY price DESC LIMIT 2 OFFSET 4")] == ["fafda", "masala chai"]
rows = [r[0] for r in q("SELECT name FROM products ORDER BY price DESC")]
assert rows[2:4] == ["dhokla", "jalebi"]
size = 2
assert [(n - 1) * size for n in (1, 2, 3)] == [0, 2, 4]
assert len(q("SELECT name FROM products ORDER BY price DESC LIMIT 10")) == 6
# source: https://www.postgresql.org/docs/current/queries-limit.html
# confirmed: "no more than that many rows will be returned (but possibly fewer, if the query itself yields fewer rows)"
# confirmed: LIMIT without ORDER BY gives an unpredictable subset; rows skipped by OFFSET still have to be computed, so a large OFFSET might be inefficient
