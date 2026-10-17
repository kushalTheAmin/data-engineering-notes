# checks for notes/047-compression-spotting-repeats.md
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop

con = shop()
statuses = [r[0] for r in con.execute("SELECT status FROM orders ORDER BY order_id").fetchall()]
assert statuses == ["delivered", "delivered", "delivered", "cancelled", "delivered", "pending", "delivered"]
assert len(statuses) == 7 and statuses.count("delivered") == 5


def rle(items):
    runs = []
    for x in items:
        if runs and runs[-1][0] == x:
            runs[-1][1] += 1
        else:
            runs.append([x, 1])
    return runs


def sizes(data):
    runs = rle(data)
    raw = len("".join(s + "\n" for s in data))
    packed = len("".join(f"{n},{s}\n" for s, n in runs))
    return len(runs), raw, packed


assert sizes(statuses) == (5, 68, 58)
assert sizes(sorted(statuses)) == (3, 68, 34)
# 10 bytes saved as ordered, half the size sorted
assert 68 - 58 == 10 and 68 // 2 == 34
# a run of one costs more than the bare word
assert len("1,cancelled\n") == 12 and len("cancelled\n") == 10
# lossless: expanding the runs gives the original back
assert [s for s, n in rle(statuses) for _ in range(n)] == statuses
# source: https://en.wikipedia.org/wiki/Run-length_encoding
#   confirmed: RLE stores a single occurrence of a value and a count of its consecutive occurrences;
#   for files without many runs, RLE could increase the file size
# source: https://parquet.apache.org/docs/file-format/data-pages/encodings/
#   confirmed: Parquet's RLE/bit-packing hybrid encoding stores repeated values more efficiently
print("047 ok")
