# 073: YAML, indentation as structure
builds on: [066 JSON, records with names on every value](./066-json-records-with-names-on-every-value.md), [068 nesting, records and lists inside records](./068-nesting.md), [072 XML, the older cousin you will still meet](./072-xml.md)
section: giving data a shape, part 13, ~2 min read

what if a format just dropped every bracket and every closing tag and let the spaces at the start of each line say what sits inside what?

that is YAML, a text format where indentation shows nesting and a dash starts each list item. [XML](./072-xml.md) (values wrapped in opening and closing tags) cost 190 characters for order 103 from the shop, the imaginary gujarati snack store these notes run on. here is the same order, the one [068](./068-nesting.md) walked through, in YAML, and python counting the leading spaces on each line:

```python
lines = [
    "order_id: 103",
    "customer: Asha",
    "items:",
    "  - product: khandvi",
    "    quantity: 1",
    "  - product: masala chai",
    "    quantity: 1",
]
for line in lines:
    spaces = len(line) - len(line.lstrip(" "))  # how many spaces start the line
    print(spaces, line.strip())
print(len("\n".join(lines)), "characters")
```

```output
0 order_id: 103
0 customer: Asha
0 items:
2 - product: khandvi
4 quantity: 1
2 - product: masala chai
4 quantity: 1
113 characters
```

read the spaces column like a map. items: has nothing after its colon, and the lines indented under it belong to it, the same idea as a [JSON array](./067-json-types.md) of objects. each dash is one item in the list, and quantity sits at 4 spaces, lined up with product, because the dash plus its space takes the first 2. thats how the item knows quantity is its own field.

i kept looking for the brackets to know where the list ends, and it ends when a line steps back out to fewer spaces. 113 characters, against 130 for [JSON](./066-json-records-with-names-on-every-value.md) with python spacing.

the gotcha is that spaces are the syntax. the YAML spec says tab characters must not be used in indentation, so a tab that looks like 4 spaces in your editor is simply not allowed.

you will meet YAML mostly as config, the settings files tools read. GitHub Actions workflows are written in it.

---
prev: [072 XML, the older cousin you will still meet](./072-xml.md) | next: not written yet
