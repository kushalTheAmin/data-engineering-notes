# checks for notes/036-memory-vs-disk.md
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop

con = shop()
row = con.execute("SELECT order_id, customer_id, ordered_at, status FROM orders WHERE order_id = 101").fetchone()
line = f"{row[0]},{row[1]},{row[2]},{row[3]}"
assert line == "101,1,2026-04-01 09:15:00,delivered"
assert len(line.encode()) == 35
# 8 bits per byte, see checks/004.py
assert 2 ** 8 == 256
# order 101 line is the one 034 decoded; one byte per ascii character
assert len(line) == len(line.encode())
# source: https://en.wikipedia.org/wiki/Volatile_memory
#   confirmed: volatile memory "retains its contents while powered on but when the power is interrupted, the stored data is quickly lost"; "Most general-purpose random-access memory (RAM) is volatile"
# source: https://man7.org/linux/man-pages/man2/fsync.2.html
#   confirmed: fsync() flushes modified in-core data of the file (buffer cache pages) out to the disk device
print("036 ok")
