# checks for notes/014-twos-complement.md
pv = [-128, 64, 32, 16, 8, 4, 2, 1]


def val(p):
    return sum(v for b, v in zip(p, pv) if b == "1")


assert val("00000110") == 6 and val("11111010") == -6 and val("11111111") == -1
assert val("10000000") == -128 and val("00000000") == 0
assert -128 + 64 + 32 + 16 + 8 + 2 == -6
vals = [val(format(i, "08b")) for i in range(256)]
assert len(set(vals)) == 256 and min(vals) == -128 and max(vals) == 127 and vals.count(0) == 1
six = "00000110"
fl = "".join("1" if b == "0" else "0" for b in six)
assert fl == "11111001" and format(int(fl, 2) + 1, "08b") == "11111010"
# source: https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Math.html
#   Math.abs(int): if the argument equals Integer.MIN_VALUE the result is that same value, which is negative
print("014 ok")
