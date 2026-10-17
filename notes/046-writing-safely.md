# 046: writing safely, write a new file then rename it
builds on: [039 a file is a named list of bytes](./039-a-file-is-a-named-list-of-bytes.md), [040 folders and paths](./040-folders-and-paths.md), [044 disks read in blocks, never single bytes](./044-disks-read-in-blocks.md), [045 torn writes, what a half finished write leaves behind](./045-torn-writes.md)
section: memory, disks and files, part 12, ~2 min read

if any write can tear (get cut off partway), how does anything ever update a file safely? [045](./045-torn-writes.md) left the shops orders file reading `106,deliveg`, and the fix is to never write into the old file at all.

the safe way: write the whole new version to a temporary file in the same [folder](./040-folders-and-paths.md), then rename it over the old name. a rename just changes which [file](./039-a-file-is-a-named-list-of-bytes.md) a name points at, and on linux it is atomic, meaning it happens whole or not at all, never half. the man page for rename promises other programs never find the name missing.

the shop, the imaginary snack store these notes run on, updates order 106 this way. old orders.csv is 96 bytes, the new copy is 98. with 16 byte blocks like 045, here is where the power can die:

| power dies | orders.csv | orders.csv.tmp |
|---|---|---|
| while writing the copy | old, 96 bytes, fine | torn, 32 of 98 bytes |
| copy done, before rename | old, 96 bytes, fine | all 98 bytes |
| after the rename | new, 98 bytes | gone, it is orders.csv now |

a tear (the cut between [blocks](./044-disks-read-in-blocks.md) from 045) can only land in the tmp file, which nobody reads. every row of the middle column is a whole file, old or new.

```python
import os, tempfile

path = os.path.join(tempfile.mkdtemp(), "orders.csv")
with open(path, "w") as f:
    f.write("106,pending\n")
tmp = path + ".tmp"
with open(tmp, "w") as f:
    f.write("106,delivered\n")
    f.flush()
    os.fsync(f.fileno())
os.replace(tmp, path)
print(open(path).read().strip(), sorted(os.listdir(os.path.dirname(path))))
```

```output
106,delivered ['orders.csv']
```

i expected the careful way to write a file to be a careful write, and its the opposite, you dont touch the file. the fsync line pushes the new bytes to disk now, instead of leaving them waiting in memory, and it is what makes row 2 true after a power cut. keep the tmp in the same folder, since rename cant move between file systems, roughly separate drives.

python calls it os.replace.

### check yourself

1. a script deletes orders.csv, then renames the finished tmp file to orders.csv. the power dies between those two lines. what is in the shop folder, and why isnt a complete tmp file enough?
<details><summary>answer</summary>

no orders.csv at all, just the complete tmp, so a reader finds nothing. the safety comes from replacing in one rename, as well as from a whole copy. the tempting answer is that a whole tmp alone makes it safe.

</details>

2. the tmp copy of the 98 byte file had 5 blocks of 16 bytes written when the power died. a reader opens orders.csv. how many bytes, and what does line 6 (order 106) say?
<details><summary>answer</summary>

```python
old = b"101,delivered\n102,delivered\n103,delivered\n104,cancelled\n105,delivered\n106,pending\n107,delivered\n"
print(len(old), old.split(b"\n")[5].decode())
```

```output
96 106,pending
```
the reader sees the old file, whole. the 80 new bytes sit in the tmp, never read. the tempting answer is the 045 tear, 96 bytes ending `106,deliveg`.

</details>

3. your script writes its tmp file in /tmp, but orders.csv is on a different drive. the rename raises an error, so you switch to the python function shutil.move, which works. whats the catch?
<details><summary>answer</summary>

shutil.move falls back to copying, writing straight into orders.csv, so it can tear like 045. it is no rename that works everywhere. put the tmp in orders.csvs folder.

</details>

---
prev: [045 torn writes, what a half finished write leaves behind](./045-torn-writes.md) | next: not written yet
