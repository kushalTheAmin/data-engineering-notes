# 068: nesting, records and lists inside records
builds on: [062 CSV, rows and columns separated by commas](./062-csv-rows-and-columns-separated-by-commas.md), [066 JSON, records with names on every value](./066-json-records-with-names-on-every-value.md), [067 JSON types, strings, numbers, booleans, null, objects and arrays](./067-json-types.md)
section: giving data a shape, part 8, ~2 min read

where do the items of an order go in a csv row? order 103 has 2 items, order 105 has 3, and a row has the same columns every time.

in [067](./067-json-types.md) a JSON record held an object (curly braces, name: value pairs) and an array (square brackets, values in order) as values. nesting is those two sitting inside each other, layer on layer. an array can hold objects, and an object can hold arrays.

here is order 103 from the shop, the imaginary gujarati snack store these notes run on, with each item now an object that carries its quantity. the code reaches "masala chai" one layer per step:

```python
import json
text = '{"order_id": 103, "customer": {"name": "Asha", "city": "Jersey City"}, "items": [{"product": "khandvi", "quantity": 1}, {"product": "masala chai", "quantity": 1}]}'
step = json.loads(text)
for key in ["items", 1, "product"]:
    step = step[key]
    print(key, "->", step)
```

```output
items -> [{'product': 'khandvi', 'quantity': 1}, {'product': 'masala chai', 'quantity': 1}]
1 -> {'product': 'masala chai', 'quantity': 1}
product -> masala chai
```

every step is either a name, to go into an object, or a position counting from 0, to go into an array. i expected nesting to need new syntax, and its the same two lookups you already know from a python dictionary and list, one per layer.

in the shop those items live in their own table, order_items, 13 rows tied to orders by order_id. a flat [csv](./062-csv-rows-and-columns-separated-by-commas.md) (text, usually one row per line) has no clean place for them, so a JSON record carries them inside the order instead.

the catch is that sizes differ. order 105 has 3 items, so items 2 exists there and raises an IndexError on 103. code that walks a nested record has to expect that.

---
prev: [067 JSON types, strings, numbers, booleans, null, objects and arrays](./067-json-types.md) | next: [069 JSON lines, one record per line](./069-json-lines.md)
