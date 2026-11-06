# 342: environment variables, settings that live outside the code
builds on: [326 running a python script from the terminal](./326-running-a-python-script-from-the-terminal.md), [314 API keys, a password for programs](./314-api-keys-a-password-for-programs.md), [329 git, commits as snapshots of your code](./329-git-commits-as-snapshots-of-your-code.md), [051 the operating system](./051-the-operating-system.md), [050 processes, a program while it runs](./050-processes.md), [049 the terminal, running programs by typing](./049-the-terminal.md)
section: python for data work, part 18, ~2 min read

[314](./314-api-keys-a-password-for-programs.md) said to keep an api key, the secret string a program sends to identify itself, out of your code. not where it goes instead. where does report.py read it from?

an environment variable is a named piece of text, kept outside your code, handed to a program when it starts. python shows them as os.environ (os is short for operating system), a dictionary whose values are all text. here is report.py for the shop, the imaginary gujarati snack store these notes run on, run three ways in the [terminal](./049-the-terminal.md), $ marking the prompt:

```text
report.py
    import os
    key = os.environ["SHOP_API_KEY"]
    limit = int(os.environ.get("ROW_LIMIT", "100"))
    print(key[:4] + "...", limit)

$ python3 report.py
KeyError: 'SHOP_API_KEY'
$ SHOP_API_KEY=k_report_7f3a python3 report.py
k_re... 100
$ SHOP_API_KEY=k_report_7f3a ROW_LIMIT=5 python3 report.py
k_re... 5
```

the first run dies with KeyError, a missing name (i trimmed the error to its last line). in bash or zsh, NAME=value before the command sets it for that one run. the second finds the key, and .get hands back the default "100" for the missing ROW_LIMIT. the third overrides it.

i assumed this was python, but the [operating system](./051-the-operating-system.md) does it: every [process](./050-processes.md), a running program, starts with its own list of name and text pairs, copied from whatever started it, here your terminal window. so one file runs with different keys on your laptop and a server.

gotchas: values are text, like [sys.argv](./326-running-a-python-script-from-the-terminal.md), so ROW_LIMIT needs int() before math. and a typo in the name given to .get quietly returns the default, so for secrets use square brackets.

a key typed into code lands in each [git snapshot](./329-git-commits-as-snapshots-of-your-code.md), a saved copy of the project, and stays in history after you delete the line.

### check yourself

1. in one terminal window you ran export SHOP_API_KEY=k_report_7f3a, which sets it for that window and the programs started from it. you open a fresh second window, with nothing set at startup, and run python3 report.py. what happens?
<details><summary>answer</summary>

KeyError: 'SHOP_API_KEY'. the second window is a different shell, the program reading your typed lines, with its own list, and export only reaches programs started from the first one. the tempting answer is that it works because the machine has the key.

</details>

2. the shop has 7 orders. you set ROW_LIMIT=5 but the script has a typo in the name it reads. what does this print, and why not 5?
<details><summary>answer</summary>

it prints 7. .get finds no ROW_LIMT, so it quietly uses the default 100, and min picks the 7 orders. no error.

```python
import os
os.environ["ROW_LIMIT"] = "5"
limit = int(os.environ.get("ROW_LIMT", "100"))
print(min(limit, 7))
```

```output
7
```

the tempting answer is 5, from assuming the setting was read.

</details>

---
prev: [341 reading JSON in python, the whole file at once](./341-reading-json-in-python-the-whole-file-at-once.md) | next: not written yet
