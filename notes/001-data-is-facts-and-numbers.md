# 001: data is facts written down, and a computer only keeps numbers
builds on: nothing, this is the start
section: data at the atom level, part 1, ~2 min read

tell a computer that Asha ordered 2 dhokla, and what does it actually keep? not those words. only numbers.

data is facts somebody wrote down so they can ask questions about them later. every example in these notes comes from one made up place, the shop: an online store selling gujarati snacks like dhokla, a steamed savory cake. it has five customers, six products, and all its data lives in [one file](../data/shop.sql). heres one order from it, and what the computer really keeps:

| piece | what you see | what the computer keeps |
|---|---|---|
| who | Asha | 65, 115, 104, 97 |
| what | dhokla | 100, 104, 111, 107, 108, 97 |
| how many | 2 | 2 |
| when | april 1 2026, 9:15 UTC | 1775034900 |

one order is four answers glued together, and every one of them ended up as numbers. heres the part i didnt expect: a computer cant hold "Asha" or "april" at all. it keeps numbers and nothing else.

so each piece goes through a shared rule. names become one number per letter. the 2 was already a number. the time becomes a count of seconds since the very start of 1970 in UTC, the worlds reference clock, which is the starting line phones, macs and most web servers agree on. you can watch the letter rule happen:

```python
for letter in "Asha":
    print(letter, ord(letter))
```

```output
A 65
s 115
h 104
a 97
```

`ord` is python asking for a letters number. and notice the catch: the numbers dont carry their meaning. 97 could be the letter a or just ninety seven. whatever reads them back has to know which rule was used, and getting that wrong is behind a lot of the garbled text you have seen online.

next up is the smallest thing those numbers are made of.

---
prev: nothing, this is the start | next: [002 bits, everything is a tiny switch](./002-bits.md)
