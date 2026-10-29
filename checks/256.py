# checks for notes/256-one-to-one-when-two-tables-share-a-key.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT c.name, k.phone FROM customers c LEFT JOIN customer_contacts k ON k.customer_id = c.customer_id ORDER BY c.customer_id") == [('Asha', '555-0101'), ('Bhavin', '555-0102'), ('Chirag', None), ('Disha', '555-0104'), ('Esha', None)]
# 5 customers in, 5 rows out; Chirag and Esha (2 of 5) have no contact row
assert q("SELECT count(*) FROM customers c LEFT JOIN customer_contacts k ON k.customer_id = c.customer_id") == [(5,)]
assert q("SELECT count(*) FROM customers WHERE customer_id NOT IN (SELECT customer_id FROM customer_contacts)") == [(2,)]
# joining customers to orders gives 8 rows, Asha repeats 3 times
assert q("SELECT count(*) FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id") == [(8,)]
assert q("SELECT count(*) FROM orders WHERE customer_id = 1") == [(3,)]
# an inner join gives only 7 rows, so the 8 needs the left join (7 orders plus Esha with none)
assert q("SELECT count(*) FROM customers c JOIN orders o ON o.customer_id = c.customer_id") == [(7,)]
# a second row for Asha is refused by the primary key
try:
    con.execute("INSERT INTO customer_contacts VALUES (1, '555-0199')")
    raise SystemExit("insert should have failed")
except Exception as e:
    assert "violates primary key constraint" in str(e)
# source: https://docs.djangoproject.com/en/5.0/ref/models/fields/#onetoonefield
# confirmed: OneToOneField is "conceptually similar to a ForeignKey with unique=True"
