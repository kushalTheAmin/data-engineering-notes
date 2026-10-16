# 007: text is numbers, one character and one number
builds on: [001 data is facts written down](./001-data-is-facts-and-numbers.md), [004 bytes, 8 bits and 256 possible values](./004-bytes.md), [006 one byte, two hex digits](./006-one-byte-two-hex-digits.md)
section: data at the atom level, part 7, ~2 min read

order 101 in the shop, the imaginary snack store these notes run on, has a quantity of 2. if that order sits in a text file, is the 2 in there stored as the number 2?

no. a character, meaning one letter, digit, space or symbol, is stored as one number from an agreed table, and the character 2 is not the number 2.

[001](./001-data-is-facts-and-numbers.md) showed letters turning into numbers. the same rule covers everything you can type. each number here fits in one [byte](./004-bytes.md), a group of 8 bits, and the last column is that byte in [hex](./006-one-byte-two-hex-digits.md), how a file viewer would show it:

| character | its number | the byte in hex |
|---|---|---|
| 2 | 50 | 32 |
| A | 65 | 41 |
| a | 97 | 61 |
| (a space) | 32 | 20 |

```python
for ch in ["2", "A", "a", " "]:
    print(repr(ch), ord(ch), format(ord(ch), "02x"))
print("2" + "2", 2 + 2)
print(sorted(["10", "9", "2"]))
```

```output
'2' 50 32
'A' 65 41
'a' 97 61
' ' 32 20
22 4
['10', '2', '9']
```

so the 2 in that file is really the byte 32 in hex, which is the number 50. the space gets a number too, and A and a get different ones, which is why "Asha" and "asha" are not equal in python.

the last two lines are the bite. adding "2" and "2" as text glues them into 22, and sorting "10", "9" and "2" as text puts 10 first, because it compares character by character from the left, and the character 1 is 49, before 2 at 50 and 9 at 57. numbers that were saved as text sort wrong all the time, one of the classic CSV surprises.

i honestly assumed the 2 in a file was just a 2. it isnt, you only see it that way because your screen turns the number back into a shape.

---
prev: [006 one byte, two hex digits](./006-one-byte-two-hex-digits.md) | next: [008 ascii runs out, 128 spots isnt enough for the world](./008-ascii-runs-out.md)
