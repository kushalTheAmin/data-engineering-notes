# checks for notes/006-one-byte-two-hex-digits.md
from itertools import product
# the dhokla table: split each byte, read each half
for c, hx in zip("dhokla", ["64", "68", "6f", "6b", "6c", "61"]):
    b = format(ord(c), "08b")
    hi, lo = int(b[:4], 2), int(b[4:], 2)
    assert format(ord(c), "02x") == hx == "0123456789abcdef"[hi] + "0123456789abcdef"[lo]
    assert hi == 6
assert [format(ord(c), "08b") for c in "dhokla"] == ["01100100", "01101000", "01101111", "01101011", "01101100", "01100001"]
# ff is 255
assert 15 * 16 + 15 == 255 == int("ff", 16) and int("11111111", 2) == 255
assert 16 * 16 == 256
# byte 5 is 05; 01 02 and 12 collide without padding
assert "%x%x" % (1, 2) == "12" == "%x" % 0x12
# jalebi j is 6a, khandvi k is 6b
assert int("6a", 16) == 106 == ord("j") and int("6b", 16) == 107 == ord("k")
assert 6 * 16 == 96 and 96 + 10 == 106 and 96 + 11 == 107
assert (ord("a"), ord("o"), ord("p")) == (97, 111, 112) and (hex(97), hex(111), hex(112)) == ("0x61", "0x6f", "0x70")
# #00ff00
assert [int(h, 16) for h in ("00", "ff", "00")] == [0, 255, 0]
# 1f2 can split two ways
assert bytes.fromhex("01f2") != bytes.fromhex("1f02")
# source: https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color
#   confirmed: #RRGGBB six-value syntax, two hex digits per red, green, blue channel
print("006 ok")
