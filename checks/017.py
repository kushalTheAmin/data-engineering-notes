# checks for notes/017-fractions-in-binary.md
import sys, os
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop

def val(bits_int, bits_frac):
    return int(bits_int, 2) + sum(int(b) * Fraction(1, 2 ** (i + 1)) for i, b in enumerate(bits_frac))

assert val("111", "100") == Fraction(15, 2)  # 7.50
assert val("100", "100") == Fraction(9, 2)   # 4.50
assert val("110", "000") == 6
assert val("0", "11") == Fraction(3, 4)
assert val("0", "101") == Fraction(5, 8)
con = shop()
prices = dict(con.execute("SELECT name, price FROM products").fetchall())
assert float(prices["khandvi"]) == 7.5 and float(prices["fafda"]) == 4.5 and float(prices["dhokla"]) == 6.0
assert Fraction(7.5) == Fraction("7.5") and Fraction(0.75) == Fraction("0.75")
assert Fraction(0.1) != Fraction("0.1")
print("017 ok")
