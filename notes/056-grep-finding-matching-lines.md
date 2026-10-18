# 056: grep, finding the lines that match
builds on: [042 line endings, the invisible characters that break files](./042-line-endings.md), [043 reading start to end vs jumping to a spot](./043-reading-start-to-end-vs-jumping.md), [049 the terminal, running programs by typing](./049-the-terminal.md), [054 head and tail, looking at the start and end of a file](./054-head-and-tail.md)
section: memory, disks and files, part 22, ~2 min read

i wanted customer 1s orders, so i typed grep 1 orders.csv and got all 7 orders back. what did it think i asked for?

grep prints every line that contains the text you give it, and skips the rest. strictly the text is a pattern, so characters like . and * mean more than themselves, but plain words and digits match as written. a [line](./042-line-endings.md) is the text up to a 0a (ten, written in hex). you run it in the [terminal](./049-the-terminal.md), text first, then the file.

here is grep delivered orders.csv on the shop, the imaginary gujarati snack store these notes run on. orders.csv is the 8 lines [054](./054-head-and-tail.md) showed, header plus 7 orders:

| line of orders.csv | printed |
| --- | --- |
| order_id,customer_id,ordered_at,status | no |
| 101,1,2026-04-01 09:15:00,delivered | yes |
| 102,2,2026-04-01 18:40:00,delivered | yes |
| 103,1,2026-04-03 12:05:00,delivered | yes |
| 104,3,2026-04-04 08:30:00,cancelled | no |
| 105,4,2026-04-06 19:10:00,delivered | yes |
| 106,1,2026-04-08 10:00:00,pending | no |
| 107,2,2026-04-09 13:45:00,delivered | yes |

that is a loop with an if:

```python
lines = ["order_id,customer_id,ordered_at,status",
         "101,1,2026-04-01 09:15:00,delivered",
         "102,2,2026-04-01 18:40:00,delivered",
         "103,1,2026-04-03 12:05:00,delivered",
         "104,3,2026-04-04 08:30:00,cancelled",
         "105,4,2026-04-06 19:10:00,delivered",
         "106,1,2026-04-08 10:00:00,pending",
         "107,2,2026-04-09 13:45:00,delivered"]
for line in lines:
    if "delivered" in line:
        print(line)
```

```output
101,1,2026-04-01 09:15:00,delivered
102,2,2026-04-01 18:40:00,delivered
103,1,2026-04-03 12:05:00,delivered
105,4,2026-04-06 19:10:00,delivered
107,2,2026-04-09 13:45:00,delivered
```

so my grep 1 matched all 7 orders, because 101 to 107 all have a 1 in the order id. i assumed it looked at the customer_id column, and it cant, it has never heard of columns. to grep a csv is just text, and the match can sit anywhere in the line.

it also reads the file start to end like [043](./043-reading-start-to-end-vs-jumping.md) described, so on a huge log it takes as long as reading the whole thing. people use it to pull the ERROR lines out of logs. just check how many lines came back before you trust a loose match.

---
prev: [055 wc, counting lines](./055-wc-counting-lines.md) | next: [057 standard input and output, how programs pass text along](./057-standard-input-and-output.md)
