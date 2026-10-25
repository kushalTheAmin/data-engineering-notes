# checks for notes/216-unique-no-two-rows-may-share-a-value.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
con.execute("CREATE TABLE login (customer_id INTEGER NOT NULL, email VARCHAR UNIQUE)")
con.execute("INSERT INTO login VALUES (1, 'asha@example.com'), (2, 'bhavin@example.com')")
assert q("SELECT * FROM login ORDER BY customer_id") == [(1, "asha@example.com"), (2, "bhavin@example.com")]
try:
    con.execute("INSERT INTO login VALUES (3, 'asha@example.com')")
    assert False
except Exception as e:
    assert "unique" in str(e).lower()
assert q("SELECT count(*) FROM login") == [(2,)]
con.execute("INSERT INTO login VALUES (4, NULL), (5, NULL)")
assert q("SELECT count(*), count(email) FROM login") == [(4, 2)]
# check yourself 1
con.execute("CREATE TABLE coupon (code VARCHAR UNIQUE, customer_id INTEGER)")
con.execute("INSERT INTO coupon VALUES ('DIWALI', 1), ('diwali', 2)")
assert q("SELECT count(*) FROM coupon") == [(2,)]
# check yourself 2
con.execute("CREATE TABLE hub (city VARCHAR UNIQUE)")
con.execute("INSERT INTO hub VALUES ('Jersey City'), ('Edison'), ('Hoboken'), (NULL), (NULL)")
assert q("SELECT count(*), count(city) FROM hub") == [(5, 3)]
# the shop cities used in question 2 are real
assert sorted(r[0] for r in q("SELECT DISTINCT city FROM customers WHERE city IS NOT NULL")) == ["Edison", "Hoboken", "Jersey City"]
# source: https://www.postgresql.org/docs/current/ddl-constraints.html
#   confirmed (opened this run): null values are never considered equal in the unique comparison, so duplicate rows with a null are storable; NULLS NOT DISTINCT changes this.
