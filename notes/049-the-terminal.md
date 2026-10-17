# 049: the terminal, running programs by typing
builds on: [007 text is numbers, one character one number](./007-text-is-numbers.md), [039 a file is a named list of bytes](./039-a-file-is-a-named-list-of-bytes.md)
section: memory, disks and files, part 15, ~2 min read

why do so many data tools want you to type a line instead of click a button?

the terminal is a text window where you type one line, press enter, and the computer types back. inside it runs a shell, a program that reads your line and runs another program for you. (strictly the window is the terminal and the shell answers in it.)

the shell reads plain text, characters stored as numbers like [007](./007-text-is-numbers.md) showed. the first word names a program, usually a file of bytes on disk like [039](./039-a-file-is-a-named-list-of-bytes.md) built. every plain word after it is an argument, like a function argument, handed to that program. here it is with the shop, the imaginary gujarati snack store these notes run on:

```text
$ echo dhokla khandvi
dhokla khandvi
```

echo prints its arguments back, and the $ is the shell saying ready. the shell cuts your line at spaces, like this in python (shlex is a python module that splits the way a shell does):

```python
import shlex
print("echo masala chai".split())
print(shlex.split('echo "masala chai"'))
```

```output
['echo', 'masala', 'chai']
['echo', 'masala chai']
```

top one is echo with two arguments. the second shows quotes gluing a name with a space into one argument, and without them the program gets two things where you meant one.

i expected a separate scary mode of the computer, and its just this: split a line, run the first word. a typed line can be saved in a file and replayed exactly, which is much harder with clicks.

the next one is about what exists once the first word starts running.

---
prev: [048 compression trades processor time for disk space](./048-compression-trades-processor-for-space.md) | next: [050 processes, a program while it runs](./050-processes.md)
