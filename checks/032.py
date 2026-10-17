# checks for notes/032-null-is-not-zero-or-empty-text.md
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop
con = shop()
rows = con.execute("SELECT order_id, stars, stars_zero_filled FROM order_ratings").fetchall()
assert rows == [(101, 5, 5), (102, 4, 4), (103, None, 0), (105, 3, 3), (107, None, 0)]
assert con.execute("SELECT avg(stars), avg(stars_zero_filled) FROM order_ratings").fetchone() == (4.0, 2.4)
# by hand: nulls skipped divides 12 by 3, zeros divides 12 by 5
assert 5 + 4 + 3 == 12 and 12 / 3 == 4.0 and 12 / 5 == 2.4
# 103 and 107 are real delivered orders in the shop
assert con.execute("SELECT count(*) FROM orders WHERE order_id IN (103, 107) AND status = 'delivered'").fetchone()[0] == 2
# quiz 1: empty strings count, nulls do not
assert con.execute("SELECT count(*), count(city) FROM (VALUES ('Edison'), (''), (''), (NULL), (NULL)) AS t(city)").fetchone() == (5, 3)
# quiz 2
assert con.execute("SELECT avg(stars_zero_filled) FROM order_ratings WHERE stars_zero_filled > 0").fetchone()[0] == 4.0
# source: https://www.postgresql.org/docs/current/functions-aggregate.html
#   confirmed: avg computes the average of all the non-null input values
# source: https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/Nulls.html
#   confirmed: "Oracle Database treats a character value with a length of zero as null."
print("032 ok")
