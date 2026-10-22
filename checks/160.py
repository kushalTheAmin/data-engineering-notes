# checks for notes/160-the-nulls-a-left-join-creates.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# Esha has no orders; the left join keeps her as one row with a NULL order_id
assert q("SELECT count(*) FROM orders WHERE customer_id = 5") == [(0,)]
assert q("SELECT c.name, o.order_id FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id WHERE c.name = 'Esha'") == [('Esha', None)]
# order_id is the primary key of orders, so it is never NULL in the table itself
assert q("SELECT count(*) FROM orders WHERE order_id IS NULL") == [(0,)]
# the grouped query in the note
big = "SELECT c.name, count(*) AS rows_kept, count(o.order_id) AS orders FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.name ORDER BY c.name"
assert q(big) == [('Asha', 3, 3), ('Bhavin', 2, 2), ('Chirag', 1, 1), ('Disha', 1, 1), ('Esha', 1, 0)]
# only Esha disagrees
assert [r[0] for r in q(big) if r[1] != r[2]] == ['Esha']
# source: https://www.postgresql.org/docs/current/functions-aggregate.html
# confirmed: count(*) is the number of input rows; count(expression) is the number of input rows in which the value is not null
# source: https://www.postgresql.org/docs/current/ddl-constraints.html
# confirmed (as in checks/087): a primary key means unique and not null
