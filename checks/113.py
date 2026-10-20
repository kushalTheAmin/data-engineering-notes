# checks for notes/113-like-matching-text-patterns.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda t, w, c="name": [r[0] for r in con.execute(f"SELECT {c} FROM {t} WHERE " + w).fetchall()]
names = q("products", "TRUE")
assert len(names) == 6
assert q("products", "name LIKE 'k%'") == [n for n in names if n.startswith("k")] == ["khandvi", "kaju katli"]
assert q("products", "name LIKE '%a'") == [n for n in names if n.endswith("a")] == ["dhokla", "fafda"]
assert q("products", "name LIKE '%ch%'") == [n for n in names if "ch" in n] == ["masala chai"]
assert q("products", "name LIKE 'k_a%'") == ["khandvi"]
assert "kaju katli"[2] == "j"
assert q("products", "name LIKE 'K%'") == []
assert q("products", "name ILIKE 'K%'") == ["khandvi", "kaju katli"]
assert q("customers", "city NOT LIKE 'J%'") == ["Bhavin", "Disha"]
assert con.execute("SELECT city FROM customers WHERE name = 'Esha'").fetchone()[0] is None
# source: https://www.postgresql.org/docs/current/functions-matching.html
# confirmed: _ matches any single character, % any sequence of zero or more characters; ILIKE is the case-insensitive form
# source: https://duckdb.org/docs/current/sql/functions/pattern_matching
# confirmed: DuckDB LIKE uses the same _ and % wildcards, and ILIKE matches case-insensitively
# source: https://en.wikipedia.org/wiki/Khandvi_(food)
# confirmed: khandvi is a savory snack of Gujarati cuisine whose main ingredient is gram flour (page: Khandvi (food))
print("113 ok")
