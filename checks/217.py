# checks for notes/217-check-a-rule-every-value-must-pass.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
from decimal import Decimal
con = shop()
q = lambda s: con.execute(s).fetchall()
def refused(sql):
    try:
        con.execute(sql)
    except Exception as e:
        return "check constraint failed" in str(e).lower()
    return False
con.execute("CREATE TABLE price_list (name VARCHAR NOT NULL, price DECIMAL(6, 2) CHECK (price > 0))")
con.execute("INSERT INTO price_list VALUES ('dhokla', 6.00), ('jalebi', 5.00), ('fafda', NULL)")
assert q("SELECT * FROM price_list") == [("dhokla", Decimal("6.00")), ("jalebi", Decimal("5.00")), ("fafda", None)]
# the table of five prices: 6.00 and 5.00 stored, NULL stored, 0 and -7.50 refused
assert refused("INSERT INTO price_list VALUES ('khandvi', -7.50)")
assert refused("INSERT INTO price_list VALUES ('chai', 0)")
assert q("SELECT count(*) FROM price_list") == [(3,)]
# check yourself 1
con.execute("CREATE TABLE stock (product VARCHAR, quantity INTEGER CHECK (quantity >= 0))")
con.execute("INSERT INTO stock VALUES ('dhokla', 0), ('jalebi', NULL)")
assert q("SELECT count(*), count(quantity) FROM stock") == [(2, 1)]
# check yourself 2: seven orders, only 104 is neither pending nor delivered
assert q("SELECT count(*) FROM orders") == [(7,)]
assert q("SELECT order_id, status FROM orders WHERE NOT (status IN ('pending', 'delivered'))") == [(104, "cancelled")]
# source: https://www.postgresql.org/docs/current/ddl-constraints.html
#   confirmed (opened this run): a check constraint is satisfied if the expression evaluates to true or the null value; NOT NULL is needed to block nulls.
assert q("SELECT status, count(*) FROM orders GROUP BY status ORDER BY status") == [("cancelled", 1), ("delivered", 5), ("pending", 1)]
