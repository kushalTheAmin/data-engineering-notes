# checks for notes/119-where-nulls-land-when-you-sort.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT name FROM customers ORDER BY city DESC")[-1][0] == "Esha"
assert q("SELECT name FROM customers ORDER BY city")[-1][0] == "Esha"
assert q("SELECT name FROM customers ORDER BY city NULLS FIRST, name")[0][0] == "Esha"
r = [x[0] for x in q("SELECT name FROM customers ORDER BY city DESC NULLS FIRST, name")]
assert r == ["Esha", "Asha", "Chirag", "Disha", "Bhavin"]
assert sum(1 for x in q("SELECT city FROM customers") if x[0] == "Jersey City") == 2
assert sum(1 for x in q("SELECT city FROM customers") if x[0] is None) == 1
# source: https://www.postgresql.org/docs/current/queries-order.html
# confirmed: nulls sort as if larger than any non-null value; NULLS FIRST is the default for DESC, NULLS LAST otherwise
# source: https://duckdb.org/docs/current/sql/query_syntax/orderby.html
# confirmed: DuckDB default is NULLS LAST, kept even for DESC, whereas PostgreSQL places NULLs first on DESC
