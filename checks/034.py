# checks for notes/034-capstone-one-order-decoded-to-bytes.md
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop

con = shop()
line = "101,1,2026-04-01 09:15:00,delivered"
r = con.execute("SELECT order_id, customer_id, ordered_at, status FROM orders WHERE order_id = 101").fetchone()
assert f"{r[0]},{r[1]},{r[2]},{r[3]}" == line
fields = line.split(",")
sizes = [len(f.encode()) for f in fields]
assert sizes == [3, 1, 19, 9]
assert sum(sizes) == 32 and sum(sizes) + 3 == 35 == len(line.encode())
assert fields[0].encode().hex(" ") == "31 30 31" and fields[1].encode().hex(" ") == "31"
assert fields[2].encode().hex(" ") == "32 30 32 36 2d 30 34 2d 30 31 20 30 39 3a 31 35 3a 30 30"
assert fields[3].encode().hex(" ") == "64 65 6c 69 76 65 72 65 64"
# as a 32 bit integer, 101 is 00 00 00 65
assert (101).to_bytes(4, "big").hex(" ") == "00 00 00 65"
# many machines (little endian) keep the same four bytes in reverse
assert (101).to_bytes(4, "little").hex(" ") == "65 00 00 00"
import sys
assert sys.byteorder == "little"
# source: https://en.wikipedia.org/wiki/Endianness
#   confirmed: little-endian stores the least significant byte first, and is the dominant order on x86 and most current processors
# 13:15 UTC on 1 April 2026 (09:15 New York, -04:00) is 1775049300
from datetime import datetime, timezone
assert int(datetime(2026, 4, 1, 13, 15, tzinfo=timezone.utc).timestamp()) == 1775049300
# quiz 1: lines of 35 and 33 bytes
rows = dict(con.execute("SELECT order_id, strlen(order_id::VARCHAR || ',' || customer_id::VARCHAR || ',' || ordered_at::VARCHAR || ',' || status) FROM orders").fetchall())
assert rows[104] == 35 and rows[106] == 33 and len("cancelled") == 9 and len("pending") == 7
# quiz 2: 1775049300 ms is about 20.5 days
assert abs(1775049300 / 1000 / 86400 - 20.54) < 0.01
assert datetime.fromtimestamp(1775049.3, timezone.utc).strftime("%Y-%m-%d %H:%M:%S") == "1970-01-21 13:04:09"
print("034 ok")
