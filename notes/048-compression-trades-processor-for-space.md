# 048: compression trades processor time for disk space
builds on: [033 kilobytes to terabytes, how big data gets](./033-kilobytes-to-terabytes.md), [035 the processor, the part that does the work](./035-the-processor.md), [037 disk is slow, memory vs SSD vs spinning disk in real numbers](./037-disk-is-slow.md), [047 compression, making files smaller by spotting repeats](./047-compression-spotting-repeats.md)
section: memory, disks and files, part 14, ~2 min read

[047](./047-compression-spotting-repeats.md) shrank the shops statuses by storing each run once. so why isnt every file compressed, always? because the saving is paid for somewhere else.

compression moves work. the file takes less space on disk and less time to read off it, but the [processor](./035-the-processor.md), the part doing tiny steps on numbers, must unpack (decompress) it before anyone can use it.

picture the shop, the imaginary gujarati snack store these notes run on, with a million orders, all delivered (made up, the real shop has 7). the status file, with run length encoding from 047:

| | raw | run length encoded |
|---|---|---|
| bytes on disk | 10,000,000 | 18 |
| bytes read off the disk | 10,000,000 | 18 |
| work for the processor | none, use it as is | build 1,000,000 lines |

```python
n = 1_000_000
print(n * len("delivered\n"), len(f"{n},delivered\n"))
```

```output
10000000 18
```

[037](./037-disk-is-slow.md) showed the disk is where time goes, an SSD lookup is 150 microseconds against 100 nanoseconds in memory. so reading 18 bytes instead of 10 million (10 MB, a million bytes is a [megabyte](./033-kilobytes-to-terabytes.md)) usually wins, even with the unpacking.

i assumed smaller was just better, but the saving and the bill come from the same file. and two things bite. you cant jump to line 600,000, you add up run counts from the top. and data with no repeats shrinks nothing, random bytes come out bigger, and the processor still did the work.

so tools give you a dial. the python library zlib has levels 1 to 9, 1 is fastest with the least compression, 9 is slowest with the most. Parquet, a file format for big tables, lets you pick the codec (the compression method), spread across a compression ratio versus processing cost range.

---
prev: [047 compression, making files smaller by spotting repeats](./047-compression-spotting-repeats.md) | next: [049 the terminal, running programs by typing](./049-the-terminal.md)
