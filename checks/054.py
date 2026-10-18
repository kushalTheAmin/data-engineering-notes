# checks for notes/054-head-and-tail.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
rows = con.execute("SELECT order_id, customer_id, ordered_at, status FROM orders ORDER BY order_id").fetchall()
lines = ["order_id,customer_id,ordered_at,status"] + [f"{a},{b},{c},{d}" for a, b, c, d in rows]
assert len(lines) == 8                      # header plus 7 orders
assert len(lines) <= 10                     # default head would print the whole file
assert lines[:3] == ["order_id,customer_id,ordered_at,status",
                     "101,1,2026-04-01 09:15:00,delivered",
                     "102,2,2026-04-01 18:40:00,delivered"]
assert len(lines[:3]) - 1 == 2              # head -n 3 gives only two orders
assert lines[-2:] == ["106,1,2026-04-08 10:00:00,pending",
                      "107,2,2026-04-09 13:45:00,delivered"]
assert 1000000 - 10 == 999990
# source: https://www.gnu.org/software/coreutils/manual/html_node/head-invocation.html
#   confirmed: head prints the first part (10 lines by default)
# source: https://www.gnu.org/software/coreutils/manual/html_node/tail-invocation.html
#   confirmed: tail prints the last part (10 lines by default)
print("054 ok")
