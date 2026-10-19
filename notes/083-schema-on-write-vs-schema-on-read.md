# 083: schema on write vs schema on read
builds on: [069 JSON lines, one record per line](./069-json-lines.md), [075 schema, the agreement about shape](./075-schema.md), [080 every column holds one type](./080-every-column-holds-one-type.md), [082 a database, a program that guards your data](./082-a-database-guards-the-data.md)
section: tables, keys and relationships, part 5, ~2 min read

a record says the quantity is "two", in words. one place refuses it the moment it arrives, another stores it happily and blows up weeks later. same data, so what differs?

when the shape gets checked. a [schema](./075-schema.md) is the agreement on shape, and you can enforce it on the way in (schema on write) or only when somebody reads (schema on read). the [database](./082-a-database-guards-the-data.md) program from 082 is the first kind, a plain [JSON lines](./069-json-lines.md) file, one record per line, is the second. one thing to flag, schema here means the rule a whole system follows, not just a files field names like in 075. the shop, the imaginary gujarati snack store these notes run on, sends two lines. the first is a real row, order 104 had 3 dhokla (a steamed savory cake). the second is made up, order 105s quantity of 2 mangled into a word:

| line | schema on write (checked at the door) | schema on read (checked when used) |
|---|---|---|
| 104, quantity 3 | stored | stored |
| 105, quantity "two" | rejected now, sender hears about it | stored, nobody knows |
| later, add up quantities | 3 | crashes on line 105 |

```python
import json
lines = ['{"order_id": 104, "quantity": 3}', '{"order_id": 105, "quantity": "two"}']
try:
    print(sum(json.loads(l)["quantity"] for l in lines))
except TypeError as e:
    print("read failed:", e)
```

```output
read failed: unsupported operand type(s) for +: 'int' and 'str'
```

i expected the schema on read side to have no schema at all. it does, it just lives in the reading code instead of the storage, so every reader has to repeat the check, and the person who finds the bad line is the one least able to fix it.

writing is strict and costs a rejected record up front. reading is loose, so nothing is lost on arrival, which helps when the shape keeps changing. neither is free, the bill just lands somewhere else.

### check yourself

1. an analyst gets the 105 line mangled as above and decides to skip any line they cant read. what does the total for order 105 come out as, against this real total?

```sql
SELECT sum(quantity) AS total FROM order_items WHERE order_id = 105
```
<details><summary>answer</summary>

```result
total
5
```

the skipping total is 3, the dropped line was 2 of the 5, and nothing errors. the tempting answer is that it crashes like the python above, but a reader that skips silently gives a wrong number with no warning.

</details>

2. a phone app adds new event fields every week, and two teams argue whether to check them on write or on read. which would you pick, and what must you add?
<details><summary>answer</summary>

read, keep the raw events so nothing is rejected while the shape keeps moving, but then someone owns a check that runs when reading. the tempting answer is write because strict is safer, but it rejects every event with a new field until the schema is updated.

</details>

---
prev: [082 a database, a program that guards your data](./082-a-database-guards-the-data.md) | next: not written yet
