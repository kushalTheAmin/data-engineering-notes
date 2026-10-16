# checks for notes/020-why-0-1-plus-0-2-is-not-0-3.md
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop
from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 60
con = shop()
# python block
assert str(Decimal(0.1) + Decimal(0.2)) == "0.3000000000000000166533453693773481063544750213623046875"
assert str(Decimal(0.1 + 0.2)) == "0.3000000000000000444089209850062616169452667236328125"
assert str(Decimal(0.3)) == "0.299999999999999988897769753748434595763683319091796875"
assert (0.1 + 0.2 == 0.3) is False and repr(0.1 + 0.2) == "0.30000000000000004"
# both stored values are slightly too big
assert Fraction(0.1) > Fraction(1, 10) and Fraction(0.2) > Fraction(2, 10)
# 0.3 stored slightly low
assert Fraction(0.3) < Fraction(3, 10)
# exact sum sits exactly halfway between float(0.3) and the rounded result
s = Fraction(0.1) + Fraction(0.2)
assert s - Fraction(0.3) == Fraction(0.1 + 0.2) - s
# floats near 0.3 are 2**-54 apart, about 5.55e-17, first nonzero digit is the 17th place
gap = Fraction(0.1 + 0.2) - Fraction(0.3)
assert gap == Fraction(1, 2 ** 54) and 5e-17 < float(gap) < 6e-17
# round to even: the chosen neighbor has an even last mantissa bit
import struct
assert struct.unpack(">Q", struct.pack(">d", 0.1 + 0.2))[0] % 2 == 0
assert struct.unpack(">Q", struct.pack(">d", 0.3))[0] % 2 == 1
# quiz 1
assert repr(0.1 + 0.2 + 0.3) == "0.6000000000000001"
assert 0.3 + 0.2 + 0.1 == 0.6 and 0.1 + 0.2 + 0.3 != 0.6
assert math.isclose(0.1 + 0.2 + 0.3, 0.6)
# quiz 2
rows = con.execute("SELECT name, price FROM products WHERE price::DOUBLE + 0.1 + 0.2 = price::DOUBLE + 0.3").fetchall()
assert [r[0] for r in rows] == ["dhokla", "khandvi", "jalebi", "fafda"]
assert con.execute("SELECT count(*) FROM products").fetchone()[0] == 6
# source: https://docs.python.org/3/library/math.html#math.isclose
#   confirmed: math.isclose default rel_tol is 1e-09, "same within about 9 decimal digits"
# source: https://docs.python.org/3/tutorial/floatingpoint.html
#   confirmed: summing 0.1 values may not give exactly 0.3, math.isclose is useful for comparing inexact values
# source: https://en.wikipedia.org/wiki/IEEE_754
#   confirmed: "round to nearest, ties to even" is the default for binary floating point; an exact tie goes to the neighbor whose last digit is even (0 in binary)
print("020 ok")
