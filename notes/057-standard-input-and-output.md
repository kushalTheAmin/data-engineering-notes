# 057: standard input and output, how programs pass text along
builds on: [049 the terminal, running programs by typing](./049-the-terminal.md), [050 processes, a program while it runs](./050-processes.md), [055 wc, counting lines](./055-wc-counting-lines.md), [056 grep, finding the lines that match](./056-grep-finding-matching-lines.md)
section: memory, disks and files, part 23, ~2 min read

in [055](./055-wc-counting-lines.md), wc -l orders.csv printed "8 orders.csv" but wc -l < orders.csv printed just 8. where did the file name go?

every [process](./050-processes.md), a running copy of a program, starts with two text channels already open. standard input, stdin, is where it reads from. standard output, stdout, is where it writes to. a stream is just bytes handed over in order. by default stdin is your keyboard and stdout is the [terminal](./049-the-terminal.md) screen. print() in python writes to stdout.

| command | where the program reads | does it see the name |
| --- | --- | --- |
| wc -l orders.csv | opens the file itself | yes |
| wc -l < orders.csv | stdin, filled from the file | no |
| grep delivered | stdin, the keyboard | no |

the program never knows what is on the other end of stdin. the shell, the program in the terminal that runs your line, can swap the keyboard for a file with < before its name. then wc just reads stdin, with no name to print. thats the answer to the 8.

[grep](./056-grep-finding-matching-lines.md) from 056 does the same. leave off the file name and it reads stdin:

```text
$ grep delivered
shipped
order 101 delivered
order 101 delivered
(ctrl+d)
$
```

i assumed grep with no file was an error, and its just a program quietly waiting on the keyboard. "shipped" has no match so nothing came back. the doubled line is my typing, then grep printing the match. ctrl+d tells it the input is over.

so a command that looks frozen may just be missing its file name. its waiting on you.

grep and wc dont care where stdin comes from, and a later note uses that to feed one program into another.

---
prev: [056 grep, finding the lines that match](./056-grep-finding-matching-lines.md) | next: not written yet
