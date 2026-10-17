# 039: a file is a named list of bytes
builds on: [004 bytes, 8 bits and 256 possible values](./004-bytes.md), [006 one byte, two hex digits](./006-one-byte-two-hex-digits.md), [007 text is numbers, one character and one number](./007-text-is-numbers.md), [036 memory vs disk, one forgets and one remembers](./036-memory-vs-disk.md)
section: memory, disks and files, part 5, ~2 min read

you rename order101.csv (a csv, text rows split by commas) to order101.jpg. what changed inside the file? not one byte.

a file is a name plus a list of bytes in order, and the disk from [036](./036-memory-vs-disk.md), storage that keeps bytes without power, holds them. the shop, the imaginary gujarati snack store these notes run on, can have a tiny file with a cut down order 101, `101,delivered`. each [byte](./004-bytes.md), a group of 8 bits, shows in [hex](./006-one-byte-two-hex-digits.md), two digits per byte, with the [character](./007-text-is-numbers.md) it stands for underneath:

```text
name:      order101.csv
position:  0  1  2  3  4  5  6  7  8  9  10 11 12
byte:      31 30 31 2c 64 65 6c 69 76 65 72 65 64
shows:     1  0  1  ,  d  e  l  i  v  e  r  e  d
size:      13 bytes
```

positions count from 0, so position 4 is the d. the name is not in that list, the computer keeps it beside the bytes, along with extras like the size. the .csv at the end is just more letters in the name, a habit that only helps programs guess how to read the bytes.

so the rename changes only the label:

```python
import os, tempfile
path = os.path.join(tempfile.mkdtemp(), "order101.csv")
with open(path, "w") as f:
    f.write("101,delivered")
before = open(path, "rb").read()
os.rename(path, path.replace(".csv", ".jpg"))
after = open(path.replace(".csv", ".jpg"), "rb").read()
print(len(before), before[4], before == after)
```

```output
13 100 True
```

"rb" means read the raw bytes, and 100 is the d, the 64 in hex. a viewer opening the .jpg (a photo format) will likely complain, but only because these bytes arent a photo. i assumed the .csv was part of what made it a csv, and its just a sticker.

a file that wont open is often just read with the wrong guess. many tools skip the name and check the first bytes, a real jpeg starts with ff d8 ff.

folders are next, because files need somewhere to live.

---
prev: [038 1000 or 1024, why your drive looks smaller than the box said](./038-1000-or-1024.md) | next: [040 folders and paths](./040-folders-and-paths.md)
