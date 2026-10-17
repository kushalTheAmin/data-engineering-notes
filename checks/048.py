# checks for notes/048-compression-trades-processor-for-space.md
import os
import zlib

n = 1_000_000
raw = n * len("delivered\n")
packed = len(f"{n},delivered\n")
assert (raw, packed) == (10_000_000, 18)
# a million bytes is a megabyte, so 10,000,000 bytes is 10 MB
assert raw // 1_000_000 == 10
# 150 microseconds against 100 nanoseconds, the note 037 numbers
assert 150_000 > 100
# random bytes with no repeats come out bigger
assert len(zlib.compress(os.urandom(10_000))) > 10_000
# level 1 vs 9: both rebuild the original exactly
data = b"delivered\n" * 1000
assert zlib.decompress(zlib.compress(data, 1)) == data == zlib.decompress(zlib.compress(data, 9))
# source: https://docs.python.org/3/library/zlib.html
#   confirmed: Z_BEST_SPEED (1) is fastest with the least compression, Z_BEST_COMPRESSION (9) is slowest with the most
# source: https://parquet.apache.org/docs/file-format/data-pages/compression/
#   confirmed: Parquet offers several codecs covering different areas in the compression ratio / processing cost spectrum
print("048 ok")
