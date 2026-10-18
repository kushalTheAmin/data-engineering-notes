# checks for notes/062-csv-rows-and-columns-separated-by-commas.md
import csv, io, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
orders = con.execute("SELECT order_id, customer_id, ordered_at, status FROM orders ORDER BY order_id LIMIT 3").fetchall()
text = "".join(f"{a},{b},{c},{d}\n" for a, b, c, d in orders)
assert text == "101,1,2026-04-01 09:15:00,delivered\n102,2,2026-04-01 18:40:00,delivered\n103,1,2026-04-03 12:05:00,delivered\n"
rows = [line.split(",") for line in text.splitlines()]
assert rows[0] == ['101', '1', '2026-04-01 09:15:00', 'delivered']
assert rows[0][0] + rows[1][0] == "101102"
assert int(rows[0][0]) + int(rows[1][0]) == 203
assert list(csv.reader(io.StringIO(text))) == rows            # csv module also returns strings
assert all(isinstance(v, str) for r in rows for v in r)
assert [rows[0][i] for i in (0, 1, 3)] == ['101', '1', 'delivered'] and len(rows[0]) == 4
# source: https://docs.python.org/3/library/csv.html
#   confirmed: the csv module reads rows as lists of strings, and the format has no single well defined standard
try:
    import pandas  # pandas guesses types, so the "some tools guess types" aside is true
    assert pandas.read_csv(io.StringIO(text), header=None)[0].sum() == 306
except ImportError:
    pass
print("062 ok")
