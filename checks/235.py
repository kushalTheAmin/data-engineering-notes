# checks for notes/235-lost-updates.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
import duckdb
con = shop()
q = lambda s: con.execute(s).fetchall()
# the dhokla price in the shop is 6.00, so +1 and +0.50 gives 7.50, and python overwrite leaves 6.50 (check yourself 1)
assert q("SELECT price FROM products WHERE name = 'dhokla'") == [(6,)] or str(q("SELECT price FROM products WHERE name = 'dhokla'")[0][0]) == "6.00"
assert str(q("SELECT price + 1 + 0.5 FROM products WHERE name = 'dhokla'")[0][0]) == "7.50"
assert str(q("SELECT price + 0.5 FROM products WHERE name = 'dhokla'")[0][0]) == "6.50"
# the two ways
db = duckdb.connect()
db.execute("CREATE TABLE stock (product VARCHAR, left_over INTEGER)")
db.execute("INSERT INTO stock VALUES ('dhokla', 10)")
asha, bhavin = db.cursor(), db.cursor()
read = lambda who: who.execute("SELECT left_over FROM stock").fetchone()[0]
a = read(asha); b = read(bhavin)
asha.execute(f"UPDATE stock SET left_over = {a - 1}")
bhavin.execute(f"UPDATE stock SET left_over = {b - 1}")
assert read(asha) == 9
db.execute("UPDATE stock SET left_over = 10")
asha.execute("UPDATE stock SET left_over = left_over - 1")
bhavin.execute("UPDATE stock SET left_over = left_over - 1")
assert read(asha) == 8
# check yourself 2: both pass the check on 1 left, both subtract 1
left = 1
left = left - 1
left = left - 1
assert left == -1
# source: https://www.postgresql.org/docs/current/transaction-iso.html
#   confirmed (opened this run): at read committed a would-be updater "will wait for the first updating transaction to commit or roll back", then "attempt to apply its operation to the updated version of the row"

#   confirmed (opened this run): "Read Committed is the default isolation level in PostgreSQL."
#   confirmed (opened this run), repeatable read section: if the first updater commits "the repeatable read transaction will be rolled back with the message ERROR:  could not serialize access due to concurrent update"
