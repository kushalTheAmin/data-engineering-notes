# checks for notes/021-storing-money-as-whole-cents.md
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop
con = shop()
# python block
assert repr(sum([0.10] * 3)) == "0.30000000000000004" and sum([0.10] * 3) != 0.30
assert sum([10] * 3) == 30
# 1200 // 100 and 1200 % 100
assert 1200 // 100 == 12 and 1200 % 100 == 0
# query: 6 products, cents are price times 100
rows = con.execute("SELECT name, price, (price * 100)::INTEGER AS cents FROM products").fetchall()
assert len(rows) == 6
assert [r[2] for r in rows] == [600, 750, 500, 1200, 300, 450]
# 32 bit top: 2**31 - 1 cents is 21,474,836.47
assert 2 ** 31 - 1 == 2147483647
assert f"{(2 ** 31 - 1) // 100:,}.{(2 ** 31 - 1) % 100:02d}" == "21,474,836.47"
# quiz 1: 15 percent of 750 is 112.5 cents, // chops to 112
assert 750 * 15 / 100 == 112.5 and 750 * 15 // 100 == 112
# quiz 2: order 105
assert 2 * 1200 + 2 * 500 + 1 * 300 == 3700 and 3700 // 100 == 37 and 3700 % 100 == 0
assert 1200 + 500 + 300 == 2000  # the tempting wrong answer: prices added, quantities forgotten (no other natural total gives 3000)
# a 32 bit INTEGER past the top errors in DuckDB when stored or added (sum() widens to HUGEINT, so an INTEGER total means a stored or added INTEGER)
for q in ("SELECT 2147483647::INTEGER + 1::INTEGER", "SELECT 2147483648::INTEGER"):
    try:
        con.execute(q); raise SystemExit("should have errored")
    except Exception as e:
        assert "Overflow" in str(e) or "out of range" in str(e)
assert con.execute("SELECT 2147483647::BIGINT + 1::BIGINT").fetchone()[0] == 2147483648
# quiz 2 from the shop data itself
assert con.execute("SELECT sum((p.price * 100)::INTEGER * i.quantity) FROM order_items i JOIN products p USING (product_id) WHERE i.order_id = 105").fetchone()[0] == 3700
# source: https://duckdb.org/docs/current/sql/data_types/numeric.html
#   confirmed: INTEGER range is -2^31 to 2^31 - 1, "Attempts to store values outside of the allowed range will result in an error"
# source: https://docs.stripe.com/currencies#zero-decimal
#   confirmed: API amounts are in the minor unit, 1000 charges 10 USD, 10 charges 10 JPY (zero-decimal)
print("021 ok")
