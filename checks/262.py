# checks for notes/262-denormalization-copying-data-on-purpose.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# 7 orders, so 7 lookups into customers
assert q("SELECT count(*) FROM orders") == [(7,)]
# the python block's dictionaries match the shop
assert q("SELECT customer_id, city FROM customers ORDER BY 1") == [(1, 'Jersey City'), (2, 'Edison'), (3, 'Jersey City'), (4, 'Hoboken'), (5, None)]
assert q("SELECT order_id, customer_id FROM orders ORDER BY 1") == [(101, 1), (102, 2), (103, 1), (104, 3), (105, 4), (106, 1), (107, 2)]
# Asha has 3 orders: 101, 103, 106
assert q("SELECT order_id FROM orders WHERE customer_id = 1 ORDER BY 1") == [(101,), (103,), (106,)]
assert q("SELECT count(*) FROM orders WHERE customer_id = 1") == [(3,)]
# source: https://docs.cloud.google.com/bigquery/docs/best-practices-performance-nested
# confirmed: BigQuery docs define denormalization as adding columns to one table to reduce or remove joins, recommend it to raise query performance, call extra storage generally a reasonable trade, and say it does not always help
assert q("SELECT count(*) FROM orders o JOIN customers c ON c.customer_id = o.customer_id WHERE c.city = 'Jersey City'") == [(4,)]
