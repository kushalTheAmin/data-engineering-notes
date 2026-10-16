# 005: hexadecimal, counting with sixteen digits
builds on: [003 counting in binary](./003-counting-in-binary.md), [004 bytes, 8 bits and 256 possible values](./004-bytes.md)
section: data at the atom level, part 5, ~2 min read

in [004](./004-bytes.md) the first byte of "dhokla" (the steamed savory cake sold in the shop, the imaginary snack store) was 01100100. eight digits for one letter. nobody wants to read a file like that, so what do people do instead?

hexadecimal, or hex, is counting with sixteen digits instead of ten. after 0 to 9 it borrows letters: a is ten, b is eleven, up to f, which is fifteen.

heres the whole alphabet next to [binary](./003-counting-in-binary.md), counting with only 0 and 1:

| decimal | binary | hex |
|---|---|---|
| 0 | 0000 | 0 |
| 1 | 0001 | 1 |
| 2 | 0010 | 2 |
| 3 | 0011 | 3 |
| 4 | 0100 | 4 |
| 5 | 0101 | 5 |
| 6 | 0110 | 6 |
| 7 | 0111 | 7 |
| 8 | 1000 | 8 |
| 9 | 1001 | 9 |
| 10 | 1010 | a |
| 11 | 1011 | b |
| 12 | 1100 | c |
| 13 | 1101 | d |
| 14 | 1110 | e |
| 15 | 1111 | f |

4 [bits](./002-bits.md), on/off switches, make 2 times 2 times 2 times 2, so 16 patterns, and each gets exactly one hex digit. thats why hex exists, it squeezes switches into fewer characters.

past f you carry, same as 9 to 10 in everyday counting. the left place is worth 16 and the right place is worth 1. so hex 64 is 6 sixteens plus 4 ones, as a loop:

```python
digits = "0123456789abcdef"
pattern = "64"
place_values = [16, 1]
total = 0
for i in range(2):
    total = total + digits.index(pattern[i]) * place_values[i]
print(total)
```

```output
100
```

same loop as 003, with `digits.index` turning f into 15. 100 is the number for "d" from 004. the gotcha: hex 10 means sixteen, not ten, so a bare "64" could be sixty four or a hundred. python marks hex with a 0x in front, hex(100) gives 0x64.

i kept reading a, b, c as letters, they are just digits that ran out of numerals. you see this daily: every commit id in git, the tool that keeps a history of code, like ceeaa63, is written in hex.

---
prev: [004 bytes, 8 bits and 256 possible values](./004-bytes.md) | next: [006 one byte, two hex digits](./006-one-byte-two-hex-digits.md)
