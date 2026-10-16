# 008: ascii runs out, 128 spots isnt enough for the world
builds on: [004 bytes, 8 bits and 256 possible values](./004-bytes.md), [007 text is numbers, one character and one number](./007-text-is-numbers.md)
section: data at the atom level, part 8, ~2 min read

what happens if the shop, the imaginary snack store these notes run on, wants to store dhokla, a steamed savory cake, in gujarati, the language of the state Gujarat in India?

the table from [007](./007-text-is-numbers.md), where every [character](./007-text-is-numbers.md) gets one number, is called ASCII, and it only has 128 spots, numbered 0 to 127. thats half of the 256 values a [byte](./004-bytes.md), a group of 8 bits, can hold. english fits. a gujarati letter has no spot at all.

```python
for ch in ["d", "~", "é", "ગ"]:
    n = ord(ch)
    print(repr(ch), n, "has a spot" if n < 128 else "no spot")
word = "ઢોકળા"
print(len(word), [ord(c) for c in word])
try:
    word.encode("ascii")
except UnicodeEncodeError:
    print("ascii cant store dhokla in gujarati")
```

```output
'd' 100 has a spot
'~' 126 has a spot
'é' 233 no spot
'ગ' 2711 no spot
5 [2722, 2763, 2709, 2739, 2750]
ascii cant store dhokla in gujarati
```

even é, one accent away from english, has no spot. the gujarati word is 5 characters and every one of them has a number far past 127, so ascii simply refuses.

the obvious fix is to use the other 128 values in the byte, and countries did exactly that, each with its own table. so one byte, 233, shows as é in one table and й in another. i kept assuming a byte meant one letter everywhere, it doesnt.

thats why old files and emails turn into garbage when opened with the wrong table, and why you still see broken text in a CSV someone exported from an old system. you need one table for everyone, which is where the next note goes.

---
prev: [007 text is numbers, one character and one number](./007-text-is-numbers.md) | next: [009 unicode, one number for every character](./009-unicode.md)
