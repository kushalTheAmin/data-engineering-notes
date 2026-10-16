# checks for notes/012-combining-marks.md
import os
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop

pre = "é"
dec = "e" + chr(769)
assert ord(pre) == 233 and chr(769) == "́"
assert pre != dec and len(pre) == 1 and len(dec) == 2
assert len(pre.encode()) == 2 and len(dec.encode()) == 3 == 1 + 2
assert unicodedata.normalize("NFC", dec) == pre
db = shop()
r = db.execute("SELECT length_grapheme(?)", [dec]).fetchone()[0]
assert r == 1
# gujarati gu = ga + vowel sign u
gu = "ગુ"
assert [ord(c) for c in gu] == [0x0A97, 0x0AC1] and len(gu.encode()) == 6
# check yourself 1
name = db.execute("SELECT name FROM customers WHERE name = 'Esha'").fetchone()[0]
assert len(name + dec[1]) == 5 and len((name + dec[1]).encode()) == 6
assert db.execute("SELECT length_grapheme(? || chr(769))", [name]).fetchone()[0] == 4
# source: https://en.wikipedia.org/wiki/Combining_character
# confirmed: precomposed and combining forms both exist, and comparing strings needs normalization first
# source: https://duckdb.org/docs/current/sql/expressions/collations.html
#   by default the BINARY collation is used, so strings are compared based only on their binary contents
