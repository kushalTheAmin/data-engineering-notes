# checks for notes/158-table-aliases-short-nicknames-for-tables.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the quoted ON line includes the word ON
assert len("ON orders.customer_id = customers.customer_id") == 45 and len("orders.customer_id = customers.customer_id") == 42
assert len("ON o.customer_id = c.customer_id") == 32
assert q("SELECT o.order_id, c.name, c.city FROM orders o JOIN customers c ON o.customer_id = c.customer_id ORDER BY o.order_id LIMIT 3") == [(101, 'Asha', 'Jersey City'), (102, 'Bhavin', 'Edison'), (103, 'Asha', 'Jersey City')]
# AS is optional
assert q("SELECT o.order_id FROM orders AS o ORDER BY 1 LIMIT 1") == q("SELECT o.order_id FROM orders o ORDER BY 1 LIMIT 1")
try:
    con.execute("SELECT orders.order_id FROM orders o JOIN customers c ON o.customer_id = c.customer_id")
    raise SystemExit("should fail")
except Exception as e:
    assert 'Referenced table "orders" not found' in str(e) and 'Candidate tables: "o"' in str(e)
# source: https://www.postgresql.org/docs/current/queries-table-expressions.html
# confirmed: "it is not allowed to refer to the table by the original name elsewhere in the query", and aliases are necessary when joining a table to itself. the same page says "The AS key word is optional noise" for table aliases
# source: https://www.postgresql.org/docs/current/tutorial-arch.html
# confirmed: "PostgreSQL uses a client/server model." (the note calls Postgres a server database)
