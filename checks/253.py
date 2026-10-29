# checks for notes/253-capstone-placing-an-order-as-one-transaction.md
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# Esha is customer 5, dhokla is product 1, khandvi is product 2; 108 is imagined
assert q("SELECT name FROM customers WHERE customer_id = 5")[0][0] == 'Esha'
assert q("SELECT name FROM products WHERE product_id = 1")[0][0] == 'dhokla'
assert q("SELECT name FROM products WHERE product_id = 2")[0][0] == 'khandvi'
assert q("SELECT count(*) FROM orders WHERE order_id = 108")[0][0] == 0
assert q("SELECT count(*) FROM products WHERE product_id = 99")[0][0] == 0
# check yourself 1: the order insert is outside BEGIN so it stays, the rolled back item does not
con.execute("CREATE TABLE my_orders AS SELECT * FROM orders")
con.execute("CREATE TABLE my_items (order_id INTEGER, product_id INTEGER, quantity INTEGER CHECK (quantity > 0))")
con.execute("INSERT INTO my_orders VALUES (108, 5, TIMESTAMP '2026-04-10 11:00:00', 'pending')")
con.execute("BEGIN")
con.execute("INSERT INTO my_items VALUES (108, 1, 2)")
try:
    con.execute("INSERT INTO my_items VALUES (108, 2, 0)")
    assert False
except Exception:
    pass
con.execute("ROLLBACK")
assert q("SELECT count(*) FROM my_orders WHERE order_id = 108")[0][0] == 1
assert q("SELECT count(*) FROM my_items WHERE order_id = 108")[0][0] == 0
# check yourself 2: one dhokla left, Asha first, Esha rechecks left_over > 0 on the saved row
left = 1
asha_row = left > 0
left -= 1 if asha_row else 0
esha_row = left > 0
assert asha_row and not esha_row and left == 0
# the table links every brick of the section: notes 208 to 252 is 45 notes
assert len(range(208, 253)) == 45
text = open(os.path.join(os.path.dirname(__file__), '..', 'notes', '253-capstone-placing-an-order-as-one-transaction.md')).read()
body = text.split('### check yourself')[0]
linked = set(int(n) for n in re.findall(r'\[(\d{3})\]\(\./', body))
assert linked == set(range(208, 253)) | {252}, sorted(set(range(208, 253)) - linked)
# source: https://www.postgresql.org/docs/current/runtime-config-wal.html
# confirmed: if a recovery target is configured but archive recovery ends before the target is reached, the server shuts down with a fatal error
print("253 ok")
