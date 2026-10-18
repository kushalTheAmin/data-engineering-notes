# 065: the header row, naming the columns
builds on: [054 head and tail, looking at the start and end of a file](./054-head-and-tail.md), [062 CSV, rows and columns separated by commas](./062-csv-rows-and-columns-separated-by-commas.md)
section: giving data a shape, part 5, ~2 min read

two exports (saved copies) of the same 3 orders, and my code says one of them has no delivered orders. no error, nothing broken.

[062](./062-csv-rows-and-columns-separated-by-commas.md) made a column a position in a csv (a text file, one row per line, values split by commas), and the file itself never named one. the header row does: the first line of the file holds the column names instead of an order, and as [054](./054-head-and-tail.md) found, its a line like any other.

a slice of the orders from the shop, the imaginary snack store these notes run on, in two exports. in export a the status is last, in export b it is first. this is what each gives for order 101 (row[3] is the fourth value):

| export | header line | row[3] | row["status"] |
|---|---|---|---|
| a | order_id,customer_id,ordered_at,status | delivered | delivered |
| b | status,order_id,customer_id,ordered_at | 2026-04-01 09:15:00 | delivered |

the code counts delivered orders both ways, the second with DictReader, a csv reader that makes each row a dictionary keyed by the header:

```python
# io.StringIO lets a string stand in for a file; [1:] skips the header line
import csv, io
a = "order_id,customer_id,ordered_at,status\n101,1,2026-04-01 09:15:00,delivered\n102,2,2026-04-01 18:40:00,delivered\n104,3,2026-04-04 08:30:00,cancelled\n"
b = "status,order_id,customer_id,ordered_at\ndelivered,101,1,2026-04-01 09:15:00\ndelivered,102,2,2026-04-01 18:40:00\ncancelled,104,3,2026-04-04 08:30:00\n"
def by_position(text):
    rows = list(csv.reader(io.StringIO(text)))[1:]
    return sum(1 for r in rows if r[3] == "delivered")
def by_name(text):
    return sum(1 for r in csv.DictReader(io.StringIO(text)) if r["status"] == "delivered")
print(by_position(a), by_position(b))
print(by_name(a), by_name(b))
```

```output
2 0
2 2
```

position 3 in export b is the time, so the count is 0 and nothing complains. a lookup by name works on both, if the names match.

i expected the file to mark the header somehow, and it doesnt. nothing in it says line 1 is names; DictReader just assumes it, and the docs say that row is left out of the results. feed it a file with no header and your first order quietly becomes the column names.

a reordered export breaks code that counts positions. the next one puts a name on every value inside the file itself.

---
prev: [064 quotes inside quotes, and newlines inside values](./064-quotes-inside-quotes-and-newlines-inside-values.md) | next: not written yet
