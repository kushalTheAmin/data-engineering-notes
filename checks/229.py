# checks for notes/229-acid-four-promises-a-database-makes.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
def fails(s):
    try:
        con.execute(s)
    except Exception:
        return True
    return False
assert q("SELECT name FROM customers WHERE customer_id = 1") == [("Asha",)]
assert q("SELECT name FROM customers WHERE customer_id = 4") == [("Disha",)]
assert q("SELECT name FROM customers WHERE customer_id = 5") == [("Esha",)]
# orders are 7 in the shop, so one extra in flight reads 8 and a recount 7
assert q("SELECT count(*) FROM orders") == [(7,)]
# a price of 600.00 passes CHECK (price > 0), -5.00 does not
con.execute("CREATE TABLE my_products (product_id INTEGER PRIMARY KEY, name VARCHAR NOT NULL, price DECIMAL(6, 2) CHECK (price > 0))")
con.execute("INSERT INTO my_products SELECT product_id, name, price FROM products")
assert not fails("INSERT INTO my_products VALUES (8, 'big tray', 600.00)")
con.execute("DELETE FROM my_products WHERE product_id = 8")
assert fails("INSERT INTO my_products VALUES (7, 'imarti', -5.00)")
assert q("SELECT count(*) FROM my_products") == [(6,)]
# source: https://www.postgresql.org/docs/current/tutorial-transactions.html
#   confirmed: "A transaction is said to be atomic ... either happens completely or not at all"; once completed and acknowledged it "won't be lost even if a crash ensues"; updates are logged on disk before the transaction is reported complete
# source: https://www.postgresql.org/docs/current/transaction-iso.html
#   confirmed: "Read Committed is the default isolation level in PostgreSQL" (Serializable is the strictest level)
