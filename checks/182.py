# checks for notes/182-union-and-union-all.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT count(*) FROM orders") == [(7,)]
assert q("SELECT count(*) FROM orders WHERE status = 'delivered'") == [(5,)]
assert q("SELECT count(*) FROM orders WHERE status <> 'delivered'") == [(2,)]
assert q("SELECT customer_id FROM orders WHERE status = 'delivered' UNION ALL SELECT customer_id FROM orders WHERE status <> 'delivered' ORDER BY customer_id") == [(1,), (1,), (1,), (2,), (2,), (3,), (4,)]
assert q("SELECT customer_id FROM orders WHERE status = 'delivered' UNION SELECT customer_id FROM orders WHERE status <> 'delivered' ORDER BY customer_id") == [(1,), (2,), (3,), (4,)]
a = [1, 2, 1, 4, 2]
b = [3, 1]
assert len(a + b) == 7 and sorted(set(a + b)) == [1, 2, 3, 4]
assert q("SELECT count(*) FROM orders WHERE customer_id = 1") == [(3,)]
# check yourself 1
assert q("SELECT name FROM products WHERE category = 'snack' ORDER BY name") == [('dhokla',), ('fafda',), ('khandvi',)]
assert q("SELECT name FROM products WHERE price < 6 ORDER BY name") == [('fafda',), ('jalebi',), ('masala chai',)]
assert q("SELECT price FROM products WHERE name = 'dhokla'") == [(6,)]
assert q("SELECT count(*) FROM (SELECT name FROM products WHERE category = 'snack' UNION SELECT name FROM products WHERE price < 6)") == [(5,)]
assert 3 + 3 - 1 == 5
# check yourself 2
assert q("SELECT name, city FROM customers WHERE customer_id = 1 UNION ALL SELECT city, name FROM customers WHERE customer_id = 1") == [('Asha', 'Jersey City'), ('Jersey City', 'Asha')]
try:
    con.execute("SELECT name, city FROM customers UNION SELECT name FROM customers")
    assert False
except Exception as e:
    assert "same number of result columns" in str(e)
# source: https://www.postgresql.org/docs/current/sql-select.html
# confirmed: operands must produce the same number of columns with compatible types; no duplicates unless ALL; "UNION ALL is usually significantly quicker than UNION"
# source: https://www.postgresql.org/docs/current/queries-union.html
# confirmed: UNION effectively appends query2 to query1 and eliminates duplicate rows in the same way as DISTINCT unless UNION ALL is used
# columns line up by position and the result names come from the first query (checked above: name | city, row two puts a city under name)
assert [d[0] for d in con.execute("SELECT name, city FROM customers WHERE customer_id = 1 UNION ALL SELECT city, name FROM customers WHERE customer_id = 1").description] == ["name", "city"]
# DuckDB also has a separate UNION BY NAME that matches by name
assert q("SELECT name, city FROM customers WHERE customer_id = 1 UNION ALL BY NAME SELECT city, name FROM customers WHERE customer_id = 1") == [('Asha', 'Jersey City'), ('Asha', 'Jersey City')]
# source: https://duckdb.org/docs/2.0/sql/query_syntax/setops
# confirmed: "Traditional set operations unify queries by column position, and require the to-be-combined queries to have the same number of input columns. ... The result will use the column names from the first query. DuckDB also supports UNION [ALL] BY NAME, which joins columns by name instead of by position."
# source: https://www.postgresql.org/docs/current/sql-select.html
# confirmed: "ALL prevents elimination of duplicates. (Therefore, UNION ALL is usually significantly quicker than UNION; use ALL when you can.)"
