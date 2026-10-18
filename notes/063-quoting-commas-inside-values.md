# 063: quoting, commas inside values
builds on: [062 CSV, rows and columns separated by commas](./062-csv-rows-and-columns-separated-by-commas.md)
section: giving data a shape, part 3, ~2 min read

what happens to a csv row (a line of values split by commas) when the value itself has a comma in it? order 101 at the shop, the imaginary gujarati snack store these notes run on, came with the note "extra chutney, less spicy", and a row that should have two values suddenly has three.

[062](./062-csv-rows-and-columns-separated-by-commas.md) split each line on commas, so a comma inside a value looks exactly like a separator. quoting fixes it: wrap the value in double quotes, and a csv reader treats everything until the closing quote as one value. here is a slice of the notes, 3 rows, as the file holds them and as each method reads them:

| line in the file | split on commas | csv reader |
|---|---|---|
| 101,"extra chutney, less spicy" | 3 values | 2 values |
| 102,no nuts | 2 values | 2 values |
| 105,"gift, please wrap" | 3 values | 2 values |

```python
# io.StringIO lets a string stand in for a file; csv.reader is python's csv reader
import csv, io
line = '101,"extra chutney, less spicy"\n'
print(line.strip().split(","))
print(next(csv.reader(io.StringIO(line))))
```

```output
['101', '"extra chutney', ' less spicy"']
['101', 'extra chutney, less spicy']
```

look at the first line of output. the quote marks stay glued to the pieces, and the space after the comma too. i assumed the quotes were part of the value, but they are only a fence, and the reader takes them off.

row 102 has no quotes and nothing breaks, because writers usually quote only when a value needs it. python does this by default, so a clean row tells you nothing about the rest.

a naive split drifts quietly: any column after the note shifts one position right, and no error ever fires.

but what if the value contains a quote mark itself? that is the next one.

### check yourself

1. order 105s note is written into a file as `105,gift, please wrap` with no quotes. how many values does a csv reader return for that line, and what is the second one?
<details><summary>answer</summary>

3 values: `105`, `gift` and ` please wrap`, with a leading space. the reader cant guess the comma was meant as text, only quotes tell it that. the tempting answer is 2, reading the line the way a person would.

</details>

2. you build each line by hand as f"{order_id},{note}" for the three notes above. which lines come out broken?
<details><summary>answer</summary>

orders 101 and 105, because their notes contain a comma. 102, "no nuts", is fine. the tempting answers are all three or only 101, from assuming the problem is the shop data or the first row. only a value containing a comma breaks.

</details>

---
prev: [062 CSV, rows and columns separated by commas](./062-csv-rows-and-columns-separated-by-commas.md) | next: [064 quotes inside quotes, and newlines inside values](./064-quotes-inside-quotes-and-newlines-inside-values.md)
