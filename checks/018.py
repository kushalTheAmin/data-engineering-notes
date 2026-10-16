# checks for notes/018-why-0-1-has-no-exact-binary-form.md
import sys, os
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop
# trace table: doubling 0.1, digit, keep
x = Fraction(1, 10)
rows = []
for _ in range(6):
    start = x
    d = x * 2
    digit = 1 if d >= 1 else 0
    x = d - digit
    rows.append((start, d, digit, x))
want = [("0.1", "0.2", 0, "0.2"), ("0.2", "0.4", 0, "0.4"), ("0.4", "0.8", 0, "0.8"),
        ("0.8", "1.6", 1, "0.6"), ("0.6", "1.2", 1, "0.2"), ("0.2", "0.4", 0, "0.4")]
for got, w in zip(rows, want):
    assert (got[0], got[1], got[2], got[3]) == (Fraction(w[0]), Fraction(w[1]), w[2], Fraction(w[3]))
# step 6 starts where step 2 started: the loop is 0011
assert rows[5][0] == rows[1][0]
# 0.5 ends in one step
assert Fraction(1, 2) * 2 == 1 and Fraction(1, 2) * 2 - 1 == 0
# python block output
x = Fraction(1, 10); bits = ""
for _ in range(16):
    x = x * 2
    if x >= 1:
        bits += "1"; x -= 1
    else:
        bits += "0"
assert "0." + bits == "0.0001100110011001"
# ends only if the bottom is a power of two (in lowest terms)
def ends(f): 
    d = Fraction(f).denominator
    return d & (d - 1) == 0
assert [ends(Fraction(s)) for s in ("0.375", "0.2", "0.35", "0.0625")] == [True, False, False, True]
assert Fraction("0.375") == Fraction(3, 8) and Fraction("0.0625") == Fraction(1, 16)
assert Fraction("0.2") == Fraction(1, 5) and Fraction("0.35") == Fraction(7, 20)
assert 10 == 2 * 5
# 0.1, 0.2, 0.3 all repeat
assert not any(ends(Fraction(s)) for s in ("0.1", "0.2", "0.3"))
# 0.5, 0.25 end; 3/8, 1/2, 1/4 end
assert all(ends(f) for f in (Fraction(1, 2), Fraction(1, 4), Fraction(3, 8)))
# shop: all 6 prices are whole eighths, a half is 4 eighths
con = shop()
assert con.execute("SELECT count(*) FROM products WHERE price * 8 = round(price * 8)").fetchone()[0] == 6
assert con.execute("SELECT count(*) FROM products").fetchone()[0] == 6
assert Fraction(1, 2) == 4 * Fraction(1, 8)
# the stored neighbor of 0.1 is a hair above 0.1
from decimal import Decimal
assert Decimal(0.1) > Decimal("0.1")
# source: https://docs.python.org/3/tutorial/floatingpoint.html
#   confirmed: 0.1 cannot be represented exactly as a base 2 fraction, and is the infinitely repeating 0.0001100110011...
print("018 ok")
