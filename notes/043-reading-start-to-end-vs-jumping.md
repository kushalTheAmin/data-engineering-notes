# 043: reading start to end vs jumping to a spot
builds on: [037 disk is slow, memory vs SSD vs spinning disk in real numbers](./037-disk-is-slow.md), [039 a file is a named list of bytes](./039-a-file-is-a-named-list-of-bytes.md), [042 line endings, the invisible characters that break files](./042-line-endings.md)
section: memory, disks and files, part 9, ~2 min read

you want the 6th order in a file. can the computer just go there, like list[5]?

there are two ways to reach a spot. reading start to end takes the bytes in order from position 0. jumping asks for a position directly, which python calls seek. [037](./037-disk-is-slow.md) priced a lookup, one value from a random spot, at 10 milliseconds on a spinning disk, and a jump is that kind.

the catch is knowing the position. here is the shop, the imaginary gujarati snack store these notes run on, as a file with one `order_id,status` line per order, each ending in the 0a of [042](./042-line-endings.md). positions count from 0, like in [039](./039-a-file-is-a-named-list-of-bytes.md), a file being a named list of bytes:

| line | text | starts at | bytes with 0a |
|---|---|---|---|
| 1 | 101,delivered | 0 | 14 |
| 2 | 102,delivered | 14 | 14 |
| 3 | 103,delivered | 28 | 14 |
| 4 | 104,cancelled | 42 | 14 |
| 5 | 105,delivered | 56 | 14 |
| 6 | 106,pending | 70 | 12 |
| 7 | 107,delivered | 82 | 14 |

line 6 starts at 70 only because lines 1 to 5 are 14 each. pending is shorter, so line 7 starts at 82, not 84. try jumping to line 7, first with a guess of 14 bytes per line, then to 82:

```python
import io
rows = ["101,delivered", "102,delivered", "103,delivered", "104,cancelled",
        "105,delivered", "106,pending", "107,delivered"]
data = ("\n".join(rows) + "\n").encode()
f = io.BytesIO(data)
f.seek(14 * 6)
print(f.readline())
f.seek(82)
print(f.readline())
```

```output
b'7,delivered\n'
b'107,delivered\n'
```

the guess landed mid line. nothing in the file lists where lines begin, so the only way to find line 6 is to read lines 1 to 5 and count the 0a bytes. i expected a file to act like a list, and it doesnt, because lines have no fixed size.

so line 1,000,000 of a big csv means reading the 999,999 before it. you can jump only when you already know the position, and keeping track of positions is a job for a later note.

### check yourself

1. the same 7 lines are saved with CRLF endings. you jump straight to the start of line 6. which position?
<details><summary>answer</summary>

```python
print(5 * (14 + 1))
```

```output
75
```
position 75, since each of the first five lines is 14 bytes plus one extra 0d. the tempting answer is 70, copied from the table, but that table was LF.

</details>

2. a log has 1 million lines, and every single line is exactly 20 bytes with its ending. to read line 500000, do you read the 499999 before it, or jump?
<details><summary>answer</summary>

```python
print(499999 * 20)
```

```output
9999980
```
jump to position 9999980. every line is the same size, so the position is just arithmetic. the tempting answer is to read through, which only holds when line sizes vary.

</details>

---
prev: [042 line endings, the invisible characters that break files](./042-line-endings.md) | next: [044 disks read in blocks, never single bytes](./044-disks-read-in-blocks.md)
