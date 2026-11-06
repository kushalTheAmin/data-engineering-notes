# 335: with, opening and closing things safely
builds on: [039 a file is a named list of bytes](./039-a-file-is-a-named-list-of-bytes.md), [046 writing safely, write a new file then rename it](./046-writing-safely.md), [334 errors in scripts, catching them without hiding them](./334-errors-in-scripts-catching-them-without-hiding-them.md)
section: python for data work, part 11, ~2 min read

i wrote a line to a file, asked for its size in bytes, and python said 0. where did the line go?

with is python opening something, running an indented block, then closing it for you, even when an [exception](./334-errors-in-scripts-catching-them-without-hiding-them.md) (python stopping on a line it cant do) cuts the block short.

the shop, the imaginary gujarati snack store these notes run on, has orders 101 and 102, both delivered. this writes one line to a [file](./039-a-file-is-a-named-list-of-bytes.md), orders.csv, a text file of rows, first without with, then with it and an error:

```python
import os, tempfile

path = os.path.join(tempfile.mkdtemp(), "orders.csv")

f = open(path, "w")
f.write("101,delivered\n")
print("open, file size:", os.path.getsize(path))
f.close()
print("closed, file size:", os.path.getsize(path))

try:
    with open(path, "w") as g:
        g.write("102,delivered\n")
        raise ValueError("bad row")
except ValueError:
    pass
with open(path) as h:
    print("after the error, closed:", g.closed, "file:", h.read().strip())
```

```output
open, file size: 0
closed, file size: 14
after the error, closed: True file: 102,delivered
```

i assumed write put the bytes in the file, but python parks small writes in memory (a write buffer) and sends them when the file closes or the buffer fills, since trips to the disk are slow. the first print shows the gap. in the second part nobody called close, yet the file is closed and the new line is in it, because with closed it on the way out of the error.

the python docs warn that skipping both with and close might leave a write incomplete, even if the program exits successfully. a system also caps how many files one program holds open at once, and past it you get "Too many open files".

with doesnt make a write all or nothing: lines written before an error stay. [046](./046-writing-safely.md) has the all or nothing way, a new file then a rename.

open hands back an object, which is what the next note is about.

---

### check yourself

1. what does this print?
```python
with open("orders.csv", "w") as f:
    f.write("101,delivered\n")
    print(f.closed)
print(f.closed)
```
<details><summary>answer</summary>

```output
False
True
```

inside the block the file is still open, and f still exists after the block (python only scopes names inside functions), now closed. the tempting answer is a NameError on the last line, from expecting f to vanish with the block. it doesnt.

</details>

2. order 105 has kaju katli (a cashew fudge sweet) x2, jalebi x2 and masala chai x1. PRICES below has no jalebi, and this try wraps the whole loop, unlike 334. how many lines does o105.csv hold afterward?
```python
PRICES = {"kaju katli": 12.0, "masala chai": 3.0}
items = [("kaju katli", 2), ("jalebi", 2), ("masala chai", 1)]
try:
    with open("o105.csv", "w") as f:
        for name, qty in items:
            f.write(f"{name},{PRICES[name] * qty}\n")
except KeyError:
    pass
with open("o105.csv") as g:
    print(g.read().strip())
```
<details><summary>answer</summary>

```output
kaju katli,24.0
```

one line. with closes the file on the error, which pushes the kaju katli line out, and nothing after jalebi runs. the tempting answers are 2, from reading jalebi as skipped like in 334, and 0, from expecting a failed write to undo itself. neither happens.

</details>

---
prev: [334 errors in scripts, catching them without hiding them](./334-errors-in-scripts-catching-them-without-hiding-them.md) | next: not written yet
