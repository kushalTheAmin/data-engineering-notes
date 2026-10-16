# 002: bits, everything is a tiny switch
builds on: [001 data is facts written down](./001-data-is-facts-and-numbers.md)
section: data at the atom level, part 2, ~2 min read

your laptop holds photos, songs, spreadsheets and this sentence. at the very bottom, how many kinds of thing is it really storing? one.

a bit is the smallest thing a computer stores: one value that is either on or off, like a tiny switch.

[001](./001-data-is-facts-and-numbers.md) showed that every fact gets stored as numbers, even a name, where each letter has its own number. so what is a number made of? bits. we write off as 0 and on as 1. inside the machine a bit is a tiny electric charge or something like it, but every bit has exactly two states.

one bit can only answer a yes or no question. the trick is lining them up. this loop builds every pattern 1, 2 and 3 switches can make:

```python
patterns = [""]
for switch in range(3):
    longer = []
    for p in patterns:
        longer.append(p + "0")
        longer.append(p + "1")
    patterns = longer
    print(len(patterns), patterns)
```

```output
2 ['0', '1']
4 ['00', '01', '10', '11']
8 ['000', '001', '010', '011', '100', '101', '110', '111']
```

look at the inner loop. every old pattern comes out twice, once with a 0 on the end and once with a 1. so each switch you add doubles the count. keep doubling, 16, 32, 64, 128, and 8 switches give 256.

i honestly expected something richer than on and off at the bottom of a computer. but a normal laptop keeps trillions of these, mostly on its drive, where your photos live.

and a pattern only means something because people agree on it. same 3 switches, two agreements:

```text
as colors:   000 = red   001 = blue   010 = green  ...
as numbers:  000 = 0     001 = 1      010 = 2      ...
```

that second agreement is counting in binary, numbers written with only 0 and 1.

---
prev: [001 data is facts written down](./001-data-is-facts-and-numbers.md) | next: not written yet
