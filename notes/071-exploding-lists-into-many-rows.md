# 071: exploding lists into many rows
builds on: [066 JSON, records with names on every value](./066-json-records-with-names-on-every-value.md), [068 nesting, records and lists inside records](./068-nesting.md), [070 flattening nested objects into columns](./070-flattening-nested-objects-into-columns.md)
section: giving data a shape, part 11, ~2 min read

order 105 has 3 items and order 106 has 1. how do both fit in a table where every row has the same columns?

[070](./070-flattening-nested-objects-into-columns.md) flattened an [object](./067-json-types.md) (name: value pairs inside a record) into columns, one value per name. a list breaks that, since its length changes: item_1, item_2, item_3 columns would sit empty for every order with fewer items. exploding goes down instead of across. one record with a list becomes one row per list item, and the outer fields get copied onto each row.

here are orders 105 and 106 from the shop (the imaginary gujarati snack store these notes run on), as [JSON](./066-json-records-with-names-on-every-value.md) records (items shortened) and then exploded:

```text
{"order_id": 105, "customer_id": 4, "items": [kaju katli x2, jalebi x2, masala chai x1]}
{"order_id": 106, "customer_id": 1, "items": [khandvi x2]}
```

| order_id | customer_id | product | quantity |
|---|---|---|---|
| 105 | 4 | kaju katli | 2 |
| 105 | 4 | jalebi | 2 |
| 105 | 4 | masala chai | 1 |
| 106 | 1 | khandvi | 2 |

```python
import json
records = [
    '{"order_id": 105, "customer_id": 4, "items": [{"product": "kaju katli", "quantity": 2}, {"product": "jalebi", "quantity": 2}, {"product": "masala chai", "quantity": 1}]}',
    '{"order_id": 106, "customer_id": 1, "items": [{"product": "khandvi", "quantity": 2}]}',
]
rows = []
for text in records:
    order = json.loads(text)  # JSON text to a dictionary
    for item in order["items"]:
        rows.append({"order_id": order["order_id"], "customer_id": order["customer_id"], **item})  # **item copies the items product and quantity in
print(len(records), "records ->", len(rows), "rows")
```

```output
2 records -> 4 rows
```

i kept expecting a row to stand for an order, and after this it stands for an item. order_id 105 now shows up 3 times, so counting rows counts items, and if you want orders you count the different order_ids, each once.

an empty list leaves a hole. the loop above gives that order zero rows, so it vanishes. pandas, a python table library, has this built in as DataFrame.explode, and for an empty list it keeps a row with a missing value instead.

the shops order_items table, one row per item, has this same one-row-per-item shape: 13 rows for 7 orders.

### check yourself

1. all 7 shop orders get exploded, one row per item. a teammate runs len(rows) and calls it orders today. what do they get, and what should they have counted?
<details><summary>answer</summary>

they get 13, the number of items, since order_items has 13 rows. the 7 comes from counting distinct order_id values. the tempting answer is 7, from forgetting that each order now repeats once per item.

</details>

2. a customer opens an order and removes everything before paying, so the record, for a made up order 108, is {"order_id": 108, "customer_id": 2, "items": []}. with the loop above, how many rows does order 108 produce, and what could go wrong in a report?
<details><summary>answer</summary>

zero rows, so order 108 disappears from the output. a report counting orders from the exploded rows would never know it existed. the tempting answer is one row with an empty product, but the inner loop never runs on an empty list.

</details>

---
prev: [070 flattening nested objects into columns](./070-flattening-nested-objects-into-columns.md) | next: not written yet
