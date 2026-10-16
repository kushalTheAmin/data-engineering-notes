# checks for notes/011-why-gujarati-takes-3-bytes.md
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop

n = ord("ગ")
assert n == 2711 and n < 2 ** 12 and len(format(n, "b")) == 12
bits = format(n, "016b")
assert bits == "0000101010010111"
b = "ગ".encode()
assert len(b) == 3 and 3 * 8 == 24
assert [format(x, "08b") for x in b] == ["11100000", "10101010", "10010111"]
# label bits: 4 + 2 + 2 = 8, leaving 16 free bits
assert 4 + 2 + 2 == 8 and 24 - 8 == 16
assert 2 ** 16 - 1 == 65535
assert 2 ** 11 - 1 == 2047 and 2 ** 7 - 1 == 127
# the free bit counts match the real ranges
for size, free in [(1, 7), (2, 11), (3, 16)]:
    assert len(chr(2 ** free - 1).encode()) == size
    assert len(chr(2 ** free).encode()) == size + 1 or free == 16
# dhokla in gujarati
w = "ઢોકળા"
assert len(w) == 5 and len(w.encode()) == 15 and len("dhokla".encode()) == 6
assert all(len(c.encode()) == 3 for c in w)
# check yourself
assert format(0b10110001, "08b").startswith("10")
db = shop()
name = db.execute("SELECT name FROM products WHERE name = 'fafda'").fetchone()[0]
assert len((name + "ગગ").encode()) == 11 == 5 + 2 * 3
# 3 units on screen
import duckdb
assert duckdb.sql("SELECT length_grapheme('ઢોકળા')").fetchone()[0] == 3
# 2 byte label 110 leaves 5 + 6 = 11 free bits
assert 5 + 6 == 11 and "é".encode()[0] >> 5 == 0b110
# source: https://en.wikipedia.org/wiki/UTF-8
#   two byte form is 110xxxxx 10xxxxxx, three byte form is 1110xxxx 10xxxxxx 10xxxxxx; the start of a code point can be found by backing up at most three bytes
# source: https://duckdb.org/docs/current/sql/functions/text.html
#   strlen(string): number of bytes; length(string): number of characters; length_grapheme(string): number of grapheme clusters
print("011 ok")
