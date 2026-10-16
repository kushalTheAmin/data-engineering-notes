# 013: negative numbers, the sign bit idea
builds on: [002 bits, everything is a tiny switch](./002-bits.md), [003 counting in binary](./003-counting-in-binary.md), [004 bytes, 8 bits and 256 possible values](./004-bytes.md)
section: data at the atom level, part 13, ~2 min read

the shop, the imaginary snack store these notes run on, refunds a dhokla, a steamed savory cake that costs 6.00. so the amount is -6. but a computer only has 0s and 1s, so where does the minus go?

the simplest idea: spend one [bit](./002-bits.md), one on/off switch, as the sign. 0 means plus, 1 means minus, and the other 7 bits of the [byte](./004-bytes.md), a group of 8 bits, hold the size in plain [binary](./003-counting-in-binary.md), counting with only 0 and 1.

```python
for bits in ["00000110", "10000110", "00000000", "10000000"]:
    sign = "minus" if bits[0] == "1" else "plus"
    print(bits, sign, int(bits[1:], 2))
```

```output
00000110 plus 6
10000110 minus 6
00000000 plus 0
10000000 minus 0
```

first row is 6, second row is the same size with the sign bit flipped, so -6. nothing else changes. thats the whole trick.

but look at the last two rows. "minus 0" is a real pattern, so this scheme has two zeros. i didnt expect negative numbers to cost a pattern. with 7 size bits the biggest size is 127, so the range is -127 to 127, which is 255 values, not 256.

this isnt only history. floating point numbers, which come later, use a sign bit like this, and python really does have a -0.0 that equals 0.0:

```python
print(-0.0, -0.0 == 0.0)
```

```output
-0.0 True
```

so a stored -0.0 can print with a minus even though it equals 0. you will see it in an export one day.

plain integers in most computers dont use this scheme though, they use a cleverer one that fixes the two zeros, and thats what comes next.

### check yourself

1. the shop refunds one kaju katli, a sweet. its price as a whole number is below. using the sign bit idea in 8 bits, what pattern is the refund?
```sql
SELECT name, CAST(price AS INTEGER) AS whole FROM products WHERE name = 'kaju katli';
```
<details><summary>answer</summary>

```result
name | whole
kaju katli | 12
```
12 is 1100 in binary, so 0001100 in the 7 size bits, and the sign bit is 1: 10001100. the tempting answer is 11100, from putting the sign on the front of 1100 without padding the size to 7 bits.

</details>

2. a program compares 10000000 and 00000000 as numbers, then as raw bit patterns. what does each comparison say?
<details><summary>answer</summary>

as numbers they are equal, both are zero. as raw patterns they differ, so a byte-by-byte compare says not equal. the tempting answer is that the first one is bigger, from reading the leading 1 as a big number.

</details>

---
prev: [012 combining marks, when one letter on screen is two numbers](./012-combining-marks.md) | next: [014 twos complement, how computers really store a minus](./014-twos-complement.md)
