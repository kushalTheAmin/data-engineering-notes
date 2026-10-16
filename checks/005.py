# checks for notes/005-hexadecimal.md
# the table: 0 to 15 in decimal, binary and hex
table = ["0000","0001","0010","0011","0100","0101","0110","0111","1000","1001","1010","1011","1100","1101","1110","1111"]
for n in range(16):
    assert format(n, "04b") == table[n] and format(n, "x") == "0123456789abcdef"[n]
assert format(10, "x") == "a" and format(15, "x") == "f"
# 4 bits: 2 times 2 times 2 times 2 patterns
assert 2 * 2 * 2 * 2 == 16 == 2 ** 4
# hex 64 is 6 sixteens plus 4 ones
assert 6 * 16 + 4 == 100 == int("64", 16)
assert ord("d") == 100
# hex 10 means sixteen; python marks hex with 0x
assert int("10", 16) == 16 and hex(100) == "0x64"
# source: https://git-scm.com/docs/gittutorial-2/2.12.5
#   every git object is named by a 40 digit hex SHA-1, and short prefixes work
print("005 ok")
