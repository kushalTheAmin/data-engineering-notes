# checks for notes/017-fractions-in-binary.md
import sys, os
from decimal import Decimal
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop
# table: places after the point are 0.5, 0.25, 0.125
for i in range(8):
    pat = format(i, "03b")
    vals = [0.5 * int(pat[0]), 0.25 * int(pat[1]), 0.125 * int(pat[2])]
    assert sum(vals) == i * 0.125
assert [i * 0.125 for i in range(8)] == [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]
# 0.30 sits between .010 (0.25) and .011 (0.375)
assert 0.25 < 0.30 < 0.375
# shop prices
con = shop()
assert float(con.execute("SELECT price FROM products WHERE name='khandvi'").fetchone()[0]) == 7.5
assert float(con.execute("SELECT price FROM products WHERE name='fafda'").fetchone()[0]) == 4.5
assert 4 + 2 + 1 + 0.5 == 7.5 and 4 + 0.5 == 4.5
assert int("111", 2) == 7 and int("100", 2) == 4
# python output
assert str(Decimal(0.75)) == "0.75"
assert str(Decimal(0.1)) == "0.1000000000000000055511151231257827021181583404541015625"
# 0.1 never lands: an exact binary fraction is a whole number over a power of 2, 0.1 is 1/10
from fractions import Fraction
assert all((Fraction(1, 10) * 2 ** k).denominator != 1 for k in range(1, 200))
# source: https://docs.python.org/3/tutorial/floatingpoint.html
#   0.1 cannot be represented exactly as a base 2 fraction, no matter how many digits you take
print("017 ok")
