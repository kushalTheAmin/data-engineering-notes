# checks for notes/060-capstone-the-life-of-one-saved-order.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
rows = con.execute("SELECT order_id, customer_id, ordered_at, status FROM orders ORDER BY order_id").fetchall()
lines = ["order_id,customer_id,ordered_at,status"] + ["%d,%d,%s,%s" % (a, b, str(c), d) for a, b, c, d in rows]
data = ("\n".join(lines) + "\n").encode()
assert len(data) == 289                                       # bytes in orders.csv
assert -(-len(data) // 4096) == 1                             # one 4096 byte block
assert data.count(b"\n") == 8 == len(rows) + 1                # 8 lines with the header
delivered = [l for l in lines if "delivered" in l]
assert len(delivered) == 5                                    # grep delivered | wc -l
crlf = ("\r\n".join(lines) + "\r\n").encode()
assert crlf.count(b"\n") == 8 and sum(b"delivered" in l for l in crlf.split(b"\n")) == 5   # q1: CRLF changes nothing for grep or wc
assert lines[0] not in delivered and len(delivered) == 5      # q2: header has no delivered, clean run leaves 5 lines
assert len(delivered) + 1 != 5 and len(lines) == 8            # q2: old file still 8 lines, tempting 6 is header plus 5
# q3: head stops after 3 lines, wc reads all bytes (no number to compute)
# source: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html
#   confirmed: for > the target is "created; otherwise, it shall be truncated to be an empty file after being opened"
new = data.replace(b"pending", b"delivered")
assert len(new) == 291 and new.count(b"delivered") == 6   # after the save
assert len("delivered") - len("pending") == 2
print("060 ok")
