# checks for notes/150-percentiles-the-medians-cousins.md
import os, sys
from decimal import Decimal as Dec
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop
con = shop()
q = lambda s: con.sql(s).fetchall()
assert q("SELECT name FROM products WHERE price = 12.00") == [("kaju katli",)]
assert q("SELECT count(*) FROM products") == [(6,)]
prices = sorted([6.00, 7.50, 5.00, 12.00, 3.00, 4.50])
pos = 0.9 * (len(prices) - 1)
low = int(pos)
assert pos == 4.5 and prices[low] == 7.5 and prices[low + 1] == 12.0
assert prices[low] + (pos - low) * (prices[low + 1] - prices[low]) == 9.75
assert 9.75 not in prices
assert round(0.9 * 12.00, 2) == 10.80
assert q("SELECT quantile_cont(price, 0.5), quantile_cont(price, 0.9), quantile_disc(price, 0.9) FROM products") == [(Dec("5.50"), Dec("9.75"), Dec("12.00"))]
assert q("SELECT median(price) FROM products") == [(Dec("5.50"),)]
# check yourself
assert q("SELECT category, quantile_cont(price, 0.9) FROM products WHERE category = 'snack' GROUP BY category") == [("snack", Dec("7.20"))]
assert sorted(p for (p,) in q("SELECT price FROM products WHERE category = 'snack'")) == [Dec("4.50"), Dec("6.00"), Dec("7.50")]
assert Dec("6.00") + Dec("0.8") * (Dec("7.50") - Dec("6.00")) == Dec("7.20") and round(0.9 * 2, 1) == 1.8
assert q("SELECT quantile_cont(x, 0.9) FROM range(1, 11) t(x)") == [(9.1,)] or abs(q("SELECT quantile_cont(x, 0.9) FROM range(1, 11) t(x)")[0][0] - 9.1) < 1e-9
assert round(0.9 * 9, 1) == 8.1
# source: https://duckdb.org/docs/2.0/sql/functions/aggregates.html
# confirmed: quantile_cont returns the pos * (n - 1)th value or an interpolation between adjacent values; quantile_disc picks an actual value of x
# source: https://www.postgresql.org/docs/current/functions-aggregate.html
# confirmed: percentile_cont(fraction) interpolates between adjacent input items if needed, fraction must be between 0 and 1
# source: https://sre.google/sre-book/monitoring-distributed-systems/
# confirmed: section "Worrying About Your Tail" covers the slowest requests; footnote says "the idea that most of your requests are near the mean is just hopeful thinking."
# source: https://www.postgresql.org/docs/current/tutorial-arch.html
# confirmed: "PostgreSQL uses a client/server model", so Postgres is a server database
print("150 ok")
