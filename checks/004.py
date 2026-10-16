# checks for notes/004-bytes.md
assert 2 ** 8 == 256
# the 6 bytes of dhokla, 8 switches each
assert list("dhokla".encode()) == [100, 104, 111, 107, 108, 97]
assert format(100, "08b") == "01100100" and 64 + 32 + 4 == 100
# you cant fit 300 in one byte
try:
    bytes([300])
    raise AssertionError("bytes([300]) should fail")
except ValueError as e:
    assert str(e) == "bytes must be in range(0, 256)"
# screen colors: one byte each for red, green, blue
assert 256 * 256 * 256 == 16777216
# check yourself
assert len("kaju katli".encode()) == 10 and ord(" ") == 32
assert 2 ** 9 < 1000 <= 2 ** 10 and 2 ** 16 - 1 == 65535
assert len("1000".encode()) == 4
assert len(range(0, 256)) == 256
# source: https://www.computerhope.com/jargon/d/dotted-quad-notation.htm
#   an IPv4 address is four numbers from 0 to 255 separated by dots, one byte each
# source: https://en.wikipedia.org/wiki/Color_depth
#   24 bit color almost always uses 8 bits each of R, G, B (16,777,216 colors); deep color uses 10 or more bits per channel
# source: https://en.wikipedia.org/wiki/Dot-decimal_notation
#   IPv4 dotted decimal is four octets, each 0 to 255
# source: https://www.catb.org/jargon/html/B/byte.html
#   older machines used other byte sizes (6, 7 or 9 bits); 8 became the standard
print("004 ok")
