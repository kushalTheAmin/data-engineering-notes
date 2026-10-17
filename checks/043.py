# checks for notes/043-reading-start-to-end-vs-jumping.md
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop

rows = shop().execute("SELECT order_id, status FROM orders ORDER BY order_id").fetchall()
assert len(rows) == 7
lines = [f"{i},{s}\n" for i, s in rows]
sizes = [len(l) for l in lines]
assert sizes == [14, 14, 14, 14, 14, 12, 14]
starts = [sum(sizes[:k]) for k in range(7)]
assert starts == [0, 14, 28, 42, 56, 70, 82]
assert 14 * 6 == 84 and 84 != 82
data = "".join(lines).encode()
f = io.BytesIO(data)
# the guess 14 * 6 is aimed at line 7 (line 6 happens to start at 14 * 5 = 70)
assert 14 * 5 == starts[5] and 14 * 6 > starts[6]
f.seek(14 * 6)
assert f.readline() == b"7,delivered\n"
f.seek(82)
assert f.readline() == b"107,delivered\n"
# q1: CRLF, line 6 starts after five lines of 14 + 1
assert sum(len(l) + 1 for l in lines[:5]) == 75 == 5 * 15
# q2: fixed 20 byte lines
assert 499999 * 20 == 9999980
assert 999_999 == 1_000_000 - 1
# source: https://docs.python.org/3/library/io.html
#   confirmed: seek changes the stream position to the given byte offset
print("043 ok")
