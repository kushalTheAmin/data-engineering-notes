# checks for notes/180-ctes-naming-each-step-with-with.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT count(*) FROM orders") == [(7,)]
assert q("WITH per_customer AS (SELECT customer_id, count(*) AS orders FROM orders GROUP BY customer_id) SELECT avg(orders) AS avg_orders FROM per_customer") == [(1.75,)]
# same value as the nested version in 175
assert q("SELECT avg(orders) AS avg_orders FROM (SELECT customer_id, count(*) AS orders FROM orders GROUP BY customer_id) AS per_customer") == [(1.75,)]
assert q("WITH per_customer AS (SELECT customer_id, count(*) AS orders FROM orders GROUP BY customer_id) SELECT c.name, p.orders FROM per_customer p JOIN customers c ON c.customer_id = p.customer_id WHERE p.orders > (SELECT avg(orders) FROM per_customer) ORDER BY c.name") == [("Asha", 3), ("Bhavin", 2)]
# check yourself
assert q("WITH orders AS (SELECT * FROM orders WHERE status = 'delivered') SELECT count(*) AS n FROM orders") == [(5,)]
assert q("WITH delivered AS (SELECT * FROM orders WHERE status = 'delivered') SELECT count(*) AS n FROM orders") == [(7,)]
# source: https://www.postgresql.org/docs/current/queries-with.html
# confirmed: WITH queries (CTEs) can be thought of as defining temporary tables that exist just for one query
# source: https://www.postgresql.org/docs/current/sql-select.html
# confirmed: "the WITH query hides any real table of the same name for the purposes of the primary query"
# the docs wording is hedged: "can be thought of as defining temporary tables", not "is a temporary table"
