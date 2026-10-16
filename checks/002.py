# checks for notes/002-bits.md
import itertools
# the loop's patterns: 2, 4, 8
for n, count in ((1, 2), (2, 4), (3, 8)):
    pats = ["".join(p) for p in itertools.product("01", repeat=n)]
    assert len(pats) == count
assert ["".join(p) for p in itertools.product("01", repeat=3)] == ["000", "001", "010", "011", "100", "101", "110", "111"]
# keep doubling: 16, 32, 64, 128, and 8 switches give 256
assert [2 ** k for k in range(4, 9)] == [16, 32, 64, 128, 256]
# a laptop drive of 256 GB (a common small size) holds over 2 trillion bits, so "trillions"
assert 256 * 10 ** 9 * 8 > 2 * 10 ** 12
# a bit having exactly two states is the definition of a bit
print("002 ok")
