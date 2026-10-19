# 078: capstone, the shop orders as raw text, CSV and JSON side by side
builds on: [055 wc, counting lines](./055-wc-counting-lines.md), [061 structure, why a pile of text is hard to ask questions of](./061-structure-why-text-is-hard-to-ask.md), [062 CSV, rows and columns separated by commas](./062-csv-rows-and-columns-separated-by-commas.md), [063 quoting, commas inside values](./063-quoting-commas-inside-values.md), [064 quotes inside quotes, and newlines inside values](./064-quotes-inside-quotes-and-newlines-inside-values.md), [065 the header row, naming the columns](./065-the-header-row-naming-the-columns.md), [066 JSON, records with names on every value](./066-json-records-with-names-on-every-value.md), [067 JSON types, strings, numbers, booleans, null, objects and arrays](./067-json-types.md), [068 nesting, records and lists inside records](./068-nesting.md), [069 JSON lines, one record per line](./069-json-lines.md), [070 flattening nested objects into columns](./070-flattening-nested-objects-into-columns.md), [071 exploding lists into many rows](./071-exploding-lists-into-many-rows.md), [072 XML, the older cousin you will still meet](./072-xml.md), [073 YAML, indentation as structure](./073-yaml.md), [074 YAML traps, when no means false](./074-yaml-traps.md), [075 schema, the agreement about shape](./075-schema.md), [076 data types in a schema](./076-data-types-in-a-schema.md), [077 required vs optional fields](./077-required-vs-optional-fields.md)
section: giving data a shape, wrap up, ~3 min read

same order, three files. which one can a program actually ask questions of, and what does each one cost you?

[077](./077-required-vs-optional-fields.md) ended on schemas, the written agreement on which names a record must have. that is the top of this whole section, so here is the whole climb on one order. order 103 from the shop, the imaginary gujarati snack store these notes run on: Asha, one khandvi (a rolled savory snack), one masala chai (spiced tea). the same facts, three ways: a plain sentence, a [csv](./062-csv-rows-and-columns-separated-by-commas.md) (rows of values split by commas), and [JSON](./066-json-records-with-names-on-every-value.md) (a record with a name on every value):

```text
raw text  Asha: 1 khandvi, 1 masala chai                                       061
csv       order_id,customer,product,quantity                                   062 to 065
          103,Asha,khandvi,1                                                   070, 071
          103,Asha,masala chai,1
json      {"order_id": 103, "customer": "Asha", "items": [{"product": "khandvi", "quantity": 1}, {"product": "masala chai", "quantity": 1}]}      066 to 069
```

```python
import csv, io, json
csv_text = "order_id,customer,product,quantity\n103,Asha,khandvi,1\n103,Asha,masala chai,1\n"
json_text = '{"order_id": 103, "customer": "Asha", "items": [{"product": "khandvi", "quantity": 1}, {"product": "masala chai", "quantity": 1}]}'
rows = list(csv.DictReader(io.StringIO(csv_text)))
order = json.loads(json_text)
print(len(rows), "csv rows,", len([order]), "json record")
print(sum(int(r["quantity"]) for r in rows), sum(i["quantity"] for i in order["items"]))
```

```output
2 csv rows, 1 json record
2 2
```

the sentence needs guessing, the other two answer with a lookup by name. csv needed int(), because splitting a line gives text, JSON already had a number. and csv spent 2 rows on one order, because a row has no room for a list inside it.

every step in between was one fix for one way the last shape broke:

| what broke | the fix | notes |
|---|---|---|
| a sentence has no agreed spots | structure, then csv rows | [061](./061-structure-why-text-is-hard-to-ask.md) [062](./062-csv-rows-and-columns-separated-by-commas.md) |
| a comma or line break inside a value | csv quoting | [063](./063-quoting-commas-inside-values.md) [064](./064-quotes-inside-quotes-and-newlines-inside-values.md) |
| positions drift when columns move | a header row, then names on every value, with six kinds | [065](./065-the-header-row-naming-the-columns.md) [066](./066-json-records-with-names-on-every-value.md) [067](./067-json-types.md) |
| a list or object needs a home | nesting, flattening, exploding | [068](./068-nesting.md) [070](./070-flattening-nested-objects-into-columns.md) [071](./071-exploding-lists-into-many-rows.md) |
| a cut off file loses everything | one record per line | [069](./069-json-lines.md) |
| the same record in other clothes | XML tags, YAML indentation, and its traps | [072](./072-xml.md) [073](./073-yaml.md) [074](./074-yaml-traps.md) |
| valid text, wrong shape | schema, types, required vs optional | [075](./075-schema.md) [076](./076-data-types-in-a-schema.md) [077](./077-required-vs-optional-fields.md) |

i expected these to be rivals, and they are one agreement written down in different places, in a header, on every value, or in a separate schema. so what changes is where the names live and what a broken file costs you.

a loader, the code that reads the file, checks the text of any of the three, not the shape. a schema is what checks the shape.

the next section gives these rows a home where a table is the whole point.

### check yourself

1. orders 105, 106 and 107 have 3, 1 and 2 items. they get saved two ways, one JSON lines file with each order and its items inside, and one csv with one row per item, no header. how many lines does each file have?
<details><summary>answer</summary>

the csv has 6 lines, 3 plus 1 plus 2, and the JSON lines file has 3, one per order. the tempting answer is 3 for both, from remembering one record per line.

</details>

2. the 3 delivery messages (103, 106, 107) are saved as JSON lines with json.dumps, pythons JSON writer, a line ending after each. JSON text cant hold a raw line break inside a value, so the writer puts the two characters \n there instead. [wc -l](./055-wc-counting-lines.md), the line counter, counts line endings. what does it print, given that [064](./064-quotes-inside-quotes-and-newlines-inside-values.md) found 4 for the same messages as csv?
<details><summary>answer</summary>

it prints 3, because the line break inside 107s message becomes \n and each record stays on one line. csv keeps the real break inside its quotes, which is why that count was 4. the tempting answer is 4, from copying the csv count without noticing JSON writes the break differently.

</details>

---
prev: [077 required vs optional fields](./077-required-vs-optional-fields.md) | next: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md)
