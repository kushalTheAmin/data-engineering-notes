# 017: fractions in binary, halves, quarters, eighths
builds on: [003 counting in binary](./003-counting-in-binary.md), [016 overflow, what happens when a count goes past the top](./016-overflow.md)
section: data at the atom level, part 17, ~2 min read

[016](./016-overflow.md) was all about whole numbers running out of room. but the shop, the imaginary snack store these notes run on, sells khandvi, a rolled gram flour snack, at 7.50. a whole number cant say that. so how do bits write the .50?

a binary fraction is the same [place value](./003-counting-in-binary.md) idea, a digit worth what its position says, carried past a dot. the dot is called the binary point. left of it the places are 4, 2, 1 like before. right of it each place is half the one before: a half, a quarter, an eighth. a slice of the shop prices:

| price | 4 | 2 | 1 | point | half | quarter | eighth |
|---|---|---|---|---|---|---|---|
| 7.50 khandvi | 1 | 1 | 1 | . | 1 | 0 | 0 |
| 4.50 fafda, a crispy chickpea strip | 1 | 0 | 0 | . | 1 | 0 | 0 |
| 6.00 dhokla, a steamed savory cake | 1 | 1 | 0 | . | 0 | 0 | 0 |

read khandvi: 4 + 2 + 1 is 7, plus a half is 7.5. thats the whole trick. i was surprised how little changed, i expected a new system and its just the places going on halving past the dot.

every digit after the point is a yes or no to a half, a quarter, an eighth. so 0.75 is 0.11, a half plus a quarter, and 0.625 is 0.101, a half plus an eighth.

notice what fits: .50, .25, .75 all land exactly, because they are built from halves. python agrees, 7.5 and 0.75 are stored with no rounding at all.

but try writing 0.10 this way. no pile of halves, quarters and eighths gets you there, and that is a real problem for money. the next one is about exactly that.

---
prev: [016 overflow, what happens when a count goes past the top](./016-overflow.md) | next: not written yet
