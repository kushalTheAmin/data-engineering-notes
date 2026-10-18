# 070: flattening nested objects into columns
builds on: [062 CSV, rows and columns separated by commas](./062-csv-rows-and-columns-separated-by-commas.md), [065 the header row, naming the columns](./065-the-header-row-naming-the-columns.md), [066 JSON, records with names on every value](./066-json-records-with-names-on-every-value.md), [068 nesting, records and lists inside records](./068-nesting.md)
section: giving data a shape, part 10, ~2 min read

a [csv](./062-csv-rows-and-columns-separated-by-commas.md) (text, usually one row per line, values split by commas) has no place to put an object inside a row, so where does a customers address go when you save them?

in [068](./068-nesting.md) an [object](./067-json-types.md) (curly braces of name: value pairs) could sit inside another. flattening gives each inner name its own column, glued to the outer name: address and city become address_city. here are 3 customers from the shop (the imaginary snack store these notes run on), a slice of its customers table (i nested the city for this demo, and Eshas is NULL in the table), as nested [JSON](./066-json-records-with-names-on-every-value.md) (records with a name on every value) and then flat:

```text
{"customer_id": 5, "name": "Esha", "address": {}}
{"customer_id": 1, "name": "Asha", "address": {"city": "Jersey City"}}
{"customer_id": 4, "name": "Disha", "address": {"city": "Hoboken"}}
```

| customer_id | name | address_city |
|---|---|---|
| 5 | Esha | |
| 1 | Asha | Jersey City |
| 4 | Disha | Hoboken |

and the loop that does it, one layer deep:

```python
import csv, json, sys
records = [
    '{"customer_id": 5, "name": "Esha", "address": {}}',
    '{"customer_id": 1, "name": "Asha", "address": {"city": "Jersey City"}}',
    '{"customer_id": 4, "name": "Disha", "address": {"city": "Hoboken"}}',
]
rows, header = [], []
for text in records:
    flat = {}
    for key, value in json.loads(text).items():
        if isinstance(value, dict):  # true when the value is an object
            for inner, v in value.items():
                flat[key + "_" + inner] = v
        else:
            flat[key] = value
    rows.append(flat)
    for name in flat:
        if name not in header:
            header.append(name)
# DictWriter writes each dictionary as one csv row; sys.stdout is the screen
out = csv.DictWriter(sys.stdout, fieldnames=header, lineterminator="\n")
out.writeheader()
out.writerows(rows)
```

```output
customer_id,name,address_city
5,Esha,
1,Asha,Jersey City
4,Disha,Hoboken
```

i kept thinking each record could be flattened on its own, and thats the trap. Eshas address is empty, so her row has no address_city. if the [header row](./065-the-header-row-naming-the-columns.md) (the first line, naming the columns) comes from the first record, csv.DictWriter raises an error on Ashas row by default, because it has a column the header never heard of. the header has to be every name from every record, which is why the loop collects it as it goes. the empty cell in the file is just empty text, a csv has no [null](./031-null.md) (a marker for a missing value).

pandas has this built in, pandas.json_normalize, and it glues names with a dot by default (address.city). my loop does one layer only.

### check yourself

1. the shop gets a customer record `{"customer_id": 2, "name": "Bhavin", "address": {"city": "Edison"}, "account": {"joined_on": "2026-01-20"}}` and the header was already built from the 3 customers above. what happens when you write Bhavins flat row with that header?
<details><summary>answer</summary>

the writer raises an error: joined_on becomes account_joined_on, a name not in the header. the header must be rebuilt from every record, including this one, and then the other 3 rows get an empty account_joined_on. the tempting answer is that it quietly drops the extra field, but it raises an error instead.

</details>

2. a flat file has the columns customer_id, name, address_city and address_state. you rebuild the nested record for one row. how many names does the address object need, and why might an empty address_state be a problem?
<details><summary>answer</summary>

two, city and state, so address becomes {"city": ..., "state": ...}. an empty cell could mean the key was missing, held an empty string, or was null, and the flat file cant say which. the tempting answer is that empty means null, but a csv has no null to tell it apart.

</details>

---
prev: [069 JSON lines, one record per line](./069-json-lines.md) | next: [071 exploding lists into many rows](./071-exploding-lists-into-many-rows.md)
