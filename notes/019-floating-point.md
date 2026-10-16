# 019: floating point, digits plus where the point sits
builds on: [003 counting in binary](./003-counting-in-binary.md), [015 integer sizes, 8, 16, 32 and 64 bit numbers](./015-integer-sizes.md), [017 fractions in binary, halves, quarters, eighths](./017-fractions-in-binary.md), [018 why 0.1 has no exact binary form](./018-why-0-1-has-no-exact-binary-form.md)
section: data at the atom level, part 19, ~2 min read

a 64 bit [integer](./015-integer-sizes.md), a whole number in a fixed row of bits (8 bits make a byte), tops out near 9 quintillion. but a 64 bit float, also 8 bytes, can roughly hold 0.000001 and a number over 300 digits long. how would you pull that off?

a float is scientific notation in [binary](./003-counting-in-binary.md), counting with only 0 and 1: a few digits, plus a count of how far to slide the [binary point](./017-fractions-in-binary.md), the dot where places start halving. it cut 0.1 off in [018](./018-why-0-1-has-no-exact-binary-form.md). here are prices from the shop, the imaginary snack store these notes run on:

| product | price | in binary | digits, then slide the point |
|---|---|---|---|
| dhokla, a steamed savory cake | 6.00 | 110 | 1.1, right 2 places |
| khandvi | 7.50 | 111.1 | 1.111, right 2 places |
| fafda | 4.50 | 100.1 | 1.001, right 2 places |
| kaju katli | 12.00 | 1100 | 1.1, right 3 places |

every number except 0 is written as 1.something, and the slide says how far right to move the point to get it back (negative goes left, for tiny numbers). 64 bits split into 1 for plus or minus, 11 for the slide, 52 for the digits. the 1 before the point is always 1, so it isnt stored, making 53 digits (0 and the tiniest numbers are special cases).

i expected big numbers to get more digits, but only the slide grows:

```python
big = 2.0 ** 53
print(big + 1)
print(big + 2)
```

```output
9007199254740992.0
9007199254740994.0
```

just past 2 to the 53 the digits cant tell neighbors apart, so +1 vanishes and whole numbers are 2 apart, then 4 apart. javascripts plain numbers (not BigInt) are floats like this, so ids above 9007199254740991 can get rounded, which is why some APIs send big ids as text: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse

so 0.1 + 0.2 is next, and why it surprises everyone.

---
prev: [018 why 0.1 has no exact binary form](./018-why-0-1-has-no-exact-binary-form.md) | next: [020 why 0.1 + 0.2 is not exactly 0.3](./020-why-0-1-plus-0-2-is-not-0-3.md)
