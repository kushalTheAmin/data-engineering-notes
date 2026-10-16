# 014: twos complement, how computers really store a minus
builds on: [003 counting in binary](./003-counting-in-binary.md), [004 bytes, 8 bits and 256 possible values](./004-bytes.md), [013 negative numbers, the sign bit idea](./013-negative-numbers-sign-bit.md)
section: data at the atom level, part 14, ~2 min read

the shop, the imaginary snack store these notes run on, refunds a dhokla, a steamed savory cake, at -6. [013](./013-negative-numbers-sign-bit.md) stored that with a sign bit and paid for it with two zeros. can a minus cost nothing?

twos complement keeps the place values of [binary](./003-counting-in-binary.md), counting with only 0 and 1, but makes the leftmost place worth negative. in a [byte](./004-bytes.md), a group of 8 bits, that place is -128 instead of +128.

| pattern | -128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 | number |
|---|---|---|---|---|---|---|---|---|---|
| 00000110 | 0 | 0 | 0 | 0 | 0 | 4 | 2 | 0 | 6 |
| 11111010 | -128 | 64 | 32 | 16 | 8 | 0 | 2 | 0 | -6 |
| 11111111 | -128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 | -1 |
| 10000000 | -128 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | -128 |
| 00000000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

read 11111010 like any binary, just add what is on: -128 + 64 + 32 + 16 + 8 + 2 comes to -6. i expected more machinery than one place getting a minus in front of its price tag.

now count: every pattern lands on its own number, and zero shows up once. 256 patterns, 256 values, from -128 to 127. the leading bit still tells you the sign, but it also carries weight.

to flip a sign without adding anything up, flip every bit and add 1:

```python
six = "00000110"
flipped = "".join("1" if b == "0" else "0" for b in six)
print(flipped, format(int(flipped, 2) + 1, "08b"))
```

```output
11111001 11111010
```

thats -6 again. the cost is lopsided, 127 on the plus side but 128 on the minus side, so -128 has no positive twin. in Java, Math.abs on the smallest int hands back a negative number, and the docs say so: https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Math.html

how many bits a number gets decides where that edge sits, and thats worth its own look.

---
prev: [013 negative numbers, the sign bit idea](./013-negative-numbers-sign-bit.md) | next: not written yet
