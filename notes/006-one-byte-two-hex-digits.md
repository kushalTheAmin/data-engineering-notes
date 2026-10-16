# 006: one byte, two hex digits
builds on: [001 data is facts written down](./001-data-is-facts-and-numbers.md), [003 counting in binary](./003-counting-in-binary.md), [004 bytes, 8 bits and 256 possible values](./004-bytes.md), [005 hexadecimal, counting with sixteen digits](./005-hexadecimal.md)
section: data at the atom level, part 6, ~2 min read

why is ff the same as 255, and why does every byte in a hex dump (a raw listing of a file) show as two characters?

because a [byte](./004-bytes.md), a group of 8 on/off switches called bits, is two [hex](./005-hexadecimal.md) digits, always. hex counts 0 to 9 then a to f (ten to fifteen), 16 digits, and 16 is 2 times 2 times 2 times 2, so one digit covers exactly 4 bits. cut the byte in half, one digit each.

here are the 6 bytes of "dhokla", a steamed savory cake from the shop, the imaginary snack store these notes use:

| letter | the byte | first 4 bits | last 4 bits | hex |
|---|---|---|---|---|
| d | 01100100 | 0110 = 6 | 0100 = 4 | 64 |
| h | 01101000 | 0110 = 6 | 1000 = 8 | 68 |
| o | 01101111 | 0110 = 6 | 1111 = f | 6f |
| k | 01101011 | 0110 = 6 | 1011 = b | 6b |
| l | 01101100 | 0110 = 6 | 1100 = c | 6c |
| a | 01100001 | 0110 = 6 | 0001 = 1 | 61 |

every row is the same move: split in the middle, read each half as 0 to 15, write one hex digit. all six start with 6 because of where letters sit in the number code from [001](./001-data-is-facts-and-numbers.md).

now ff. 1111 1111 is f twice, and f is 15. the left digit sits in the 16s place, same [place value](./003-counting-in-binary.md) idea, a digit is worth what its spot says, so:

```python
print(15 * 16 + 15)
print(int("ff", 16))
```

```output
255
255
```

thats the top of a byte, and 00 is the bottom. 16 times 16 is the 256 values from [004](./004-bytes.md), so i stopped seeing 256 as random.

the gotcha: in a hex dump the byte 5 is written 05, never 5, or the bytes 1 and 2 side by side read 12, same as the one byte 12. you will meet pairs in web colors: #ff8000 is three bytes, red ff, green 80, blue 00.

### check yourself

1. a log prints two bytes as "1f2" with no spaces. can you tell what the bytes are?

<details><summary>answer</summary>

no. bytes are always two digits, so "1f2" has an odd count and something dropped a leading zero. it could be 01 f2 or 1f 02. the tempting answer is 1f and 2, but 2 alone isnt a whole byte.

</details>

2. in the shop, jalebi starts with the byte 6a and khandvi with 6b. what are they in decimal?

<details><summary>answer</summary>

106 and 107. 6 sixteens is 96, plus a (10) is 106, plus b (11) is 107. the tempting answer is 16 and 17, from adding the digits instead of using the 16s place.

</details>

3. what is the color #00ff00 in decimal red, green and blue?

<details><summary>answer</summary>

0, 255, 0. split into pairs 00, ff, 00, each pair is one byte. its pure green. the tempting answer is 0, 30, 0, from adding f and f instead of using the 16s place.

</details>

---
prev: [005 hexadecimal, counting with sixteen digits](./005-hexadecimal.md) | next: [007 text is numbers, one character and one number](./007-text-is-numbers.md)
