# checks for notes/013-negative-numbers-sign-bit.md
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop

db = shop()
price = db.execute("SELECT price FROM products WHERE name = 'dhokla'").fetchone()[0]
assert float(price) == 6.0
assert format(6, "08b") == "00000110" and "1" + format(6, "07b") == "10000110"
assert int("0000000", 2) == 0
# range with 7 size bits
assert 2**7 - 1 == 127 and len(range(-127, 128)) == 255 and 2**8 == 256
assert -0.0 == 0.0 and str(-0.0) == "-0.0"
# check yourself 1
whole = db.execute("SELECT CAST(price AS INTEGER) FROM products WHERE name = 'kaju katli'").fetchone()[0]
assert whole == 12 and format(12, "b") == "1100" and "1" + format(12, "07b") == "10001100"
# check yourself 2
# the unpadded guess is only 5 bits, not a full byte
assert "1" + "1100" == "11100" and len("11100") == 5 != 8
assert int("10000000"[1:], 2) == int("00000000"[1:], 2) == 0 and "10000000" != "00000000"
# source: https://en.wikipedia.org/wiki/Signed_number_representations
#   sign-magnitude: sign bit 0 for positive and 1 for negative, remaining bits hold the magnitude; it can represent negative zero; it is the most common way of representing the significand in floating-point values
print("013 ok")
