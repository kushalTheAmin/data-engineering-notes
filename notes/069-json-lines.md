# 069: JSON lines, one record per line
builds on: [042 line endings, the invisible characters that break files](./042-line-endings.md), [045 torn writes, what a half finished write leaves behind](./045-torn-writes.md), [055 wc, counting lines](./055-wc-counting-lines.md), [066 JSON, records with names on every value](./066-json-records-with-names-on-every-value.md), [068 nesting, records and lists inside records](./068-nesting.md)
section: giving data a shape, part 9, ~2 min read

a file save gets cut off halfway through 3 orders. as one JSON array (a list in square brackets) you can read 0 of them, as JSON lines you can read 2.

JSON lines is a text file with one whole [JSON](./066-json-records-with-names-on-every-value.md) record (one order, written like a dictionary) on each line, no brackets around the file and no commas between the lines. the [line ending](./042-line-endings.md) is what separates records. here are shop orders 105 to 107 (the shop is the imaginary gujarati snack store these notes run on), both ways, after a [torn write](./045-torn-writes.md), a save cut off partway, ended it:

```text
one array:     [{"order_id": 105, ...}, {"order_id": 106, ...}, {"order_id": 107, "status": "deliv
one per line:  {"order_id": 105, "status": "delivered"}
               {"order_id": 106, "status": "pending"}
               {"order_id": 107, "status": "deliv
```

and python reading each:

```python
import json
array = '[{"order_id": 105, "status": "delivered"}, {"order_id": 106, "status": "pending"}, {"order_id": 107, "status": "deliv'
lines = '{"order_id": 105, "status": "delivered"}\n{"order_id": 106, "status": "pending"}\n{"order_id": 107, "status": "deliv'
try:
    json.loads(array)
except json.JSONDecodeError:
    print("one array: 0 orders")
good = []
for line in lines.split("\n"):
    try:
        good.append(json.loads(line)["order_id"])
    except json.JSONDecodeError:
        print("bad line, skipped:", line)
print("one per line:", good)
```

```output
one array: 0 orders
bad line, skipped: {"order_id": 107, "status": "deliv
one per line: [105, 106]
```

i expected the outer brackets to be harmless, but they make the whole file one record that is only valid once the last byte arrives. with lines every record stands alone, so one bad line costs one record.

it also means [wc -l](./055-wc-counting-lines.md) (a terminal command that counts line endings) counts records, head -n 2 (prints the first 2 lines) shows 2 whole ones, and adding an order is adding a line.

the catch is that a record cant contain a raw line break. json.dumps (python data to JSON text) keeps a newline inside a value as the two characters \n, but pretty printing (indent=2, spreading a record over many lines) breaks the format. a [nested](./068-nesting.md) record still has to fit on its one line.

BigQuery, Googles database for big analytics, wants this when you load JSON files, and calls it newline-delimited.

### check yourself

1. a script writes each of the 7 shop orders with `json.dumps(order, indent=2)`, a line ending after each, into one file. orders have 4 fields (order_id, customer_id, ordered_at, status). what does wc -l print, and is it still JSON lines?
<details><summary>answer</summary>

it prints 42. indent=2 puts the braces and each of the 4 fields on their own line, 6 lines per order, 7 times 6. its not JSON lines anymore, since no single line is a whole record. the tempting answer is 7, from remembering one record per line.

</details>

2. order 107 has the message "call first" then a line break then "leave at the door". a teammate types it into the file by hand, pressing Enter between the two inside the quotes. a reader splits the file on line endings and runs json.loads on each piece. what happens?
<details><summary>answer</summary>

the record is now 2 lines, and each half alone is not valid JSON, so both fail to load. json.dumps would have written the break as the two characters \n and kept it on one line. the tempting answer is that json.loads copes because the quotes are still matched, but it only ever sees one line at a time.

</details>

---
prev: [068 nesting, records and lists inside records](./068-nesting.md) | next: not written yet
