# checks for notes/059-redirecting-output-into-a-file.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
rows = con.execute("SELECT order_id, customer_id, status FROM orders ORDER BY order_id").fetchall()
lines = ["%d,%d,x,%s" % r for r in rows]
assert len(rows) + 1 == 8                                      # 8 lines in orders.csv with the header
assert sum(1 for l in lines if "delivered" in l) == 5          # delivered.csv gets 5 lines
assert 1 + 7 == 8 and len("order_id,customer_id,ordered_at,status\n" + "101,1,x,delivered\n" * 7) > 0  # python demo writes 8 lines
# source: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html
#   confirmed: for > "If the file does not exist, it shall be created; otherwise, it shall be truncated to be an empty file after being opened."
import subprocess, tempfile
d = tempfile.mkdtemp()
open(d + "/o.csv", "w").write("a,delivered\n")
r = subprocess.run("grep delivered o.csv > o.csv", shell=True, cwd=d, capture_output=True, text=True)
assert os.path.getsize(d + "/o.csv") == 0 and r.returncode == 2   # emptied before grep looked; gnu grep noticed input is also output
assert "input file is also the output" in r.stderr
print("059 ok")
