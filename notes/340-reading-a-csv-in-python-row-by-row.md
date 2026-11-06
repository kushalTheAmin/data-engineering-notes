# 340: reading a csv in python, row by row
builds on: [335 with, opening and closing things safely](./335-with-opening-and-closing-things-safely.md), [065 the header row, naming the columns](./065-the-header-row-naming-the-columns.md), [064 quotes inside quotes, and newlines inside values](./064-quotes-inside-quotes-and-newlines-inside-values.md), [062 CSV, rows and columns separated by commas](./062-csv-rows-and-columns-separated-by-commas.md)
section: python for data work, part 16, ~2 min read

i looped over a csv to count delivered orders, looped again, and the second loop found nothing. the file hadnt changed.

reading a csv row by row means python opens the file and a csv reader, an object that remembers its place in the file like a bookmark, hands you one row at a time, and only once.

the shop, the imaginary gujarati snack store these notes run on, has orders. this writes a slice of 3 to orders.csv (a [csv](./062-csv-rows-and-columns-separated-by-commas.md) is a text file, usually one row per line), then reads it back with DictReader ([065](./065-the-header-row-naming-the-columns.md)), which makes each row a dictionary keyed by the header line, inside a [with](./335-with-opening-and-closing-things-safely.md) block that closes the file:

```python
import csv, os, tempfile

# make a temp file
path = os.path.join(tempfile.mkdtemp(), "orders.csv")
with open(path, "w", newline="") as f:
    f.write("order_id,customer_id,ordered_at,status\n101,1,2026-04-01 09:15:00,delivered\n102,2,2026-04-01 18:40:00,delivered\n104,3,2026-04-04 08:30:00,cancelled\n")

with open(path, newline="") as f:
    reader = csv.DictReader(f)
    delivered = 0
    for row in reader:
        if row["status"] == "delivered":
            delivered += 1
    print(row)
    print("delivered:", delivered)
    # count the rows still left to read
    print("second loop:", sum(1 for _ in reader))
```

```output
{'order_id': '104', 'customer_id': '3', 'ordered_at': '2026-04-04 08:30:00', 'status': 'cancelled'}
delivered: 2
second loop: 0
```

every value in that last row is text, even order_id, as [062](./062-csv-rows-and-columns-separated-by-commas.md) found, so int("104"), turning text into a number, is your job. and the second loop sees 0 because the reader only walks forward. i assumed the reader was a list of rows i could loop over as often as i liked, but it holds no rows at all, only its place in the file, and the loop used it up.

newline="" in open is what the python docs ask for with csv files, so a line break inside a quoted value ([064](./064-quotes-inside-quotes-and-newlines-inside-values.md)) stays part of that value.

the payoff is memory, where your program keeps its data. a loop holds one row at a time, so a huge file still reads, while list(reader), which collects every row, holds them all at once.

---
prev: [339 decorators, the @ shorthand for wrapping a function](./339-decorators-the-at-shorthand-for-wrapping-a-function.md) | next: not written yet
