# checks for notes/063-quoting-commas-inside-values.md
import csv, io, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
notes = con.execute("SELECT order_id, note FROM order_notes ORDER BY order_id").fetchall()
assert notes == [(101, 'extra chutney, less spicy'), (102, 'no nuts'), (105, 'gift, please wrap')]
b = io.StringIO()
w = csv.writer(b, lineterminator="\n")
for o, n in notes:
    w.writerow([o, n])
lines = b.getvalue().splitlines()
assert lines == ['101,"extra chutney, less spicy"', '102,no nuts', '105,"gift, please wrap"']
assert [len(l.split(",")) for l in lines] == [3, 2, 3]
assert [len(next(csv.reader(io.StringIO(l)))) for l in lines] == [2, 2, 2]
line = '101,"extra chutney, less spicy"\n'
assert line.strip().split(",") == ['101', '"extra chutney', ' less spicy"']
assert next(csv.reader(io.StringIO(line))) == ['101', 'extra chutney, less spicy']
# check yourself 1
assert next(csv.reader(io.StringIO("105,gift, please wrap\n"))) == ['105', 'gift', ' please wrap']
# check yourself 2: hand built f"{order_id},{note}" breaks where the note has a comma
broken = [o for o, n in notes if len(f"{o},{n}".split(",")) != 2]
assert broken == [101, 105]
# source: https://docs.python.org/3/library/csv.html
#   confirmed: QUOTE_MINIMAL, the writer default, quotes only fields containing special characters such as the delimiter
print("063 ok")
