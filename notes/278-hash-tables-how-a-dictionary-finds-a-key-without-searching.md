# 278: hash tables, how a dictionary finds a key without searching
builds on: [277 hash functions, turning anything into a number in a fixed range](./277-hash-functions-turning-anything-into-a-number-in-a-fixed-range.md), [270 flat and straight line, the two shapes of growth](./270-flat-and-straight-line-the-two-shapes-of-growth.md), [273 binary search, finding one item in sorted data by halving](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md), [269 big O in plain words, how work grows as data grows](./269-big-o-in-plain-words-how-work-grows-as-data-grows.md)
section: tricks that make data fast, part 10, ~2 min read

in [270](./270-flat-and-straight-line-the-two-shapes-of-growth.md) a missing id made `in` walk the whole list. ask a python dictionary for a name it doesnt have and it says no in one look. why is a miss cheap too?

a hash table is a row of numbered slots plus a hash function. to store a key (here the name you look things up by, not the table key of [087](./087-primary-key.md)), hash it and put it, with its value, in that slot. to find it, hash again and look in that one slot.

the shop, the imaginary gujarati snack store these notes run on, uses the toy hash from [277](./277-hash-functions-turning-anything-into-a-number-in-a-fixed-range.md): add up the byte of each letter (one number per character, [007](./007-text-is-numbers.md)), then % 8 (the remainder). the products table (dhokla a steamed savory cake, jalebi a fried syrup sweet) goes into 8 slots:

```python
def slot_of(name):
    return sum(name.encode()) % 8

slots = [None] * 8
for name, price in [("dhokla", 6.00), ("khandvi", 7.50), ("jalebi", 5.00),
                    ("kaju katli", 12.00), ("masala chai", 3.00), ("fafda", 4.50)]:
    slots[slot_of(name)] = (name, price)

for i, s in enumerate(slots):
    print(i, s)

for wanted in ["jalebi", "thepla", "kholda"]:
    s = slots[slot_of(wanted)]
    found = s is not None and s[0] == wanted
    print(wanted, "-> slot", slot_of(wanted), "| found" if found else "| not here", "| 1 look")
```

```output
0 ('kaju katli', 12.0)
1 None
2 ('fafda', 4.5)
3 ('dhokla', 6.0)
4 ('masala chai', 3.0)
5 ('khandvi', 7.5)
6 None
7 ('jalebi', 5.0)
jalebi -> slot 7 | found | 1 look
thepla -> slot 6 | not here | 1 look
kholda -> slot 3 | not here | 1 look
```

no sorting, no halving ([273](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md)), one look each time. thepla, a spiced flatbread, lands in an empty slot, so the answer is no. kholda lands on dhokla, which is why each slot keeps the name next to the price: without it, kholda would get the dhokla price.

i assumed a miss would be the slow case, like in a list, but here it costs the same as a hit.

python dictionaries use the same idea with a much better hash, and its docs list a lookup as O(1) ([269](./269-big-o-in-plain-words-how-work-grows-as-data-grows.md), steps that stay flat), but only on average ([docs](https://docs.python.org/3/builtins/time-complexity.html)). what happens when two names want the same slot is the next one.

### check yourself

1. the shop adds "ladoo" (a round sweet) to this table, 8 slots. which slot, and is it free?

<details><summary>answer</summary>

the bytes add to 527, and 527 % 8 is 7. slot 7 already holds jalebi, so it is not free (the code above would overwrite jalebi, the next note is about that). the tempting answer is that there are two free slots, so ladoo fits, but the hash picks the slot and ignores which ones are empty.

</details>

2. a teammate wants to check if "barfi" is in the table. how many slots do you look at, and is the answer yes?

<details><summary>answer</summary>

one slot. barfi adds to 516, 516 % 8 is 4, and slot 4 holds masala chai, so the answer is no, since masala chai is not barfi. the tempting answer is that a no needs checking all 8 slots, as a list would.

</details>

---
prev: [277 hash functions, turning anything into a number in a fixed range](./277-hash-functions-turning-anything-into-a-number-in-a-fixed-range.md) | next: not written yet
