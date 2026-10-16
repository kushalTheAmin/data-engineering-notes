# 003: counting in binary
builds on: [002 bits, everything is a tiny switch](./002-bits.md)
section: data at the atom level, part 3, ~2 min read

if a row of switches like 101 is all a computer has, how is that the number 5?

binary is counting with only two digits, 0 and 1, where each place is worth double the place to its right.

you already read numbers by place. in 345 the 3 is worth hundreds, the 4 tens, the 5 ones, each place ten times the one to its right. this clicked for me once i saw binary is the exact same idea, with two instead of ten.

[bits](./002-bits.md), tiny on/off switches written 0 or 1, make patterns: 1 switch makes 2, 2 make 4, 3 make 8. to read them as numbers, give each place a value, 1 on the right, then 2, then 4, and add up the places that are on:

| pattern | 4s place | 2s place | 1s place | number |
|---|---|---|---|---|
| 000 | 0 | 0 | 0 | 0 |
| 001 | 0 | 0 | 1 | 1 |
| 010 | 0 | 2 | 0 | 2 |
| 011 | 0 | 2 | 1 | 3 |
| 100 | 4 | 0 | 0 | 4 |
| 101 | 4 | 0 | 1 | 5 |
| 110 | 4 | 2 | 0 | 6 |
| 111 | 4 | 2 | 1 | 7 |

find 101: the 4 is on, the 2 is off, the 1 is on. 4 plus 1 is 5. every pattern gets its own number, 0 to 7, none missing, none twice. a fourth switch would add an 8s place, then 16, and so on to the left. the same rule as a loop, for 3 switches:

```python
pattern = "101"
place_values = [4, 2, 1]
total = 0
for i in range(3):
    if pattern[i] == "1":
        total = total + place_values[i]
print(total)
```

```output
5
```

this rule sits under a famous date bug. many older systems count seconds since 1970 using 32 switches, but one is reserved for marking negative numbers, so 31 do the counting. the most 31 switches can hold is 2,147,483,647 seconds, about 68 years, which runs out on january 19, 2038. one second later those clocks wrap around to december 1901.

### check yourself

1. someone sees the binary 1000 and reads it as one thousand. what number is it really, and what would you write in binary to get 9?

<details><summary>answer</summary>

its 8. only the 8s place is on, the 4, 2 and 1 places are off. 9 is 8 plus 1, so 1001. the trap is reading binary with the ten digit rules you grew up with.

</details>

2. the shop, an imaginary online snack store, wants a binary code for each of its 6 products, using as few switches as possible. how many switches, and how many codes go unused?

<details><summary>answer</summary>

3 switches make 8 patterns, so 2 codes go unused. 2 switches only make 4 patterns, not enough. the tempting answer is 6 switches, one per product, but doubling means you need far fewer.

</details>

3. 4 switches make 16 patterns. so why is the biggest number they can show 15 and not 16?

<details><summary>answer</summary>

one of the 16 patterns, 0000, is spent on zero, so they cover 0 through 15. the tempting answer is 16, from counting the patterns and forgetting that zero takes one of them.

</details>

---
prev: [002 bits, everything is a tiny switch](./002-bits.md) | next: [004 bytes, 8 bits and 256 possible values](./004-bytes.md)
