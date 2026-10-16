# checks for notes/003-counting-in-binary.md
import datetime
# the table: each 3 bit pattern and its number
for n in range(8):
    p = format(n, "03b")
    assert int(p[0]) * 4 + int(p[1]) * 2 + int(p[2]) * 1 == n == int(p, 2)
assert int("101", 2) == 5
assert 3 * 100 + 4 * 10 + 5 == 345
# patterns: 1 switch makes 2, 2 make 4, 3 make 8
assert [2 ** k for k in (1, 2, 3)] == [2, 4, 8]
# check yourself
assert int("1000", 2) == 8 and format(9, "b") == "1001"
assert 2 ** 3 >= 6 > 2 ** 2 and 2 ** 3 - 6 == 2
assert 2 ** 4 == 16 and int("1111", 2) == 15
# the 2038 bug: 31 counting switches
assert 2 ** 31 - 1 == 2147483647
utc = datetime.timezone.utc
assert datetime.datetime.fromtimestamp(2 ** 31 - 1, utc) == datetime.datetime(2038, 1, 19, 3, 14, 7, tzinfo=utc)
assert datetime.datetime.fromtimestamp(-(2 ** 31), utc).date() == datetime.date(1901, 12, 13)
assert 67.5 < (2 ** 31 - 1) / (365.2425 * 86400) < 68.5
# source: https://en.wikipedia.org/wiki/Year_2038_problem
#   signed 32 bit time overflows at 03:14:07 UTC on 19 January 2038 and
#   wraps to 20:45:52 UTC on 13 December 1901
print("003 ok")
