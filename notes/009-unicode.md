# 009: unicode, one number for every character
builds on: [007 text is numbers, one character and one number](./007-text-is-numbers.md), [008 ascii runs out, 128 spots isnt enough for the world](./008-ascii-runs-out.md)
section: data at the atom level, part 9, ~2 min read

can one table hold the letters of every language, so byte 233 never means two different things again?

yes, its called Unicode: one table where every [character](./007-text-is-numbers.md), one letter, digit or symbol, gets its own number, a code point. the shop, the imaginary snack store these notes run on, can finally spell dhokla, a steamed savory cake, in gujarati.

```python
for ch in ["a", "é", "ગ", "ઢ", "🙂"]:
    n = ord(ch)
    print(ch, n, "U+" + format(n, "04X"))
print(0x10FFFF + 1)
```

```output
a 97 U+0061
é 233 U+00E9
ગ 2711 U+0A97
ઢ 2722 U+0AA2
🙂 128578 U+1F642
1114112
```

the same `ord` from [007](./007-text-is-numbers.md) works on all of them. U+ then the number in [hex](./005-hexadecimal.md), counting with sixteen digits, is how Unicode people write it. the last line is how many spots exist, over a million, with over 150,000 filled so far.

two things stand out. a still gets 97, so everything [ASCII](./008-ascii-runs-out.md), the old 128 character table, did stays true. and ઢ is 2722, way past what one [byte](./004-bytes.md), a group of 8 bits, can hold.

that second one tripped me up. i expected Unicode to say how the numbers sit in a file, but it only hands out numbers. how would you store 2722 in bytes? separate question.

### check yourself

1. the shop query below grabs the code point of the first letter of each product name starting with k. predict the result.
```sql
SELECT name, unicode(name) AS first_letter FROM products WHERE name LIKE 'k%' ORDER BY name;
```
<details><summary>answer</summary>

```result
name | first_letter
kaju katli | 107
khandvi | 107
```
only the first letter counts, and both start with k. the tempting guess is two different numbers, from reading the whole name.

</details>

2. a friend says "Unicode gives ઢ the number 2722, so store it in one byte". whats wrong?
<details><summary>answer</summary>

a byte tops out at 255 and 2722 is bigger, so it cant fit. Unicode only picks the number, not how it gets stored. the tempting answer is that the table is broken, but its the storage step thats missing.

</details>

---
prev: [008 ascii runs out, 128 spots isnt enough for the world](./008-ascii-runs-out.md) | next: not written yet
