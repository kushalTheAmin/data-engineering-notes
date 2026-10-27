# checks for notes/231-isolation-two-people-at-the-same-time.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
import duckdb
con = shop()
q = lambda s: con.execute(s).fetchall()
# the shop has 7 orders, 5 delivered (check yourself 1)
assert q("SELECT count(*) FROM orders") == [(7,)]
assert q("SELECT count(*) FROM orders WHERE status = 'delivered'") == [(5,)]
# two connections: uncommitted insert is invisible to the other one
db = duckdb.connect()
db.execute("CREATE TABLE my_orders AS SELECT 101 + range AS order_id FROM range(7)")
asha, esha = db.cursor(), db.cursor()
cnt = lambda w: w.execute("SELECT count(*) FROM my_orders").fetchone()[0]
esha.execute("BEGIN"); esha.execute("INSERT INTO my_orders VALUES (108)")
assert (cnt(esha), cnt(asha)) == (8, 7)
esha.execute("ROLLBACK"); assert cnt(asha) == 7
esha.execute("BEGIN"); esha.execute("INSERT INTO my_orders VALUES (108)"); esha.execute("COMMIT")
assert cnt(asha) == 8
# source: https://www.postgresql.org/docs/current/transaction-iso.html
#   confirmed (opened this run): "Read Committed is the default isolation level in PostgreSQL"; a SELECT "sees only data committed before the query began; it never sees either uncommitted data or changes committed by concurrent transactions during the query's execution"; Serializable is the strictest level
