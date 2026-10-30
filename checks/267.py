# checks for notes/267-schemas-as-namespaces-folders-for-tables.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
q = lambda con, s: con.execute(s).fetchall()
con = shop()
# the shop has 7 orders, all in the default schema main
assert q(con, "SELECT count(*) FROM main.orders") == [(7,)]
assert q(con, "SELECT current_schema()") == [("main",)]
con.execute("CREATE SCHEMA archive")
con.execute("CREATE TABLE archive.orders AS SELECT * FROM orders WHERE order_id < 103")
# two tables named orders, one per folder; the bare name goes to main
assert q(con, "SELECT 'main.orders' AS full_name, count(*) AS n FROM main.orders UNION ALL SELECT 'archive.orders', count(*) FROM archive.orders UNION ALL SELECT 'orders', count(*) FROM orders") == [("main.orders", 7), ("archive.orders", 2), ("orders", 7)]
assert q(con, "SELECT order_id FROM archive.orders ORDER BY order_id") == [(101,), (102,)]
# USE moves the current folder, so the bare name now means archive.orders
con.execute("USE archive")
assert q(con, "SELECT current_schema()") == [("archive",)]
assert q(con, "SELECT count(*) AS n FROM orders") == [(2,)]
# the main one is still reachable by its full name: a folder is not a wall
assert q(con, "SELECT count(*) FROM main.orders") == [(7,)]
# the Postgres schemas page confirms:
# source: https://www.postgresql.org/docs/current/ddl-schemas.html
#  a database contains one or more named schemas which contain tables; the same object name can be used in different schemas without conflict; the search path is a list of schemas, first match wins, default "$user", public; tables go in public by default; schemas are not rigidly separated, a user can access objects in any schema they have privileges for; reasons: many users in one database, logical groups, third party apps avoiding name collisions
# the DuckDB USE page confirms:
# source: https://duckdb.org/docs/2.0/sql/statements/use.html
#  USE sets a default database, schema, or database/schema combination for future operations, and USE memory uses the main schema implicitly
# no DuckDB page states a fallback to main for bare table names, so the note does not claim one (it works in 1.5.6, but unsourced)
# source: https://www.postgresql.org/docs/current/sql-commands.html
# confirmed: the list of SQL commands has no USE (the U commands are UNLISTEN and UPDATE)
assert q(con, "SELECT count(*) FROM customers") == [(5,)]
