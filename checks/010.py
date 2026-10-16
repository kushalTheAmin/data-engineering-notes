# checks for notes/010-utf-8.md
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop

rows = [("d", 100, 1, "64"), ("é", 233, 2, "c3 a9"), ("ગ", 2711, 3, "e0 aa 97"), ("🙂", 128578, 4, "f0 9f 99 82")]
for ch, n, size, hx in rows:
    b = ch.encode("utf-8")
    assert ord(ch) == n and len(b) == size and b.hex(" ") == hx
# the range table: first and last code point of each row
for lo, hi, size in [(0, 127, 1), (128, 2047, 2), (2048, 65535, 3), (65536, 1114111, 4)]:
    assert len(chr(lo).encode()) == size and len(chr(hi).encode()) == size
assert 0x10FFFF == 1114111
# multi-byte characters only use bytes 128 or higher, and ascii is unchanged
for cp in range(128, 0x110000):
    if 0xD800 <= cp <= 0xDFFF:
        continue
    assert all(x >= 128 for x in chr(cp).encode("utf-8"))
assert "dhokla".encode("utf-8") == "dhokla".encode("ascii")
# 4 bytes for every character would make english 4 times bigger
assert len("dhokla".encode("utf-32-be")) == 4 * len("dhokla".encode("utf-8"))
try:
    chr(55296).encode("utf-8")
    raise SystemExit("surrogates should not encode")
except UnicodeEncodeError:
    pass
assert 0xD800 == 55296 and 0xDFFF == 57343
# the character count and byte count disagree
assert len("é") == 1 and len("é".encode()) == 2
assert 10 // len("é".encode()) == 5 and 10 // len("d".encode()) == 10
con = shop()
assert con.execute("SELECT strlen(name), strlen(name || 'é') FROM products WHERE name = 'jalebi'").fetchall() == [(6, 8)]
# source: https://en.wikipedia.org/wiki/UTF-8
#   encodes code points in one to four bytes; U+0000-007F one, 0080-07FF two, 0800-FFFF three, 10000-10FFFF four;
#   first 128 code points use one byte with the same value as ASCII; surrogates U+D800 to U+DFFF are not legal
# source: https://duckdb.org/docs/current/sql/functions/text.html
#   strlen(string): number of bytes in string
print("010 ok")
