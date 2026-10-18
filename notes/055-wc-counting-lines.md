# 055: wc, counting lines
builds on: [042 line endings, the invisible characters that break files](./042-line-endings.md), [045 torn writes, what a half finished write leaves behind](./045-torn-writes.md), [049 the terminal, running programs by typing](./049-the-terminal.md), [054 head and tail, looking at the start and end of a file](./054-head-and-tail.md)
section: memory, disks and files, part 21, ~2 min read

a csv holds 7 orders and the terminal says 8 lines. a copy with every row still there says 7. how can a line count be off by one both ways?

wc -l (wc is short for word count) prints how many lines a file has. it just counts the 0a bytes (ten, written in hex), the invisible character called LF that ends a [line](./042-line-endings.md). you run it in the [terminal](./049-the-terminal.md).

here it is on the shop, the imaginary gujarati snack store these notes run on. orders.csv is the header plus 7 orders, and cut.csv is the same rows with the final 0a missing:

```text
$ wc -l orders.csv
8 orders.csv
$ wc -l cut.csv
7 cut.csv
$ wc -l < orders.csv
8
```

the 8 is the header counted as a line, same as [054](./054-head-and-tail.md) found for head. the 7 is the odd one. all 8 rows of text are in cut.csv, but the last one never ends in 0a, so wc doesnt see it as a line. in python:

```python
data = b"106,1,2026-04-08 10:00:00,pending\n107,2,2026-04-09 13:45:00,delivered"
print(data.count(b"\n"), len(data.split(b"\n")))
```

```output
1 2
```

two rows of text, one 0a. i assumed wc counted the lines i can see, and it counts line endings, so a last row without one just isnt there for it.

the third command hands the file over with <, so wc has no name to print, just the number.

this is a quick check on a csv exported from a database: 7 orders plus the header should mean 8 lines. a count one short can be a harmless missing final newline or a [torn write](./045-torn-writes.md), a save cut off partway, and tail can show which.

---
prev: [054 head and tail, looking at the start and end of a file](./054-head-and-tail.md) | next: [056 grep, finding the lines that match](./056-grep-finding-matching-lines.md)
