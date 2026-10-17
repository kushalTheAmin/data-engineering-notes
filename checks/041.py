# checks for notes/041-text-files-vs-binary-files.md
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
for n, text_hex, text_len, int_hex in [
    (101, "31 30 31", 3, "65 00 00 00"),
    (100000, "31 30 30 30 30 30", 6, "a0 86 01 00"),
]:
    t = str(n).encode("utf-8")
    i = struct.pack("<i", n)
    assert t.hex(" ") == text_hex and len(t) == text_len
    assert i.hex(" ") == int_hex and len(i) == 4
# a0 alone is not valid utf-8
try:
    struct.pack("<i", 100000).decode("utf-8")
    raise SystemExit("should fail")
except UnicodeDecodeError:
    pass
# the integer for 101 does decode, as e plus three NUL characters
assert struct.pack("<i", 101).decode("utf-8") == "e\x00\x00\x00"
# 4 text digits... text length grows with digits, integer stays 4
assert len(str(10 ** 8).encode()) == 9
# source: https://parquet.apache.org/docs/file-format/
#   confirmed: a Parquet file starts with the 4-byte magic number "PAR1"
print("041 ok")
