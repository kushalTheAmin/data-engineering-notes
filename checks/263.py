# checks for notes/263-choosing-column-types-by-what-you-do-with-the-value.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# 3 phones, last 4 as text and as number
assert q("SELECT right(phone, 4), CAST(right(phone, 4) AS INTEGER) FROM customer_contacts ORDER BY customer_id") == [('0101', 101), ('0102', 102), ('0104', 104)]
# Bhavin is customer 2, his phone ends 0102
assert q("SELECT right(phone, 4) FROM customer_contacts WHERE customer_id = 2") == [('0102',)]
assert int('0102') == 102 and str(int('0102')) == '102'
# average of 101, 102, 104 is 102.33
assert round((101 + 102 + 104) / 3, 2) == 102.33
assert round(q("SELECT avg(CAST(right(phone, 4) AS INTEGER)) FROM customer_contacts")[0][0], 2) == 102.33
# 32 bit max and a 10 digit number that does not fit
assert 2**31 - 1 == 2147483647
assert 9876543210 > 2147483647
try:
    q("SELECT CAST('9876543210' AS INTEGER)")
    assert False
except Exception as e:
    assert 'Conversion' in str(e)
# check yourself 1: no row survives the round trip
assert q("SELECT count(*) FROM customer_contacts WHERE CAST(CAST(right(phone, 4) AS INTEGER) AS VARCHAR) = right(phone, 4)") == [(0,)]
# check yourself 2: 007 as a number is 7
assert str(int('007')) == '7'
