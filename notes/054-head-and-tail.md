# 054: head and tail, looking at the start and end of a file
builds on: [042 line endings, the invisible characters that break files](./042-line-endings.md), [043 reading start to end vs jumping to a spot](./043-reading-start-to-end-vs-jumping.md), [049 the terminal, running programs by typing](./049-the-terminal.md), [052 the working directory, where the terminal is standing](./052-the-working-directory.md)
section: memory, disks and files, part 20, ~2 min read

someone sends you a huge csv. do you open the whole thing just to see what the columns are?

head prints the first lines of a file and tail prints the last ones. both give 10 lines unless you add -n and a number. you type them in the [terminal](./049-the-terminal.md), and a bare file name is looked up from the [working directory](./052-the-working-directory.md), the folder you stand in.

here they are on the shop, the imaginary gujarati snack store these notes run on, saved as orders.csv (a text file, usually one row per line, commas between values). the header line plus 7 orders makes 8 lines, ending in the 0a that [042](./042-line-endings.md) showed:

```text
$ head -n 3 orders.csv
order_id,customer_id,ordered_at,status
101,1,2026-04-01 09:15:00,delivered
102,2,2026-04-01 18:40:00,delivered
$ tail -n 2 orders.csv
106,1,2026-04-08 10:00:00,pending
107,2,2026-04-09 13:45:00,delivered
```

i kept counting the header as free, and head -n 3 gave me only two orders. the header is a line like any other. with no -n, head would print 10 lines, which here is the whole file.

why is this cheap on a huge file? [043](./043-reading-start-to-end-vs-jumping.md) said a file has no list of where lines begin, so reaching line 1,000,000 means reading everything before it. head only wants the first lines, so it reads those and stops, and the other 999,990 lines never need reading.

tail is for the other end. logs add new lines at the bottom, so tail shows what just happened, and the last row of a data file tells you if the write finished or got cut off mid-line.

---
prev: [053 absolute vs relative paths](./053-absolute-vs-relative-paths.md) | next: [055 wc, counting lines](./055-wc-counting-lines.md)
