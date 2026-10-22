# checks for notes/156-inner-join-traced-by-hand.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT customer_id FROM orders WHERE order_id = 105") == [(4,)]
cust = q("SELECT customer_id, name, city FROM customers ORDER BY 1")
assert [(c[0], c[1]) for c in cust] == [(1, 'Asha'), (2, 'Bhavin'), (3, 'Chirag'), (4, 'Disha'), (5, 'Esha')]
assert cust[3] == (4, 'Disha', 'Hoboken')
assert sum(1 for c in cust if c[0] == 4) == 1 and len(cust) - 1 == 4
n_orders, n_cust = q("SELECT count(*) FROM orders")[0][0], len(cust)
assert (n_orders, n_cust, n_orders * n_cust) == (7, 5, 35)
assert q("SELECT count(*) FROM orders, customers") == [(35,)]
assert q("SELECT count(*) FROM orders JOIN customers ON orders.customer_id = customers.customer_id") == [(7,)]
assert 35 - 7 == 28
assert q("SELECT DISTINCT customers.name FROM customers JOIN orders ON customers.customer_id = orders.customer_id ORDER BY 1") == [('Asha',), ('Bhavin',), ('Chirag',), ('Disha',)]
assert q("SELECT count(*) FROM orders JOIN customers ON orders.customer_id = customers.customer_id WHERE customers.city = 'Jersey City'") == [(4,)]
assert q("SELECT count(*) FROM customers WHERE city = 'Jersey City'") == [(2,)]
assert q("SELECT count(*) FROM orders WHERE customer_id = 1") == [(3,)] and q("SELECT count(*) FROM orders WHERE customer_id = 3") == [(1,)]
assert 7 * (5 + 1) == 42
assert q("SELECT count(*) FROM orders JOIN (SELECT * FROM customers UNION ALL SELECT 6, 'Farhan', NULL, DATE '2026-04-01') c ON orders.customer_id = c.customer_id") == [(7,)]
# DuckDB: plain JOIN and INNER JOIN give the same rows
assert q("SELECT o.order_id, c.name FROM orders o JOIN customers c ON o.customer_id = c.customer_id ORDER BY 1") == q("SELECT o.order_id, c.name FROM orders o INNER JOIN customers c ON o.customer_id = c.customer_id ORDER BY 1")
# source: https://www.postgresql.org/docs/current/sql-select.html
# confirmed: join_type is "[ INNER ] JOIN", so INNER is optional and plain JOIN is the inner join
# source: https://duckdb.org/docs/2.0/sql/query_syntax/from.html
# confirmed: "A join that is not OUTER is INNER (only rows that get paired are returned)", and its example writes a plain JOIN
