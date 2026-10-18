# 064: quotes inside quotes, and newlines inside values
builds on: [042 line endings, the invisible characters that break files](./042-line-endings.md), [055 wc, counting lines](./055-wc-counting-lines.md), [062 CSV, rows and columns separated by commas](./062-csv-rows-and-columns-separated-by-commas.md), [063 quoting, commas inside values](./063-quoting-commas-inside-values.md)
section: giving data a shape, part 4, ~2 min read

a csv file (text, one row per line, values split by commas) with 3 orders in it, and `wc -l`, the line counter, says 4. nothing is broken, so who is lying?

[063](./063-quoting-commas-inside-values.md) said double quotes around a value are a fence the reader removes, so commas inside stay text. 063 left two cases open. a quote mark inside the fence is written twice, and a reader turns `""` back into one `"`. a [line ending](./042-line-endings.md) inside the fence is just more of the value, not the end of the row.

here is a slice of the delivery messages from the shop, the imaginary gujarati snack store these notes run on, as the file holds them:

```text
103,less sweet
106,"the ""extra crispy"" fafda please"
107,"call first
leave at the door"
```

```python
import csv, io
text = '103,less sweet\n106,"the ""extra crispy"" fafda please"\n107,"call first\nleave at the door"\n'
print(len(text.splitlines()))
rows = list(csv.reader(io.StringIO(text)))
print(len(rows))
print(rows[1][1])
print(rows[2])
```

```output
4
3
the "extra crispy" fafda please
['107', 'call first\nleave at the door']
```

in [062](./062-csv-rows-and-columns-separated-by-commas.md) i said one row per line, and the fuller picture is that its usually true. i kept treating a line and a row as the same thing, and they arent. order 107 is one row spread over 2 lines, so [wc -l](./055-wc-counting-lines.md), which counts the invisible line endings, says 4 for 3 rows. the safe rule: only a reader that tracks the quotes can say where a row ends.

this bites in practice, and you often get no error at all. the python csv docs say to open files with newline="" so embedded newlines are read correctly, and splitting a big export on lines can cut a row in half.

### check yourself

1. a message for order 103 is `less "sweet"`, quote marks included. what does a csv writer put in the file for that row?
<details><summary>answer</summary>

`103,"less ""sweet"""`. the value has quotes in it, so it gets fenced, and each inner quote is doubled; the last three quotes are the doubled one and the closing fence. the tempting answer is `103,less "sweet"`, which python reads back fine but the writer does not produce by default, or `103,"less "sweet""`, which is fenced but not doubled and silently reads back wrong. a backslash version is what some other tools use, but not the python csv default.

</details>

2. a script reads the messages file above with `for line in file` and takes each line split on the first comma as the order id. which ids does it print?
<details><summary>answer</summary>

103, 106, 107 and then `leave at the door"`, a fourth "id". the second line of order 107s message is a line on its own, and it has no comma, so the whole line comes back. the tempting answer is 103, 106, 107, from thinking one row is one line.

</details>

---
prev: [063 quoting, commas inside values](./063-quoting-commas-inside-values.md) | next: [065 the header row, naming the columns](./065-the-header-row-naming-the-columns.md)
