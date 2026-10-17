# checks for notes/038-1000-or-1024.md
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# ten doublings of 1
assert 2 ** 10 == 1024
x = 1
for _ in range(10):
    x *= 2
assert x == 1024
assert 1000 ** 1 == 1000 and 1024 ** 2 == 1_048_576 and 1024 ** 3 == 1_073_741_824 and 1024 ** 4 == 1_099_511_627_776
assert [f"{1000 ** s / 1024 ** s:.1%}" for s in range(1, 5)] == ["97.7%", "95.4%", "93.1%", "90.9%"]
# 2.3 percent off at KB, about 9 percent at TB
assert round((1 - 1000 / 1024) * 100, 1) == 2.3
assert round((1 - 1000 ** 4 / 1024 ** 4) * 100) == 9
# the 500 GB drive and the shops 35 TB of orders
assert round(500 * 1000 ** 3 / 1024 ** 3, 1) == 465.7
assert round(35 * 10 ** 12 / 1024 ** 4, 1) == 31.8
# 500 minus 465 is the 35 the opening asks about
assert 500 - 465 == 35
# source: https://en.wikipedia.org/wiki/Binary_prefix
#   confirmed: kibi, mebi, gibi, tebi are IEC names for 1024 powers, KiB = 1024 bytes; Windows still uses GB for binary values; Mac OS X, Ubuntu and Debian use decimal
# source: https://en.wikipedia.org/wiki/Gigabyte
#   confirmed: 1 GiB = 1073741824 bytes; Windows reports sizes in binary, Mac OS X 10.6+ in decimal; a 400 GB drive shows as 372 in Windows
print("038 ok")
