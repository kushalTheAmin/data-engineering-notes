# 079: a table, rows are records, columns are fields
builds on: [031 null](./031-null.md), [062 CSV, rows and columns separated by commas](./062-csv-rows-and-columns-separated-by-commas.md), [066 JSON, records with names on every value](./066-json-records-with-names-on-every-value.md), [077 required vs optional fields](./077-required-vs-optional-fields.md), [078 capstone, the shop orders as raw text, CSV and JSON side by side](./078-capstone-the-shop-orders-three-ways.md)
section: tables, keys and relationships, part 1, ~2 min read

in [077](./077-required-vs-optional-fields.md) a [JSON](./066-json-records-with-names-on-every-value.md) record (name: value pairs) could just skip Eshas city. try that in a table and you cant, so what goes there instead?

[078](./078-capstone-the-shop-orders-three-ways.md) set csv rows (lines of values split by commas) next to a JSON record. a table is a grid where each row is one record, one thing the data is about, and each column is one field, a fact every row has a spot for. a slice of the customers from the shop, the imaginary gujarati snack store:

| customer_id | name | city | joined_on |
|---|---|---|---|
| 3 | Chirag | Jersey City | 2026-02-11 |
| 4 | Disha | Hoboken | 2026-03-02 |
| 5 | Esha | NULL | 2026-03-15 |

in code, one way to hold it is a list of dictionaries (name: value pairs). a row is one dictionary, a column is the same key in every dictionary:

```python
rows = [
    {"customer_id": 3, "name": "Chirag", "city": "Jersey City", "joined_on": "2026-02-11"},
    {"customer_id": 4, "name": "Disha", "city": "Hoboken", "joined_on": "2026-03-02"},
    {"customer_id": 5, "name": "Esha", "city": None, "joined_on": "2026-03-15"},
]
print(rows[2])
print([r["city"] for r in rows])
print(all(r.keys() == rows[0].keys() for r in rows))
```

```output
{'customer_id': 5, 'name': 'Esha', 'city': None, 'joined_on': '2026-03-15'}
['Jersey City', 'Hoboken', None]
True
```

Eshas row still has a city spot, and it holds [NULL](./031-null.md), the marker for no value (None in python). i expected a missing fact to leave a gap, but the spot is always there, only what sits in it changes. the last line checks the rule: every row has the same keys. a JSON record could drop a name, a table row cant. a plain list wont enforce that, a database table does. only a column that allows NULL can hold it, and name doesnt.

that sameness lets a database table, or a pandas DataFrame (pandas is a python library), pull a whole column in one go. a [csv](./062-csv-rows-and-columns-separated-by-commas.md) is the grid with nothing enforcing it.

what kind of value goes in each spot, text or a number, is next.

---
prev: [078 capstone, the shop orders as raw text, CSV and JSON side by side](./078-capstone-the-shop-orders-three-ways.md) | next: not written yet
