# 062: CSV, rows and columns separated by commas
builds on: [041 text files vs binary files](./041-text-files-vs-binary-files.md), [042 line endings, the invisible characters that break files](./042-line-endings.md), [061 structure, why a pile of text is hard to ask questions of](./061-structure-why-text-is-hard-to-ask.md)
section: giving data a shape, part 2, ~2 min read

add the first two order ids read from a csv in python and you get 101102, not 203.

[061](./061-structure-why-text-is-hard-to-ask.md) said structure is an agreement on where each fact sits. the usual agreement for rows like those is CSV, comma separated values: a [text file](./041-text-files-vs-binary-files.md), one row per [line](./042-line-endings.md), the values in a row split by commas, so a column is just a position. the orders.csv from before was already one.

here is a slice of the orders from the shop, the imaginary gujarati snack store these notes run on, as the file holds them and then as python sees each line after splitting on commas:

```text
file:    101,1,2026-04-01 09:15:00,delivered
python:  ["101", "1", "2026-04-01 09:15:00", "delivered"]
         position 0 = order id, 1 = customer id, 2 = time, 3 = status
```

a table is a list of rows, so reading a csv gives you a list of lists, one inner list per line:

```python
text = "101,1,2026-04-01 09:15:00,delivered\n102,2,2026-04-01 18:40:00,delivered\n103,1,2026-04-03 12:05:00,delivered\n"
rows = [line.split(",") for line in text.splitlines()]
print(rows[0])
print(rows[0][0] + rows[1][0])
print(int(rows[0][0]) + int(rows[1][0]))
```

```output
['101', '1', '2026-04-01 09:15:00', 'delivered']
101102
203
```

look at the quotes around 101. i expected a number to come back as a number, but the file only holds characters, so every value arrives as text, dates included. adding two strings glues them, which is where 101102 came from. turning "101" into an int is your job.

python has a csv module for this, and its reader hands back lists of strings the same way. one honest caveat: csv has no single strict standard, just a common habit, so files from different programs can differ in small ways.

---
prev: [061 structure, why a pile of text is hard to ask questions of](./061-structure-why-text-is-hard-to-ask.md) | next: [063 quoting, commas inside values](./063-quoting-commas-inside-values.md)
