# checks for notes/015-integer-sizes.md
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop
for bits, by, lo, hi in [(8, 1, -128, 127), (16, 2, -32768, 32767), (32, 4, -2147483648, 2147483647), (64, 8, -9223372036854775808, 9223372036854775807)]:
    assert bits // 8 == by and -(2 ** (bits - 1)) == lo and 2 ** (bits - 1) - 1 == hi
assert 127 + 1 == 128 and 128 > 107
con = shop()
ids = [r[0] for r in con.execute("SELECT order_id FROM orders ORDER BY 1").fetchall()]
assert ids[0] == 101 and ids[-1] == 107
assert con.execute("SELECT typeof(order_id) FROM orders LIMIT 1").fetchone()[0] == "INTEGER"
try:
    con.execute("SELECT 2147483648::INTEGER")
    raise SystemExit("should fail")
except Exception as e:
    assert "Conversion Error" in str(e)
assert con.execute("SELECT typeof(2147483648::BIGINT)").fetchone()[0] == "BIGINT"
assert 256 ** 2 == 65536 and 65536 ** 2 == 4294967296  # doubling bits squares the number of values
# source: https://www.postgresql.org/docs/current/datatype-numeric.html
#   smallint 2 bytes, integer 4 bytes, bigint 8 bytes, with the ranges above; out of range raises an error
# source: https://docs.python.org/3/reference/datamodel.html
#   python int is an unlimited range, subject to available memory
print("015 ok")
