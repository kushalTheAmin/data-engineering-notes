# 058: pipes, chaining small programs together
builds on: [049 the terminal, running programs by typing](./049-the-terminal.md), [050 processes, a program while it runs](./050-processes.md), [055 wc, counting lines](./055-wc-counting-lines.md), [056 grep, finding the lines that match](./056-grep-finding-matching-lines.md), [057 standard input and output, how programs pass text along](./057-standard-input-and-output.md)
section: memory, disks and files, part 24, ~2 min read

how many orders in the shop, the imaginary gujarati snack store these notes run on, are delivered? [grep](./056-grep-finding-matching-lines.md) prints those lines and [wc -l](./055-wc-counting-lines.md) counts lines, so can you hand one to the other?

yes, with a pipe, written |. it connects the stdout of the left program, where it writes, to the stdin of the right one, where it reads ([057](./057-standard-input-and-output.md)). the shell, the program that runs your line, starts both as separate [processes](./050-processes.md), running copies of programs:

```text
$ grep delivered orders.csv | wc -l
5
```

| program | reads | writes |
| --- | --- | --- |
| grep delivered orders.csv | the file, 8 lines | the 5 delivered lines |
| wc -l | those 5 lines, on stdin | 5 |

in python, one function feeding the next:

```python
lines = ["order_id,customer_id,ordered_at,status",
         "101,1,2026-04-01 09:15:00,delivered",
         "102,2,2026-04-01 18:40:00,delivered",
         "103,1,2026-04-03 12:05:00,delivered",
         "104,3,2026-04-04 08:30:00,cancelled",
         "105,4,2026-04-06 19:10:00,delivered",
         "106,1,2026-04-08 10:00:00,pending",
         "107,2,2026-04-09 13:45:00,delivered"]

def grep(word, lines):
    return [line for line in lines if word in line]

def wc_l(lines):
    return len(lines)

print(wc_l(grep("delivered", lines)))
```

```output
5
```

i expected grep to save a file that wc then opens, and theres no file at all. wc never knows a pipe exists, it just reads stdin, and the system passes the bytes along through a small holding area.

a pipe only feeds stdin, so order matters. this is a shell pipe, and a data pipeline later is a bigger idea. people run grep ERROR app.log | wc -l on logs and save nothing in between.

### check yourself

1. what does wc -l orders.csv | grep delivered print, and why?
<details><summary>answer</summary>

nothing. wc writes the one line 8 orders.csv, that line has no "delivered", so grep prints nothing. the tempting answer is 5, from thinking grep still reads the file. it only sees what wc wrote.

</details>

2. what does grep delivered orders.csv | wc -l orders.csv print?
<details><summary>answer</summary>

8 orders.csv. given a file name, wc opens that file and ignores stdin, so the pipe feeds nothing. the tempting answer is 5.

</details>

3. customer 1 has 3 orders. how many lines does grep delivered orders.csv | grep ,1, | wc -l print?
<details><summary>answer</summary>

two. the first grep keeps the 5 delivered lines, the second keeps those containing ,1, which are orders 101 and 103. order 106 is pending, so it never reaches the second grep. the tempting answer is 3.

</details>

---
prev: [057 standard input and output, how programs pass text along](./057-standard-input-and-output.md) | next: not written yet
