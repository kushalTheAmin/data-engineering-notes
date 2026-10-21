# checks for notes/125-concatenating-text-and-taking-pieces-of-it.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
rows = q("SELECT name, city FROM customers ORDER BY customer_id")
assert len(rows) == 5
labels = [n + " from " + c if c is not None else None for n, c in rows]
assert labels == [r[0] for r in q("SELECT name || ' from ' || city FROM customers ORDER BY customer_id")]
assert labels[4] is None and rows[4] == ("Esha", None)
assert q("SELECT name || ' from ' || coalesce(city, '?') FROM customers WHERE name = 'Esha'") == [("Esha from ?",)]
# counting from 1 in SQL, from 0 in python
assert q("SELECT substr('dhokla', 2, 3)") == [("hok",)]
assert "dhokla"[1:4] == "hok"
assert list(enumerate("dhokla", 1)) == [(1, "d"), (2, "h"), (3, "o"), (4, "k"), (5, "l"), (6, "a")]
assert len("dhokla") == 6
# DuckDB concat skips nulls
assert q("SELECT concat('a', NULL, 'b')") == [("ab",)]
# source: https://www.postgresql.org/docs/current/functions-string.html
# confirmed: substring('Thomas' from 2 for 3) gives hom, start is the start'th character (first character is 1)
# confirmed: concat concatenates the text representations of all the arguments, NULL arguments are ignored
# source: https://en.wikipedia.org/wiki/Dhokla
# confirmed: dhokla is a savoury sponge dish steamed to a cake-like consistency (seen in the check for note 122)
assert q("SELECT name || ' from ' || coalesce(city, '?') AS label FROM customers WHERE name = 'Esha'") == [("Esha from ?",)]
