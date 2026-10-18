# checks for notes/056-grep-finding-matching-lines.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
rows = con.execute("SELECT order_id, customer_id, ordered_at, status FROM orders ORDER BY order_id").fetchall()
lines = ["order_id,customer_id,ordered_at,status"] + [f"{a},{b},{c},{d}" for a, b, c, d in rows]
assert len(lines) == 8                                    # header plus 7 orders
hits = [l for l in lines if "delivered" in l]
assert len(hits) == 5                                     # 101 102 103 105 107
assert [l.split(",")[0] for l in hits] == ["101", "102", "103", "105", "107"]
assert [l for l in lines if "1" in l] == lines[1:]        # grep 1: all 7 orders, not the header
assert len([l for l in lines if "1" in l]) == 7
assert all("1" in str(r[0]) for r in rows)                # every order id has a 1
assert sum(1 for r in rows if r[1] == 1) == 3             # customer 1 really has 3 orders
# source: https://man7.org/linux/man-pages/man1/grep.1.html
#   confirmed: "grep - print lines that match patterns", "grep searches for patterns in each FILE"
# source: https://man7.org/linux/man-pages/man1/grep.1.html
#   confirmed: patterns are read as basic regular expressions by default ("-G ... This is the default"), so . and * are special
print("056 ok")
