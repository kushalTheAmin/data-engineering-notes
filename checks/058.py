# checks for notes/058-pipes.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
rows = con.execute("SELECT order_id, customer_id, status FROM orders ORDER BY order_id").fetchall()
lines = ["%d,%d,x,%s" % r for r in rows]
delivered = [l for l in lines if "delivered" in l]
assert len(rows) + 1 == 8                                  # 8 lines in orders.csv with the header
assert len(delivered) == 5                                 # grep delivered keeps 5, wc -l prints 5
assert [l[:3] for l in delivered if ",1," in l] == ["101", "103"]   # question 3 prints 2
assert sum(1 for r in rows if r[1] == 1) == 3              # customer 1 has 3 orders
assert not any("delivered" in l for l in ["8 orders.csv"])  # question 1 prints nothing
# source: https://www.gnu.org/software/bash/manual/html_node/Pipelines.html
#   confirmed: "The output of each command in the pipeline is connected via a pipe to the input of the next command."; each command runs in its own subshell, a separate process
# source: https://man7.org/linux/man-pages/man7/pipe.7.html
#   confirmed: pipes provide a unidirectional interprocess communication channel; "A pipe has a limited capacity."
# source: https://man7.org/linux/man-pages/man1/wc.1.html
#   confirmed: with a FILE given wc reads that file, with no FILE it reads standard input
print("058 ok")
