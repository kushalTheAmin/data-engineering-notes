# checks for notes/110-not-flipping-a-condition.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda t, w: [r[0] for r in con.execute("SELECT name FROM " + t + " WHERE " + w).fetchall()]
assert len(con.execute("SELECT 1 FROM customers").fetchall()) == 5
rows = con.execute("SELECT name, city FROM customers ORDER BY customer_id").fetchall()
assert rows[4] == ("Esha", None)
assert [n for n, c in rows if not c == "Jersey City"] == ["Bhavin", "Disha", "Esha"]
assert q("customers", "NOT city = 'Jersey City'") == ["Bhavin", "Disha"]
assert len([n for n, c in rows if c != "Jersey City" and c is not None]) == 2
assert len([n for n, c in rows if c == "Jersey City"]) == 2
assert q("customers", "city <> 'Jersey City'") == ["Bhavin", "Disha"]
assert q("products", "price <> 6") == q("products", "NOT price = 6")
assert q("products", "NOT category = 'snack' AND price < 6") == ["jalebi", "masala chai"]
whole = q("products", "NOT (category = 'snack' AND price < 6)")
assert len(whole) == 5 and "fafda" not in whole
slice_ = ["dhokla", "jalebi", "kaju katli", "masala chai", "fafda"]  # the 5 products the question lists
assert len([n for n in whole if n in slice_]) == 4
assert con.execute("SELECT count(*) FROM customers WHERE city = 'Jersey City' OR NOT city = 'Jersey City'").fetchone()[0] == 4
# source: https://www.postgresql.org/docs/current/sql-syntax-lexical.html
# confirmed: operator precedence table lists NOT above AND, and AND above OR
# source: https://www.postgresql.org/docs/current/functions-logical.html
# confirmed: SQL uses three-valued logic with true, false and null, where null represents unknown
assert con.execute("SELECT (NOT (NULL = 1)) IS NULL, (NULL OR NULL) IS NULL").fetchone() == (True, True)
# source: https://www.postgresql.org/docs/current/queries-table-expressions.html
# confirmed: "If the result of the condition is true, the row is kept in the output table, otherwise (i.e., if the result is false or null) it is discarded."
# source: https://duckdb.org/docs/current/sql/expressions/logical_operators
# confirmed: truth tables give NOT NULL as NULL and NULL OR NULL as NULL
print("110 ok")
