# 059: redirecting output into a file
builds on: [046 writing safely, write a new file then rename it](./046-writing-safely.md), [049 the terminal, running programs by typing](./049-the-terminal.md), [056 grep, finding the lines that match](./056-grep-finding-matching-lines.md), [057 standard input and output, how programs pass text along](./057-standard-input-and-output.md), [058 pipes, chaining small programs together](./058-pipes.md)
section: memory, disks and files, part 25, ~2 min read

i want only the delivered orders kept in orders.csv, so i type grep delivered orders.csv > orders.csv. do you think the file ends up with the 5 delivered lines?

a redirect, written >, sends the stdout of a program ([057](./057-standard-input-and-output.md), the channel it writes to) into a file instead of the [terminal](./049-the-terminal.md) screen. the shell, the program that runs your line, does the swap, so [grep](./056-grep-finding-matching-lines.md) never knows. a missing file is created, and an existing one is emptied first.

here is the shop, the imaginary gujarati snack store these notes run on, with its 8 line orders.csv:

| command | orders.csv after | delivered.csv after |
| --- | --- | --- |
| (start) | 8 lines | does not exist |
| grep delivered orders.csv > delivered.csv | 8 lines | 5 lines |
| grep delivered orders.csv > orders.csv | 0 lines | 5 lines, untouched |

the shell opens the file for writing before it starts grep, and opening for writing empties it. so grep reads an empty file and finds nothing. python does the same:

```python
import os, tempfile
path = os.path.join(tempfile.mkdtemp(), "orders.csv")
with open(path, "w") as f:
    f.write("order_id,customer_id,ordered_at,status\n" + "101,1,x,delivered\n" * 7)
print(len(open(path).readlines()))
f = open(path, "w")
print(len(open(path).readlines()))
```

```output
8
0
```

i assumed the command ran first and the file got touched after, and its the other way round. the second open "w" is what the shell does, before any reading happens.

this is the same worry as [046](./046-writing-safely.md): > writes into the old file with no undo. send the result to a new name, check it, then rename it over the old one.

---
prev: [058 pipes, chaining small programs together](./058-pipes.md) | next: [060 capstone, the life of one saved order, memory to disk and back](./060-capstone-the-life-of-one-saved-order.md)
