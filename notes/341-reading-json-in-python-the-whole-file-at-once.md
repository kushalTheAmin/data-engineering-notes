# 341: reading JSON in python, the whole file at once
builds on: [340 reading a csv in python, row by row](./340-reading-a-csv-in-python-row-by-row.md), [335 with, opening and closing things safely](./335-with-opening-and-closing-things-safely.md), [066 JSON, records with names on every value](./066-json-records-with-names-on-every-value.md), [067 JSON types, strings, numbers, booleans, null, objects and arrays](./067-json-types.md), [069 JSON lines, one record per line](./069-json-lines.md)
section: python for data work, part 17, ~2 min read

a [csv reader](./340-reading-a-csv-in-python-row-by-row.md), the tool that hands out a csv file one row at a time, goes empty after one loop. does reading a JSON file do the same?

no. json.load reads the whole file in one go and hands back finished python values, here a list of dictionaries, instead of a reader that walks the file.

the shop, the imaginary gujarati snack store these notes run on, has orders. this writes a slice of 3 as a [JSON](./066-json-records-with-names-on-every-value.md) array (square brackets, records inside) to orders.json, then loads it inside a [with](./335-with-opening-and-closing-things-safely.md) block that closes the file:

```python
import json, os, tempfile

path = os.path.join(tempfile.mkdtemp(), "orders.json")
with open(path, "w") as f:
    f.write('[{"order_id": 101, "customer_id": 1, "status": "delivered"}, {"order_id": 102, "customer_id": 2, "status": "delivered"}, {"order_id": 104, "customer_id": 3, "status": "cancelled"}]')

with open(path) as f:
    orders = json.load(f)

print(type(orders).__name__, len(orders))
print(orders[2])
first = sum(1 for o in orders if o["status"] == "delivered")
second = sum(1 for o in orders if o["status"] == "delivered")
print("delivered:", first, second)
```

```output
list 3
{'order_id': 104, 'customer_id': 3, 'status': 'cancelled'}
delivered: 2 2
```

i expected json.load to hand me a reader like the csv one, but it hands back the finished list, so the second count is 2 again. and order_id came back as a number, where the csv gave text. json keeps its types, as [067](./067-json-types.md) showed.

the price is memory, the working space where your program keeps its data. the whole file sits there before your first loop runs, painful for a huge file of millions of orders. one reason some big exports are [JSON lines](./069-json-lines.md), one record per line, which can be read a line at a time. json.load cant read those whole:

```python
import json
lines = '{"order_id": 105, "status": "delivered"}\n{"order_id": 106, "status": "pending"}\n'
try:
    json.loads(lines)
except json.JSONDecodeError as e:
    print(e)
print([json.loads(line)["order_id"] for line in lines.splitlines()])
```

```output
Extra data: line 2 column 1 (char 41)
[105, 106]
```

json.loads is the same thing for text already in a variable. it sees record 1, then hits line 2, raises an error and hands back nothing. so you parse each line on its own, looping over a real file line by line like the csv reader did.

---
prev: [340 reading a csv in python, row by row](./340-reading-a-csv-in-python-row-by-row.md) | next: [342 environment variables, settings that live outside the code](./342-environment-variables-settings-that-live-outside-the-code.md)
