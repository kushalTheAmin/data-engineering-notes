# 075: schema, the agreement about shape
builds on: [065 the header row, naming the columns](./065-the-header-row-naming-the-columns.md), [066 JSON, records with names on every value](./066-json-records-with-names-on-every-value.md), [074 YAML traps, when no means false](./074-yaml-traps.md)
section: giving data a shape, part 15, ~2 min read

a file of orders loads with no error and some statuses come back empty. who was supposed to catch that?

nobody, unless something wrote down the expected shape. a parser, the code that reads a file, only checks the syntax, that the text is well formed: json.loads from [066](./066-json-records-with-names-on-every-value.md) accepts any valid [JSON](./066-json-records-with-names-on-every-value.md), right shape or not (and [074](./074-yaml-traps.md) showed one deciding what a value means). a schema is the written down agreement, kept apart from the data, on which field names (the keys) every record (one order) must have.

a [csv header](./065-the-header-row-naming-the-columns.md) only says what this file has, not what it should have. here is a schema for the shop, the imaginary gujarati snack store these notes run on, checked against three simplified order records. the schema is just three names, order_id, customer, status:

| order | field names in the record | missing | extra | verdict |
|---|---|---|---|---|
| 101 | order_id, customer, status | none | none | ok |
| 104 | order_id, customer, state | status | state | rejected |
| 105 | order_id, customer, status, gift_wrap | none | gift_wrap | rejected |

the check is a plain loop:

```text
for each record:
    missing = names in the schema that the record lacks
    extra   = names in the record that the schema lacks
    if missing or extra: reject the record
```

order 104 is the sneaky one, and it is the empty status from the start. someone renamed status to state, the file is still valid, and code you write that looks up status gets nothing, or an error. the schema rejects it. order 105: a schema also decides about extras. this one refuses them, another could allow them.

i assumed loading a file without an error meant it was fine, and the loader only checks syntax, not shape. JSON Schema is a real written specification for writing this down for JSON files.

what each value should look like, text or number, comes next.

---
prev: [074 YAML traps, when no means false](./074-yaml-traps.md) | next: [076 data types in a schema](./076-data-types-in-a-schema.md)
