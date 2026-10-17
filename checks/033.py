# checks for notes/033-kilobytes-to-terabytes.md
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop

con = shop()
line = "101,1,2026-04-01 09:15:00,delivered"
assert len(line.encode()) == 35 and len(line) == 35
# the line really is order 101 as the shop stores it
r = con.execute("SELECT order_id, customer_id, ordered_at, status FROM orders WHERE order_id = 101").fetchone()
assert f"{r[0]},{r[1]},{r[2]},{r[3]}" == line
# the other six orders are 33 to 35 bytes
sizes = [len(f"{a},{b},{c},{d}".encode()) for a, b, c, d in
         con.execute("SELECT order_id, customer_id, ordered_at, status FROM orders").fetchall()]
assert len(sizes) == 7 and min(sizes) == 33 and max(sizes) == 35
assert sorted(sizes)[1:] == [35] * 6 or max(sizes) == 35
# each step is 1000 times the last
assert 1000 ** 4 == 1_000_000_000_000
assert 35 * 1000 ** 2 == 35_000_000 and 35 * 1000 ** 3 == 35_000_000_000 and 35 * 1000 ** 4 == 35 * 10 ** 12
# 100 megabits a second, 8 bits per byte
assert 100 / 8 == 12.5
# source: https://www.nist.gov/pml/owm/metric-si-prefixes
#   confirmed: kilo is 1000, mega million, giga billion, tera trillion
# source: https://en.wikipedia.org/wiki/Kilobyte
#   confirmed: SI defines kilo as 1000 so a kilobyte is 1000 bytes; some IT usage uses 1024
# source: https://en.wikipedia.org/wiki/Byte
#   confirmed: unit symbol for the byte is upper-case B
# source: https://en.wikipedia.org/wiki/Megabit
#   confirmed: megabit is 1000^2 bits, and lower-case b is widely used as the symbol for bit
print("033 ok")
