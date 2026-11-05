# 326: running a python script from the terminal
builds on: [325 modules and imports, using code from other files](./325-modules-and-imports-using-code-from-other-files.md), [049 the terminal, running programs by typing](./049-the-terminal.md), [050 processes, a program while it runs](./050-processes.md), [052 the working directory](./052-the-working-directory.md), [053 absolute vs relative paths](./053-absolute-vs-relative-paths.md)
section: python for data work, part 2, ~2 min read

[325](./325-modules-and-imports-using-code-from-other-files.md) left report.py as a file you start yourself, with order 101 baked in. how do you point it at a different product without editing the file every time?

a script is a python file you run directly, and anything you type after its name arrives in a list called sys.argv. in the [terminal](./049-the-terminal.md), where you type commands, you write python3 and the file name. python3 is a program, so it starts a [process](./050-processes.md), a running copy, which reads your file top to bottom. a bare file name like total.py is a [relative path](./053-absolute-vs-relative-paths.md), looked up in the [working directory](./052-the-working-directory.md), the folder you are standing in.

the $ marks the prompt. here is total.py for the shop, the imaginary gujarati snack store these notes run on, and two runs:

```text
total.py
    import sys
    PRICES = {"dhokla": 6.00, "masala chai": 3.00}
    print(sys.argv)
    print(PRICES[sys.argv[1]] * int(sys.argv[2]))

$ python3 total.py dhokla 2
['total.py', 'dhokla', '2']
12.0
$ python3 total.py "masala chai" 2
['total.py', 'masala chai', '2']
6.0
```

each word after python3 is an [argument](./049-the-terminal.md), a word handed to the program and quotes glue two words into one. two things surprised me. the script name is sys.argv[0], so your first real argument is [1]. the 2 arrives as the text "2", not a number, because the terminal only ever passes text. i assumed it would arrive as a number. leave out int() and you get a TypeError, because 6.0 times text makes no sense.

scheduled jobs run lines like this too: cron, the timer on unix machines, runs a command on a schedule ([source](https://en.wikipedia.org/wiki/Cron)). for many arguments, python ships argparse, a built-in helper that can turn the text into numbers if you ask ([docs](https://docs.python.org/3/library/argparse.html)).

---
prev: [325 modules and imports, using code from other files](./325-modules-and-imports-using-code-from-other-files.md) | next: [327 packages and pip, installing code other people wrote](./327-packages-and-pip-installing-code-other-people-wrote.md)
