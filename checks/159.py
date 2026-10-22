# checks for notes/159-left-join-keep-every-row-from-the-left-table.md
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT customer_id, name FROM customers WHERE customer_id IN (4, 5) ORDER BY 1") == [(4, 'Disha'), (5, 'Esha')]
assert q("SELECT order_id, customer_id FROM orders WHERE order_id = 105") == [(105, 4)]
# the python loop in the note
customers = [{"customer_id": 4, "name": "Disha"}, {"customer_id": 5, "name": "Esha"}]
orders = [{"order_id": 105, "customer_id": 4}]
out = []
for c in customers:
    found = False
    for o in orders:
        if o["customer_id"] == c["customer_id"]:
            out.append((c["name"], o["order_id"])); found = True
    if not found:
        out.append((c["name"], None))
assert out == [("Disha", 105), ("Esha", None)]
left = "SELECT c.name, o.order_id FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id ORDER BY c.name, o.order_id"
assert q(left) == [('Asha', 101), ('Asha', 103), ('Asha', 106), ('Bhavin', 102), ('Bhavin', 107), ('Chirag', 104), ('Disha', 105), ('Esha', None)]
assert len(q(left)) == 8
assert q("SELECT count(*) FROM orders o JOIN customers c ON c.customer_id = o.customer_id") == [(7,)]
assert 8 - 7 == 1
# swapping sides: every order has a customer, so 7
assert q("SELECT count(*) FROM orders o LEFT JOIN customers c ON c.customer_id = o.customer_id") == [(7,)]
assert q("SELECT count(*) FROM customers") == [(5,)]
# a sixth customer with no orders: 9 rows one way, 7 the other
six = "(SELECT * FROM customers UNION ALL SELECT 6, 'Farhan', NULL, DATE '2026-04-01')"
assert q(f"SELECT count(*) FROM {six} c LEFT JOIN orders o ON c.customer_id = o.customer_id") == [(9,)]
assert q(f"SELECT count(*) FROM orders o LEFT JOIN {six} c ON c.customer_id = o.customer_id") == [(7,)]
# Asha has 3 orders, so 3 rows; one row per customer needs GROUP BY
assert q("SELECT count(*) FROM orders WHERE customer_id = 1") == [(3,)]
assert q("SELECT count(*) FROM (SELECT c.customer_id FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id)") == [(5,)]
# source: https://www.postgresql.org/docs/current/queries-table-expressions.html
# confirmed: LEFT OUTER JOIN adds a row with null values in the right columns for each left row with no match, so there is at least one row per left row. the docs write [ INNER ] JOIN and LEFT [ OUTER ] JOIN in the syntax (OUTER optional) at https://www.postgresql.org/docs/current/sql-select.html
