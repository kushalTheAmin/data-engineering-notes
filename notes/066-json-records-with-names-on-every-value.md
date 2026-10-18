# 066: JSON, records with names on every value
builds on: [062 CSV, rows and columns separated by commas](./062-csv-rows-and-columns-separated-by-commas.md), [065 the header row, naming the columns](./065-the-header-row-naming-the-columns.md)
section: giving data a shape, part 6, ~2 min read

what if every value in a file carried its own label, so nobody ever had to count commas?

a [csv](./062-csv-rows-and-columns-separated-by-commas.md) (text, usually one row per line, values split by commas) usually names its columns once, in a [header row](./065-the-header-row-naming-the-columns.md) on line 1, and [065](./065-the-header-row-naming-the-columns.md) showed code that looks values up by name survives a reordered file. JSON, JavaScript Object Notation, puts the name next to every value instead. a JSON record is curly braces around name: value pairs, the names in double quotes.

here is order 101 from the shop, the imaginary gujarati snack store these notes run on, as a csv line and as JSON, plus the same record with the names reordered:

```text
csv:   101,1,2026-04-01 09:15:00,delivered
json:  {"order_id": 101, "customer_id": 1, "ordered_at": "2026-04-01 09:15:00", "status": "delivered"}
json:  {"status": "delivered", "ordered_at": "2026-04-01 09:15:00", "customer_id": 1, "order_id": 101}
```

json.loads, from pythons json module, reads JSON text and gives back a dictionary:

```python
import json
a = '{"order_id": 101, "customer_id": 1, "ordered_at": "2026-04-01 09:15:00", "status": "delivered"}'
b = '{"status": "delivered", "ordered_at": "2026-04-01 09:15:00", "customer_id": 1, "order_id": 101}'
print(json.loads(a)["status"], json.loads(b)["status"])
print(json.loads(a) == json.loads(b))
print(len("101,1,2026-04-01 09:15:00,delivered"), len(a))
```

```output
delivered delivered
True
35 95
```

the two orderings come back as the same dictionary, so nothing counts positions. i assumed a JSON record was a csv row with extra punctuation, and the part that matters is that you can read one record alone, with no header up top to go find. and 101 has no quotes, so it comes back as a number, unlike splitting a csv, which gives text.

you pay for it. the record is 95 characters against 35 with these spaces, since every record repeats its names. one gotcha: names need double quotes, and single quotes are an error, even though a python dictionary printed with them looks the same.

programs still have to agree on the names, just not the order.

---
prev: [065 the header row, naming the columns](./065-the-header-row-naming-the-columns.md) | next: [067 JSON types, strings, numbers, booleans, null, objects and arrays](./067-json-types.md)
