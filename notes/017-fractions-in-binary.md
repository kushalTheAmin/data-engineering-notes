# 017: fractions in binary, halves, quarters, eighths
builds on: [003 counting in binary](./003-counting-in-binary.md), [015 integer sizes, 8, 16, 32 and 64 bit numbers](./015-integer-sizes.md)
section: data at the atom level, part 17, ~2 min read

the shop, the imaginary snack store these notes run on, sells khandvi, a rolled savory snack, for 7.50. an [integer](./015-integer-sizes.md), a whole number stored in a fixed row of bits (0 or 1 switches), has no spot for that .50. if a computer keeps 7.50 as plain binary, where does the half live?

a binary fraction is [binary](./003-counting-in-binary.md), counting with only 0 and 1, carried past a dot, the binary point. going left each [place](./003-counting-in-binary.md), what a digit is worth by where it sits, doubles. going right each place halves. here are 3 places after the point:

| after the point | halves (0.5) | quarters (0.25) | eighths (0.125) | number |
|---|---|---|---|---|
| .000 | 0 | 0 | 0 | 0 |
| .001 | 0 | 0 | 0.125 | 0.125 |
| .010 | 0 | 0.25 | 0 | 0.25 |
| .011 | 0 | 0.25 | 0.125 | 0.375 |
| .100 | 0.5 | 0 | 0 | 0.5 |
| .101 | 0.5 | 0 | 0.125 | 0.625 |
| .110 | 0.5 | 0.25 | 0 | 0.75 |
| .111 | 0.5 | 0.25 | 0.125 | 0.875 |

so khandvi at 7.50 is 111.1, the 4, 2 and 1 make 7 and the .1 is one half. fafda, a crisp fried snack, at 4.50 is 100.1. i expected a new set of rules for fractions, but its 003s places again, just halving instead of doubling once you pass the dot.

3 places only land on steps of 0.125, so a price like 0.30 sits between .010 and .011 and no row of the table hits it. more places shrink the steps, but you only land on sums of a half, a quarter, an eighth and so on.

0.1 is one of the values that never lands, no matter how many places you add. python keeps numbers with far more places than 3, and this prints the exact value it really kept:

```python
from decimal import Decimal
print(Decimal(0.75))
print(Decimal(0.1))
```

```output
0.75
0.1000000000000000055511151231257827021181583404541015625
```

0.75 is exact, 0.1 is only a close neighbor. the next one is why.

---
prev: [016 overflow, what happens when a count goes past the top](./016-overflow.md) | next: not written yet
