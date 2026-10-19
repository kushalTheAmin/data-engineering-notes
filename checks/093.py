# checks for notes/093-foreign-key.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
assert con.execute("SELECT order_id, customer_id FROM orders WHERE order_id IN (101,103,104) ORDER BY 1").fetchall() == [(101,1),(103,1),(104,3)]
assert con.execute("SELECT customer_id, name FROM customers WHERE customer_id IN (1,3) ORDER BY 1").fetchall() == [(1,'Asha'),(3,'Chirag')]
assert [r[0] for r in con.execute("SELECT order_id FROM orders WHERE customer_id = 1 ORDER BY 1").fetchall()] == [101,103,106]
assert con.execute("SELECT count(*) FROM customers WHERE customer_id = 1").fetchone()[0] == 1
# the shop file declares it with REFERENCES
sql = open(os.path.join(os.path.dirname(__file__), "..", "data", "shop.sql")).read()
assert "customer_id INTEGER NOT NULL REFERENCES customers (customer_id)" in sql
# source: https://learn.microsoft.com/en-us/ef/core/modeling/relationships/conventions
# confirmed: EF Core discovers a foreign key by name pattern <principal entity type name>Id (e.g. CustomerId), alongside a navigation to that type
# source: https://www.postgresql.org/docs/current/ddl-constraints.html
# confirmed: "A foreign key must reference columns that either are a primary key or form a unique constraint, or are columns from a non-partial unique index."
print("093 ok")
