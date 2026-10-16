# 011: why a gujarati letter takes 3 bytes and g takes 1
builds on: [002 bits, everything is a tiny switch](./002-bits.md), [003 counting in binary](./003-counting-in-binary.md), [004 bytes, 8 bits and 256 possible values](./004-bytes.md), [007 text is numbers, one character and one number](./007-text-is-numbers.md), [009 unicode, one number for every character](./009-unicode.md), [010 utf-8, storing those numbers in 1 to 4 bytes](./010-utf-8.md)
section: data at the atom level, part 11, ~2 min read

ગ is number 2711, and that needs only 12 [bits](./002-bits.md), the tiny on/off switches. so why does it cost 3 whole bytes, 24 bits?

because some bits in every [byte](./004-bytes.md) are labels, not letter. [UTF-8](./010-utf-8.md) stores each code point, the number [Unicode](./009-unicode.md) gives a character, in 1 to 4 bytes, and the first bits of each byte say what that byte is. in [010](./010-utf-8.md) i gave the ranges, heres where they come from.

```python
n = ord("ગ")
bits = format(n, "016b")
b1 = "1110" + bits[0:4]
b2 = "10" + bits[4:10]
b3 = "10" + bits[10:16]
print(bits)
print(b1, b2, b3)
print(bytes([int(b1, 2), int(b2, 2), int(b3, 2)]) == "ગ".encode())
```

```output
0000101010010111
11100000 10101010 10010111
True
```

the number gets padded to 16 bits and sliced 4, 6 and 6 across the three bytes. the first byte starts 1110, meaning "3 bytes long". the other two start 10, meaning "still the same character". thats 8 label bits out of 24, so 16 are left, and 16 bits count up to 65535, where the 3 byte range stops.

why not 2 bytes? those start 110 and keep only 11 free bits, up to 2047, and ગ needs 12. 1 byte keeps 7 (up to 127), since its label is a single 0.

the price shows up on whole words. dhokla, a steamed savory cake, is ઢોકળા in gujarati, and the shop, the imaginary snack store these notes run on, could sell either. strlen counts bytes, length counts code points:

```sql
SELECT strlen('dhokla') AS english_bytes, length('ઢોકળા') AS gujarati_code_points, strlen('ઢોકળા') AS gujarati_bytes;
```

```result
english_bytes | gujarati_code_points | gujarati_bytes
6 | 5 | 15
```

vowel signs like ો get their own code point, so you see 3 units on screen but it counts 5, all 3 bytes each in UTF-8.

i honestly thought a byte carried 8 bits of the letter. the labels were news to me.

### check yourself

1. a program opens a UTF-8 file at a random spot and the first byte is 10110001. can it be the start of a character? whats the safe move?
<details><summary>answer</summary>

no, it starts with 10, so it continues a character that began earlier. step back to the nearest byte that doesnt start with 10. the tempting answer is that any byte can start one, from treating bytes as independent letters.

</details>

2. predict the byte count after adding two ગ to the shop product fafda, a crunchy snack.
```sql
SELECT name, strlen(name || 'ગગ') AS bytes FROM products WHERE name = 'fafda';
```
<details><summary>answer</summary>

```result
name | bytes
fafda | 11
```
5 plain english letters at 1 byte plus 2 times 3. the tempting answer is 7, from counting each new character as one byte.

</details>

---
prev: [010 utf-8, storing those numbers in 1 to 4 bytes](./010-utf-8.md) | next: not written yet
