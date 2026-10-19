# 076: data types in a schema
builds on: [062 CSV, rows and columns separated by commas](./062-csv-rows-and-columns-separated-by-commas.md), [067 JSON types, strings, numbers, booleans, null, objects and arrays](./067-json-types.md), [075 schema, the agreement about shape](./075-schema.md)
section: giving data a shape, part 16, ~2 min read

double a quantity of 3 and get 33 instead of 6. every name in the record was right, so how did it get past a schema?

because the [schema](./075-schema.md) from 075, the written agreement on which names every record has, only lists names. a data type is the kind of value allowed next to a name, like number or text. the check now asks two things per name: is it there, and is it the right kind. the kinds are the ones [JSON has](./067-json-types.md), a string (text in double quotes) or a number (no quotes).

```text
order_id: number
product:  text
quantity: number
```

here are three versions of one order item from the shop, the imaginary gujarati snack store these notes run on. order 104 had 3 dhokla, a steamed savory cake, so the first row is real and the other two are made up:

| quantity as written | python loads it as (int = whole number, str = text) | schema wants | verdict |
|---|---|---|---|
| 3 | int | number | ok |
| "3" | str | number | rejected |
| "three" | str | number | rejected |

```python
print(3 * 2, "3" * 2)
```

```output
6 33
```

i expected the quote marks to be harmless decoration, and they change what the value is. python repeats text instead of multiplying it, so "3" doubles into 33 with no error anywhere. the names check from 075 passes it, only a type check catches it.

in a [csv](./062-csv-rows-and-columns-separated-by-commas.md) quotes dont carry a kind, every value comes back as text, so there the question you ask becomes whether the text can be read as a number. "3" can, "three" cant.

JSON Schema, the real standard 075 mentioned, has a keyword (a reserved word in the schema file) called type that does this check.

---
prev: [075 schema, the agreement about shape](./075-schema.md) | next: [077 required vs optional fields](./077-required-vs-optional-fields.md)
