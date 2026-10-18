# checks for notes/055-wc-counting-lines.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
rows = con.execute("SELECT order_id, customer_id, ordered_at, status FROM orders ORDER BY order_id").fetchall()
lines = ["order_id,customer_id,ordered_at,status"] + [f"{a},{b},{c},{d}" for a, b, c, d in rows]
assert len(rows) == 7                       # 7 orders
full = ("\n".join(lines) + "\n").encode()
cut = ("\n".join(lines)).encode()           # final 0a missing
assert full.count(b"\n") == 8               # wc -l orders.csv
assert cut.count(b"\n") == 7                # wc -l cut.csv
assert len(cut.split(b"\n")) == 8           # 8 rows of text still there
data = b"106,1,2026-04-08 10:00:00,pending\n107,2,2026-04-09 13:45:00,delivered"
assert (data.count(b"\n"), len(data.split(b"\n"))) == (1, 2)
assert lines[-2:] == ["106,1,2026-04-08 10:00:00,pending", "107,2,2026-04-09 13:45:00,delivered"]
# source: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/wc.html
#   confirmed: wc -l writes the number of <newline> characters in each input file
# source: https://man7.org/linux/man-pages/man1/wc.1.html
#   confirmed: wc prints newline, word and byte counts
print("055 ok")
