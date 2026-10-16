# checks for notes/019-floating-point.md
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop
con = shop()
# table rows: real shop prices, binary form, 1.x digits, slide
def norm(x):
    s = 0
    while x >= 2:
        x /= 2; s += 1
    return x, s
want = {"dhokla": ("6.00", "110", "1.1", 2), "khandvi": ("7.50", "111.1", "1.111", 2),
        "fafda": ("4.50", "100.1", "1.001", 2), "kaju katli": ("12.00", "1100", "1.1", 3)}
def tobin(x):
    i, f = int(x), x - int(x)
    out = bin(i)[2:]
    if f:
        out += "."
        while f:
            f *= 2
            out += str(int(f)); f -= int(f)
    return out
for name, (price, b, digits, slide) in want.items():
    row = con.execute("SELECT price FROM products WHERE name = ?", [name]).fetchone()
    assert str(row[0]) == price
    assert tobin(float(price)) == b
    m, s = norm(float(price))
    assert s == slide and tobin(m) == digits
# bit split
assert 1 + 11 + 52 == 64 and 64 // 8 == 8
# integer 64 bit top is about 9 quintillion
assert 2 ** 63 - 1 == 9223372036854775807
# float range holds tiny and about 1e300
assert sys.float_info.max > 1e300 and len(str(int(1e300))) == 301 and 1e-6 > 0
# python block
big = 2.0 ** 53
assert str(big + 1) == "9007199254740992.0" and str(big + 2) == "9007199254740994.0"
# javascript safe integer
assert 2 ** 53 - 1 == 9007199254740991
# source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER
#   confirmed: JS numbers are double precision floats, MAX_SAFE_INTEGER is 2^53 - 1 = 9007199254740991, above it +1 and +2 round to the same value
# source: https://en.wikipedia.org/wiki/Double-precision_floating-point_format
#   confirmed: 1 sign bit, 11 exponent bits, 52 stored fraction bits, implicit leading 1, exponent stored with bias 1023
# 2 apart then 4 apart, and the largest float has 309 digits
assert 2.0 ** 53 + 3 == 2.0 ** 53 + 4 and 2.0 ** 54 + 2 == 2.0 ** 54 and 2.0 ** 54 + 4 != 2.0 ** 54
assert len(str(int(sys.float_info.max))) == 309 and sys.float_info.min == 2.2250738585072014e-308
# source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse
#   confirmed: "One way to transfer large numbers without loss of precision is to serialize them as strings"
# the wikipedia page above also says: zero and subnormal numbers have no implicit leading 1, the largest normal number is about 1.7976931348623157 x 10^308
# source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER
#   confirmed: "For larger integers, consider using BigInt", so only the ordinary Number type is a float
print("019 ok")
