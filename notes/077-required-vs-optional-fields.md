# 077: required vs optional fields
builds on: [031 null](./031-null.md), [066 JSON, records with names on every value](./066-json-records-with-names-on-every-value.md), [075 schema, the agreement about shape](./075-schema.md), [076 data types in a schema](./076-data-types-in-a-schema.md)
section: giving data a shape, part 17, ~2 min read

Esha has no city in the shop, the imaginary gujarati snack store these notes run on. should a customer record without a city get rejected?

depends on what the schema says. a [schema](./075-schema.md), the written agreement on shape, can split its field names in two: required ones must be in every record, optional ones may be left out. 075 rejected any missing name, and this is the finer version. here the schema requires customer_id and name, and city is optional. the records are a slice of the customers table, plus one made up row with no name:

```python
required = ["customer_id", "name"]
records = [
    {"customer_id": 1, "name": "Asha", "city": "Jersey City"},
    {"customer_id": 5, "name": "Esha"},
    {"customer_id": 2, "city": "Edison"},
]
for rec in records:
    missing = [n for n in required if n not in rec]
    print(rec.get("name", "?"), "| missing:", missing, "|", "rejected" if missing else "ok")
```

```output
Asha | missing: [] | ok
Esha | missing: [] | ok
? | missing: ['name'] | rejected
```

the check only looks at the required list, so Esha passes without a city and the nameless record fails. i expected optional to mean the value can be empty, but it means the name can be absent, which is not the same as a [null](./031-null.md), a marker for no value. a [JSON](./066-json-records-with-names-on-every-value.md) record can say "city": null with the name there, or leave city out entirely.

```python
esha = {"customer_id": 5, "name": "Esha"}
print(esha.get("city"))
try:
    print(esha["city"])
except KeyError as e:
    print("KeyError", e)
```

```output
None
KeyError 'city'
```

.get hides the difference and plain lookup crashes on it, and that is how code you write breaks on an optional field, only on the records that skip it. in JSON Schema, properties are not required unless a required list names them, so optional is the default there.

### check yourself

1. an export writes each rating as a record with order_id and stars, and the schema lists both as required. if the exporter writes `{"order_id": 103, "stars": null}`, does the required check pass? what if it drops the null and writes `{"order_id": 103}`? these orders have no stars in the shop:

```sql
SELECT order_id, stars FROM order_ratings WHERE stars IS NULL;
```
<details><summary>answer</summary>

```result
order_id | stars
103 | NULL
107 | NULL
```

the first passes, because the name stars is there, and whether null is allowed is a type question from 076. the second fails, the name is gone. the tempting answer is that both fail since there is no rating, which mixes up a missing value with a missing name.

</details>

2. the shop adds a gift_wrap field and has 7 old orders without it. should the schema require it?
<details><summary>answer</summary>

optional, at least until the old files are rewritten. required would reject all 7 old orders even though nothing is wrong with them. the tempting answer is required, so the data is complete, but that breaks every file written before the change.

</details>

---
prev: [076 data types in a schema](./076-data-types-in-a-schema.md) | next: not written yet
