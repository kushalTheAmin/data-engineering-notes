# 045: torn writes, what a half finished write leaves behind
builds on: [036 memory vs disk, one forgets and one remembers](./036-memory-vs-disk.md), [039 a file is a named list of bytes](./039-a-file-is-a-named-list-of-bytes.md), [042 line endings, the invisible characters that break files](./042-line-endings.md), [044 disks read in blocks, never single bytes](./044-disks-read-in-blocks.md)
section: memory, disks and files, part 11, ~2 min read

the shops orders file now has a line that reads `106,deliveg`. nobody typed that, nothing crashed. [044](./044-disks-read-in-blocks.md) showed a disk hands over whole blocks, usually 4096 bytes, and a write goes out the same way, one block at a time. so a power cut, like the one in [036](./036-memory-vs-disk.md), can land between two blocks.

a torn write is a write cut off partway, so the file holds some new blocks and some old ones.

i shrank blocks to 16 bytes. the shop, the imaginary snack store these notes run on, keeps a [file](./039-a-file-is-a-named-list-of-bytes.md) of orders 101 to 107. order 106 goes from pending to delivered, overwritten in place. the new text is 98 bytes, 7 blocks instead of 6, and the power dies right after block 4. a `/` stands for the 0a [line ending](./042-line-endings.md), the character ending a line. blocks 0 to 3 match in both versions, so here are 4 to 6:

| block | old file | new file | on disk after the cut |
|---|---|---|---|
| 4 | vered/106,pendin | vered/106,delive | vered/106,delive |
| 5 | g/107,delivered/ | red/107,delivere | g/107,delivered/ |
| 6 | (none) | d/ | (none) |

block 4 got written, 5 and 6 never did. new `106,delive` sits glued to the old `g/`, and the file is still 96 bytes. line 6 reads `106,deliveg`.

i assumed a save either happens or it doesnt, but theres a third outcome, a mix, and it looks like valid text. would you spot it?

this is why SQLite, a database in one file, saves a copy of the old data before changing the file in its rollback mode, because power failures can leave part of a write done. the fix for plain files is the next note.

### check yourself

1. same shop file, but the power dies after block 3 is written instead of block 4. what does line 6 say afterwards?
<details><summary>answer</summary>

```python
old = b"ncelled\n105,deli"
new = b"ncelled\n105,deli"
print(old == new)
```

```output
True
```
that is block 3 in both versions, and blocks 0 to 2 match too, so writing them changes nothing and line 6 still says `106,pending`. the tempting answer is a broken line, but a tear only shows if the half written blocks differ.

</details>

2. suppose block 5 lands on disk but block 4 does not. what do the last two lines look like?
<details><summary>answer</summary>

```python
old4, new5 = "vered/106,pendin", "red/107,delivere"
print(("106,pendin" + new5).replace("/", "\n"))
```

```output
106,pendinred
107,delivere
```
line 6 is the old start glued to the new end, and line 7 loses its last letter and its line ending. the tempting answer is two clean lines, one old and one new.

</details>

---
prev: [044 disks read in blocks, never single bytes](./044-disks-read-in-blocks.md) | next: [046 writing safely, write a new file then rename it](./046-writing-safely.md)
