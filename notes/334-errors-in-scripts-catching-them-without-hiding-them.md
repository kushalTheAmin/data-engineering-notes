# 334: errors in scripts, catching them without hiding them
builds on: [326 running a python script from the terminal](./326-running-a-python-script-from-the-terminal.md), [313 json over http, the answer is text until you parse it](./313-json-over-http-the-answer-is-text-until-you-parse-it.md)
section: python for data work, part 10, ~2 min read

my script for order 101 hit an error, carried on, and printed 12.0. the real total is 18.0. where did 6.00 go?

an exception is python saying "i cant do this line": the script stops and prints a traceback, the trail of lines that led to the failure. try/except catches the kind of exception you name, like the try around json.loads in [313](./313-json-over-http-the-answer-is-text-until-you-parse-it.md).

the shop, the imaginary gujarati snack store these notes run on, has order 101 (2 dhokla, a steamed savory cake, at 6.00, and 2 masala chai at 3.00) and a typo in the chai name. a [script](./326-running-a-python-script-from-the-terminal.md) with no try dies like this (shortened):

```text
$ python3 total.py
Traceback (most recent call last):
  File "total.py", line 6, in <module>
    total += PRICES[name] * qty
KeyError: 'masalla chai'
```

and with a try:

```python
PRICES = {"dhokla": 6.00, "masala chai": 3.00}
lines = [("dhokla", 2), ("masalla chai", 2)]

total = 0
skipped = []
for name, qty in lines:
    try:
        total += PRICES[name] * qty
    except KeyError:
        skipped.append(name)

print("total:", total)
print("skipped:", skipped)
```

```output
total: 12.0
skipped: ['masalla chai']
```

the last traceback line names the kind, KeyError, a dictionary lookup with a missing key. i assumed catching an error was the safe move, but the branch decides. replace the append with `pass`, which does nothing, and skipped stays [], with nothing to say a line vanished. the skipped list answers the question at the top.

name the exact error you expect. an unexpected one, like a TypeError from a float price times a quantity that arrived as text, still crashes, and you want that. the [python docs](https://docs.python.org/3/tutorial/errors.html) say `except Exception` catches almost everything, and suggest printing the error then writing `raise` to pass it on.

a data job that swallows errors can report success after copying only part of the rows, and the report built on them just shows a smaller number.

---

### check yourself

1. same PRICES as above. what does this print?
```python
PRICES = {"dhokla": 6.00, "masala chai": 3.00}
total = 0
for name, qty in [("dhokla", 1), ("fafda", 3), ("masala chai", 1)]:
    try:
        total += PRICES[name] * qty
    except KeyError:
        continue
print(total)
```
<details><summary>answer</summary>

```output
9.0
```

fafda isnt in PRICES, so its line is skipped with no trace, and 6.0 + 3.0 is 9.0. the tempting answer is 6.0, from thinking the loop stops at the first failure, but continue moves on to the next line.

</details>

2. a file you read hands over qty as the text "2", like the argument in [326](./326-running-a-python-script-from-the-terminal.md). with `except KeyError` around `PRICES["dhokla"] * qty`, is that line skipped?
<details><summary>answer</summary>

no, it crashes with a TypeError, because 6.0 times text makes no sense and TypeError isnt a KeyError. the tempting answer is skipped, from reading except as catching any failure. it only catches the kind you name.

</details>

---
prev: [333 pull requests, asking for a review before merging](./333-pull-requests-asking-for-a-review-before-merging.md) | next: not written yet
