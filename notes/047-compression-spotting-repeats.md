# 047: compression, making files smaller by spotting repeats
builds on: [004 bytes, 8 bits and 256 possible values](./004-bytes.md), [039 a file is a named list of bytes](./039-a-file-is-a-named-list-of-bytes.md), [046 writing safely, write a new file then rename it](./046-writing-safely.md)
section: memory, disks and files, part 13, ~2 min read

a file listing the shops order statuses says `delivered` again and again. why store the same word five times? [046](./046-writing-safely.md) copied every byte of such a file.

compression is storing the same information in fewer [bytes](./004-bytes.md) (here one byte is one character), so you can rebuild the original exactly. the simplest version is run length encoding: a run is the same value repeated back to back, and you store the value once with a count.

the shop, the imaginary gujarati snack store these notes run on, has 7 orders, 101 to 107, and each has a status. each status is a line of text in a [file](./039-a-file-is-a-named-list-of-bytes.md), ending with a newline character, which is one byte too. each run becomes `count,word` plus a newline:

```python
statuses = ["delivered", "delivered", "delivered", "cancelled", "delivered", "pending", "delivered"]

def rle(items):
    runs = []
    for x in items:
        if runs and runs[-1][0] == x:
            runs[-1][1] += 1
        else:
            runs.append([x, 1])
    return runs

for label, data in [("as ordered", statuses), ("sorted", sorted(statuses))]:
    runs = rle(data)
    raw = len("".join(s + "\n" for s in data))
    packed = len("".join(f"{n},{s}\n" for s, n in runs))
    print(f"{label:10} {len(runs)} runs {raw} bytes -> {packed} bytes")
```

```output
as ordered 5 runs 68 bytes -> 58 bytes
sorted     3 runs 68 bytes -> 34 bytes
```

in the original order the lone `cancelled` breaks the run, so only 10 bytes saved. sorted, the five delivered sit together, 3 runs, half the size. the catch is that sorting loses which order had which status, so it only works if you keep the order ids somewhere else.

i expected compression to always shrink things, and it doesnt. a run of one costs `1,cancelled`, 12 bytes against 10 for the bare word. no repeats, bigger file.

Parquet, a file format for storing big tables, uses run length encoding to store repeated values, and a column of a table that holds mostly one word is where it shines. the next one is about what this costs.

---
prev: [046 writing safely, write a new file then rename it](./046-writing-safely.md) | next: not written yet
