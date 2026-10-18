# checks for notes/064-quotes-inside-quotes-and-newlines-inside-values.md
import csv, io, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
msgs = con.execute("SELECT order_id, message FROM order_messages ORDER BY order_id").fetchall()
assert msgs == [(103, 'less sweet'), (106, 'the "extra crispy" fafda please'), (107, 'call first\nleave at the door')]
b = io.StringIO()
csv.writer(b, lineterminator="\n").writerows(msgs)
text = b.getvalue()
assert text == '103,less sweet\n106,"the ""extra crispy"" fafda please"\n107,"call first\nleave at the door"\n'
assert text.count("\n") == 4          # what wc -l counts
assert len(text.splitlines()) == 4
rows = list(csv.reader(io.StringIO(text)))
assert len(rows) == 3
assert rows[1][1] == 'the "extra crispy" fafda please'
assert rows[2] == ['107', 'call first\nleave at the door']
# check yourself 1
b = io.StringIO()
csv.writer(b, lineterminator="\n").writerow([103, 'less "sweet"'])
assert b.getvalue() == '103,"less ""sweet"""\n'
assert next(csv.reader(io.StringIO('103,"less "sweet""\n')))[1] == 'less sweet""'
# check yourself 2
assert [l.split(",")[0] for l in text.splitlines()] == ['103', '106', '107', 'leave at the door"']
# source: https://docs.python.org/3/library/csv.html
#   confirmed: files should be opened with newline='' or embedded newlines in quoted fields are not read correctly
#   confirmed: doublequote defaults to True, a quotechar inside a field is doubled
#   confirmed: line_num counts lines read, not records, since records can span multiple lines
print("064 ok")
