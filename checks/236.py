# checks for notes/236-dirty-reads.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# dhokla is 6.00 in the shop, the committed price in the trace table and in the query
assert str(q("SELECT price FROM products WHERE name = 'dhokla'")[0][0]) == "6.00"
# check yourself 1: 7 orders committed, a dirty reader would add draft 108 to make 8
assert q("SELECT count(*) FROM orders") == [(7,)]
assert 7 + 1 == 8
# source: https://www.postgresql.org/docs/current/transaction-iso.html
#   confirmed (opened this run): "dirty read: A transaction reads data written by a concurrent uncommitted transaction"; Table 13.1 lists dirty read at Read uncommitted as "Allowed, but not in PG"; "PostgreSQL's Read Uncommitted mode behaves like Read Committed"
