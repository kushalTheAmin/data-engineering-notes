# checks for notes/008-ascii-runs-out.md
assert 2 ** 7 == 128 and 256 // 2 == 128
for ch, n in [("d", 100), ("~", 126), ("é", 233), ("ગ", 2711)]:
    assert ord(ch) == n
w = "ઢોકળા"
assert len(w) == 5 and [ord(c) for c in w] == [2722, 2763, 2709, 2739, 2750]
assert all(ord(c) > 127 for c in w)
try:
    w.encode("ascii"); assert False
except UnicodeEncodeError:
    pass
assert [bytes([233]).decode(e) for e in ["latin-1", "cp1251"]] == ["é", "й"]
# ascii is a 7 bit code with 128 characters; other countries used the spare half of the byte differently
# source: https://en.wikipedia.org/wiki/ASCII
import duckdb
assert duckdb.sql("SELECT length_grapheme('ઢોકળા')").fetchone()[0] == 3 != len(w)
# source: https://duckdb.org/docs/current/sql/functions/text.html
#   length_grapheme(string): number of grapheme clusters in string, so 3 units on screen against 5 characters
print("008 ok")
