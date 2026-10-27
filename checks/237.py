# checks for notes/237-non-repeatable-reads.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# dhokla is 6.00 in the shop before Esha raises it to 7.00
assert str(q("SELECT price FROM products WHERE name = 'dhokla'")[0][0]) == "6.00"
# check yourself 1: all six prices total 38.00, a 1.00 raise makes 39.00
assert str(q("SELECT sum(price) FROM products")[0][0]) == "38.00"
assert 38.00 + (7.00 - 6.00) == 39.00
# source: https://www.postgresql.org/docs/current/transaction-iso.html
#   confirmed (opened this run): "nonrepeatable read: A transaction re-reads data it has previously read and finds that data has been modified by another transaction (that committed since the initial read)"; Table 13.1 lists nonrepeatable read as Possible at Read committed
