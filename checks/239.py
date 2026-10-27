# checks for notes/239-isolation-levels-read-committed.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the shop has 7 orders, an imagined committed 108 makes 8
assert q("SELECT count(*) FROM orders")[0][0] == 7
assert 7 + 1 == 8
# check yourself 1: 5 delivered now, order 107 is delivered, cancelling it leaves 4
assert q("SELECT count(*) FROM orders WHERE status = 'delivered'")[0][0] == 5
assert q("SELECT status FROM orders WHERE order_id = 107") == [("delivered",)]
assert q("SELECT count(*) FROM orders WHERE status = 'delivered' AND order_id <> 107")[0][0] == 4
# source: https://www.postgresql.org/docs/current/transaction-iso.html
#   confirmed (opened this run): "Read Committed is the default isolation level in PostgreSQL"; a SELECT "sees only data committed before the query began; it never sees either uncommitted data or changes committed by concurrent transactions during the query's execution"; "two successive SELECT commands can see different data, even though they are within a single transaction"
#   confirmed (opened this run): the rule is worded for "a SELECT query"; "UPDATE, DELETE, SELECT FOR UPDATE, and SELECT FOR SHARE commands behave the same as SELECT in terms of searching for target rows" but a target row "might have already been updated ... by another concurrent transaction", then the updater waits and applies to the updated row (so the note words the rule for SELECT)
