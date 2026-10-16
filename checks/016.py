# checks for notes/016-overflow.md
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop

def wrap8(n):
    return (n + 128) % 256 - 128

# table rows
for sale, pat, val in [("before", "01111110", 126), ("+1", "01111111", 127), ("+1", "10000000", -128), ("+1", "10000001", -127)]:
    raw = int(pat, 2)
    assert (raw - 256 if raw >= 128 else raw) == val
assert int("01111110", 2) + 1 == int("01111111", 2)
assert int("01111111", 2) + 1 == int("10000000", 2)
assert wrap8(127 + 1) == -128 and wrap8(127 + 2) == -127
# quiz 1
con = shop()
assert con.execute("SELECT max(order_id) FROM orders").fetchone()[0] == 107
assert 107 + 21 == 128 and wrap8(128) == -128
for q in ["SELECT 127::TINYINT + 1::TINYINT", "SELECT max(order_id)::TINYINT + 21::TINYINT FROM orders"]:
    try:
        con.execute(q)
        raise SystemExit("should fail")
    except Exception as e:
        assert "Overflow" in str(e) or "Out of Range" in str(e)
# quiz 2
assert wrap8(200) == -56 and wrap8(456) == -56 and 456 - 200 == 256
assert 2 ** 31 - 1 == 2147483647
# source: https://docs.oracle.com/javase/specs/jls/se21/html/jls-4.html
#   "The integer operators do not indicate overflow or underflow in any way."
# source: https://en.wikipedia.org/wiki/Gangnam_Style
#   Dec 1 2014, YouTube said views passed 2,147,483,647 (32-bit signed max) and moved to 64-bit integers
# source: https://www.postgresql.org/docs/current/datatype-numeric.html
#   storing values outside smallint, integer, bigint ranges results in an error
# source: https://duckdb.org/docs/current/sql/data_types/numeric.html
#   TINYINT is 1 byte, -2^7 to 2^7 - 1; values outside the allowed range result in an error
print("016 ok")
