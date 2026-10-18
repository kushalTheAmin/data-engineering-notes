# 060: capstone, the life of one saved order, memory to disk and back
builds on: [035 the processor, the part that does the work](./035-the-processor.md), [036 memory vs disk, one forgets and one remembers](./036-memory-vs-disk.md), [037 disk is slow, memory vs SSD vs spinning disk in real numbers](./037-disk-is-slow.md), [038 1000 or 1024, why your drive looks smaller than the box said](./038-1000-or-1024.md), [039 a file is a named list of bytes](./039-a-file-is-a-named-list-of-bytes.md), [040 folders and paths](./040-folders-and-paths.md), [041 text files vs binary files](./041-text-files-vs-binary-files.md), [042 line endings, the invisible characters that break files](./042-line-endings.md), [043 reading start to end vs jumping to a spot](./043-reading-start-to-end-vs-jumping.md), [044 disks read in blocks, never single bytes](./044-disks-read-in-blocks.md), [045 torn writes, what a half finished write leaves behind](./045-torn-writes.md), [046 writing safely, write a new file then rename it](./046-writing-safely.md), [047 compression, making files smaller by spotting repeats](./047-compression-spotting-repeats.md), [048 compression trades processor time for disk space](./048-compression-trades-processor-for-space.md), [049 the terminal, running programs by typing](./049-the-terminal.md), [050 processes, a program while it runs](./050-processes.md), [051 the operating system, the program that shares the machine out](./051-the-operating-system.md), [052 the working directory, where the terminal is standing](./052-the-working-directory.md), [053 absolute vs relative paths](./053-absolute-vs-relative-paths.md), [054 head and tail, looking at the start and end of a file](./054-head-and-tail.md), [055 wc, counting lines](./055-wc-counting-lines.md), [056 grep, finding the lines that match](./056-grep-finding-matching-lines.md), [057 standard input and output, how programs pass text along](./057-standard-input-and-output.md), [058 pipes, chaining small programs together](./058-pipes.md), [059 redirecting output into a file](./059-redirecting-output-into-a-file.md)
section: memory, disks and files, wrap up, ~3 min read

order 106 goes from pending to delivered and you hit save. how many separate ideas does that one click lean on, and which note covers each?

the shop, the imaginary gujarati snack store these notes run on, exports its orders to a text file, orders.csv (a header line plus 7 orders, one per line). a byte is a group of 8 bits, and a file is just bytes with a name. here is the whole trip, from the order arriving to someone counting delivered orders in the terminal, the text window where you type commands:

| stage | what happens to order 106 | notes |
|---|---|---|
| 1 | a process, one running copy of a program, gets its turns on the processor, and the order sits in memory, which forgets at power off | [035](./035-the-processor.md) [036](./036-memory-vs-disk.md) [050](./050-processes.md) [051](./051-the-operating-system.md) |
| 2 | the program finds the file by its path, the folder names leading to it, and a relative one starts from the folder it is run in | [039](./039-a-file-is-a-named-list-of-bytes.md) [040](./040-folders-and-paths.md) [052](./052-the-working-directory.md) [053](./053-absolute-vs-relative-paths.md) |
| 3 | the text ends each line with the byte 0a (hex, two digits per byte; windows files often use 0d 0a), and bytes that decode as characters make a text file | [041](./041-text-files-vs-binary-files.md) [042](./042-line-endings.md) |
| 4 | the disk takes fixed chunks called blocks, so a cut-off write can leave half a file, and the fix is a whole temporary copy, pushed to disk, then renamed over the old name | [036](./036-memory-vs-disk.md) [044](./044-disks-read-in-blocks.md) [045](./045-torn-writes.md) [046](./046-writing-safely.md) |
| 5 | before writing it could be compressed, spending processor time to store fewer bytes, and how big the file looks depends on 1000 or 1024 | [038](./038-1000-or-1024.md) [047](./047-compression-spotting-repeats.md) [048](./048-compression-trades-processor-for-space.md) |
| 6 | anyone reading it later starts at the top, since lines have no fixed size so no position is known, and disk reads are slow | [037](./037-disk-is-slow.md) [043](./043-reading-start-to-end-vs-jumping.md) |
| 7 | in the terminal, head and tail peek, wc counts lines, grep keeps matching lines, a pipe hands one output to the next, and > saves it in a file | [049](./049-the-terminal.md) [054](./054-head-and-tail.md) [055](./055-wc-counting-lines.md) [056](./056-grep-finding-matching-lines.md) [057](./057-standard-input-and-output.md) [058](./058-pipes.md) [059](./059-redirecting-output-into-a-file.md) |

some of those numbers can be checked, here on the file before the save:

```python
lines = ["order_id,customer_id,ordered_at,status",
         "101,1,2026-04-01 09:15:00,delivered",
         "102,2,2026-04-01 18:40:00,delivered",
         "103,1,2026-04-03 12:05:00,delivered",
         "104,3,2026-04-04 08:30:00,cancelled",
         "105,4,2026-04-06 19:10:00,delivered",
         "106,1,2026-04-08 10:00:00,pending",
         "107,2,2026-04-09 13:45:00,delivered"]
data = ("\n".join(lines) + "\n").encode()
print(len(data), "bytes,", -(-len(data) // 4096), "block,", data.count(b"\n"), "lines")
print(sum("delivered" in l for l in lines), "delivered")
new = data.replace(b"106,1,2026-04-08 10:00:00,pending", b"106,1,2026-04-08 10:00:00,delivered")
print(len(new), "bytes after,", new.count(b"delivered"), "delivered")
```

```output
289 bytes, 1 block, 8 lines
5 delivered
291 bytes after, 6 delivered
```

before the save that is 289 bytes, one 4096 byte block, 8 lines because the header counts, and 5 delivered, which is what `grep delivered orders.csv | wc -l` prints. pending is 7 letters and delivered is 9, so after the save the file is 2 bytes bigger and the count is 6.

i expected saving to be one step, and the actual write is the easy part. the rest is making sure the right program, in the right folder, wrote a whole file or nothing.

### check yourself

1. orders.csv is saved with CRLF endings (two bytes, 0d 0a, ending each line). what does `grep delivered orders.csv | wc -l` print, and why does the hidden 0d change nothing?

<details><summary>answer</summary>

five. grep only asks whether delivered appears in the line, and the 0d sits after it. wc counts 0a bytes, and CRLF has one per line. the tempting answer is 0, from 042, where an exact match failed.

</details>

2. you run `grep delivered orders.csv > orders.csv.tmp`, then rename the tmp over orders.csv. the power dies halfway through the grep. what is orders.csv, and how many lines after a clean run?

<details><summary>answer</summary>

still the old 8 line file, because > emptied the tmp, not orders.csv. after a clean run, 5 lines and no header, since the header has no delivered in it. the tempting answers are an emptied file, from 059, and 6 lines.

</details>

3. a 35 MB export. which finishes faster, `head -n 3` or `wc -l`, and why?

<details><summary>answer</summary>

head. it stops after 3 lines, while wc reads every byte to count the 0a characters. the tempting answer is the same time.

</details>

the next section is about giving this text a shape, so a program can tell the columns apart.

---
prev: [059 redirecting output into a file](./059-redirecting-output-into-a-file.md) | next: not written yet
