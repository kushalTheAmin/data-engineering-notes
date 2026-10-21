# checks for notes/124-text-functions-lower-upper-length-and-trim.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
rows = q("SELECT signup_id, typed_name FROM signups ORDER BY signup_id")
assert len(rows) == 4
assert [len(n) for _, n in rows] == [4, 7, 7, 5]
assert [len(n.strip()) for _, n in rows] == [4, 6, 6, 5]
assert [(i, n.strip().lower(), n.strip().upper()) for i, n in rows] == q(
    "SELECT signup_id, lower(trim(typed_name)), upper(trim(typed_name)) FROM signups ORDER BY signup_id")
assert [r[0] for r in rows if r[1].endswith(" ")] == [2, 3]
assert q("SELECT signup_id FROM signups WHERE typed_name = 'CHIRAG'") == []
assert q("SELECT signup_id FROM signups WHERE lower(trim(typed_name)) = 'chirag'") == [(3,)]
# trim removes only spaces by default in DuckDB: a tab survives
assert q("SELECT length(trim(chr(9) || 'x'))") == [(2,)]
# length counts characters, strlen counts bytes
assert q("SELECT length('ગ'), strlen('ગ')") == [(1, 3)]
assert len("ગ") == 1 and len("ગ".encode()) == 3
# source: https://www.postgresql.org/docs/current/functions-string.html
# confirmed: btrim removes the longest string containing only characters in characters (a space by default) from the start and end of string
