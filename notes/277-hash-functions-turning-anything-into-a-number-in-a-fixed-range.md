# 277: hash functions, turning anything into a number in a fixed range
builds on: [273 binary search, finding one item in sorted data by halving](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md), [270 flat and straight line, the two shapes of growth](./270-flat-and-straight-line-the-two-shapes-of-growth.md), [007 text is numbers, one character and one number](./007-text-is-numbers.md), [004 bytes, 8 bits and 256 possible values](./004-bytes.md)
section: tricks that make data fast, part 9, ~2 min read

halving ([273](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md)) needs sorted data. a python dictionary has no sorted order and still jumps straight to "dhokla" without reading the other keys. how does it know where to jump?

the first half of that trick is a hash function: it turns any input into a number, and the same input always gives the same number. then a remainder (the leftover after dividing, written %) squeezes the number into a fixed range.

the shop, the imaginary gujarati snack store these notes run on, sells dhokla, a steamed savory cake. each character is one number ([007](./007-text-is-numbers.md)), one [byte](./004-bytes.md), a group of 8 bits. a toy hash: add the bytes of the name, then % 8 to land in one of 8 slots, numbered 0 to 7.

```text
"dhokla" into 8 slots
bytes:      100 104 111 107 108 97
added up:   627
627 % 8:    627 = 78 x 8 + 3, so slot 3
```

all six products, same recipe:

| product | bytes added | % 8 |
|---|---|---|
| dhokla | 627 | 3 |
| khandvi | 741 | 5 |
| jalebi | 615 | 7 |
| kaju katli | 992 | 0 |
| masala chai | 1060 | 4 |
| fafda | 498 | 2 |

ask again tomorrow and dhokla is still 3, so you find a slot by calculating instead of searching. that is the flat shape from [270](./270-flat-and-straight-line-the-two-shapes-of-growth.md), a jump.

i expected a hash function to be some scary scrambling, but this one is addition and a remainder. it is also a bad one: "kholda" has the same letters, adds to 627 and lands in slot 3 too. real ones mix the order of the bytes in.

python hashes text this way for dictionaries, but its value for a string changes each time python starts, on purpose ([docs](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONHASHSEED)). same within one run, never saved to a file.

### check yourself

1. the shop adds 2 slots, so it is % 10 instead of % 8. which slot does dhokla get, and does any product keep its old slot?

<details><summary>answer</summary>

627 % 10 is 7. the new slots are dhokla 7, khandvi 1, jalebi 5, kaju katli 2, masala chai 0, fafda 8, and none match the old 3, 5, 7, 0, 4, 2. the tempting answer is that only the new slots change, but the remainder depends on the range, so everything can move.

</details>

2. a teammate saves python hash values of customer names to a file, and a script reads them next day to pick slots. why do the slots not match?

<details><summary>answer</summary>

python mixes a random secret into text hashes each run, so Asha gets a new number tomorrow. the tempting answer is a bad file, but a name only keeps its number inside one run.

</details>

3. a messy export has "fafda " with a trailing space. toy hash, which slot?

<details><summary>answer</summary>

slot 2, same as fafda. a space is byte 32, so the sum is 530, and 530 % 8 is 2. the tempting answer is a different slot because the text differs, but 32 is 4 x 8 and adds nothing to the remainder.

</details>

---
prev: [276 why sorting costs more than one pass over the data](./276-why-sorting-costs-more-than-one-pass-over-the-data.md) | next: not written yet
