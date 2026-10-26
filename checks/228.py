# checks for notes/228-commit-and-rollback-keeping-or-undoing-a-transaction.md
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
def counts(n):
    return q(f"SELECT (SELECT count(*) FROM my_orders WHERE order_id = {n}), (SELECT count(*) FROM my_items WHERE order_id = {n})")
con.execute("CREATE TABLE my_orders AS SELECT * FROM orders")
con.execute("CREATE TABLE my_items (order_id INTEGER, product_id INTEGER REFERENCES products (product_id), quantity INTEGER)")
con.execute("INSERT INTO my_items SELECT * FROM order_items")
assert q("SELECT name FROM customers WHERE customer_id = 4") == [("Disha",)]
assert q("SELECT name FROM customers WHERE customer_id = 5") == [("Esha",)]
assert q("SELECT name FROM products WHERE product_id = 1") == [("dhokla",)]
assert q("SELECT count(*) FROM products WHERE product_id = 99") == [(0,)]
# rollback: both rows visible inside, both gone after
con.execute("BEGIN")
con.execute("INSERT INTO my_orders VALUES (108, 4, TIMESTAMP '2026-04-10 11:00:00', 'pending')")
con.execute("INSERT INTO my_items VALUES (108, 1, 2)")
assert counts(108) == [(1, 1)]
con.execute("ROLLBACK")
assert counts(108) == [(0, 0)]
# same steps ending in COMMIT keep both rows
con.execute("BEGIN")
con.execute("INSERT INTO my_orders VALUES (108, 4, TIMESTAMP '2026-04-10 11:00:00', 'pending')")
con.execute("INSERT INTO my_items VALUES (108, 1, 2)")
con.execute("COMMIT")
assert counts(108) == [(1, 1)]
# question 1: ROLLBACK after COMMIT has nothing to undo
con.execute("BEGIN")
con.execute("INSERT INTO my_orders VALUES (109, 4, TIMESTAMP '2026-04-10 12:00:00', 'pending')")
con.execute("INSERT INTO my_items VALUES (109, 1, 1)")
con.execute("COMMIT")
assert fails("ROLLBACK")
assert counts(109) == [(1, 1)]
# question 2: a failed insert aborts the transaction in DuckDB, COMMIT then rolls back
con.execute("BEGIN")
con.execute("INSERT INTO my_orders VALUES (110, 5, TIMESTAMP '2026-04-10 13:00:00', 'pending')")
assert fails("INSERT INTO my_items VALUES (110, 99, 1)")
assert fails("INSERT INTO my_items VALUES (110, 1, 1)")
con.execute("COMMIT")
assert counts(110) == [(0, 0)]
# autocommit: with no BEGIN each statement is kept on its own
con.execute("INSERT INTO my_orders VALUES (111, 1, TIMESTAMP '2026-04-10 14:00:00', 'pending')")
assert counts(111) == [(1, 0)]
# source: https://www.postgresql.org/docs/current/tutorial-transactions.html
# confirmed: a transaction is set up by surrounding the commands with BEGIN and COMMIT; ROLLBACK instead cancels all updates so far; without BEGIN each statement has an implicit BEGIN and COMMIT wrapped around it; updates of an open transaction are invisible to other transactions until it completes, then all become visible simultaneously
