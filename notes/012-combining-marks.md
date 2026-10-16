# 012: combining marks, when one letter on screen is two numbers
builds on: [007 text is numbers, one character and one number](./007-text-is-numbers.md), [009 unicode, one number for every character](./009-unicode.md), [010 utf-8, storing those numbers in 1 to 4 bytes](./010-utf-8.md), [011 why a gujarati letter takes 3 bytes and g takes 1](./011-why-gujarati-takes-3-bytes.md)
section: data at the atom level, part 12, ~2 min read

two é that look identical on screen, and a database says theyre not equal. how?

a combining mark is a code point, the number [Unicode](./009-unicode.md) gives a character, that has no letter of its own. it attaches to the letter before it, so e followed by the accent mark draws é. the other way to get é is the single precomposed code point 233. both are valid, and the shop, the imaginary snack store these notes run on, would meet either in a customer name.

```sql
SELECT s, s = 'é' AS same_as_precomposed, length(s) AS code_points, strlen(s) AS bytes, length_grapheme(s) AS on_screen FROM (VALUES ('é'), ('e' || chr(769))) t(s);
```

```result
s | same_as_precomposed | code_points | bytes | on_screen
é | true | 1 | 2 | 1
é | false | 2 | 3 | 1
```

chr(769) is the accent mark. look at the s column, you cant tell the rows apart, but the database can. by default it compares code points one by one, never how the text looks. the second é is 2 code points, e (1 byte) plus the mark (2 bytes in [UTF-8](./010-utf-8.md)), and length_grapheme counts what you see, 1.

i kept assuming one thing on screen meant one number underneath. [011](./011-why-gujarati-takes-3-bytes.md) already hinted at it with the vowel sign ો, and ગુ is the same story, ગ plus the sign ુ, 2 code points and 6 bytes.

this bites in real systems: a search or a join on a name typed two ways just misses. the fix is normalizing both to one form before comparing, which is a later note. [source on the idea](https://en.wikipedia.org/wiki/Combining_character)

### check yourself

1. a customer form lets people type any text. someone enters Esha with an accent mark glued to the end. predict all three counts.
```sql
SELECT name, length(name || chr(769)) AS code_points, strlen(name || chr(769)) AS bytes, length_grapheme(name || chr(769)) AS on_screen FROM customers WHERE name = 'Esha';
```
<details><summary>answer</summary>

```result
name | code_points | bytes | on_screen
Esha | 5 | 6 | 4
```
the mark is a 5th code point costing 2 bytes, but it draws on the a, so you still see 4 letters. the tempting answer is 5 on screen, from counting every code point as a visible letter.

</details>

2. a signup checks "does this email already exist" with plain equality, and a user types their é precomposed once and combined the next time. what happens?
<details><summary>answer</summary>

the check says no match, so the same person gets a second account. equality compares code points, not looks. the tempting answer is that it matches, because the two look identical.

</details>

---
prev: [011 why a gujarati letter takes 3 bytes and g takes 1](./011-why-gujarati-takes-3-bytes.md) | next: [013 negative numbers, the sign bit idea](./013-negative-numbers-sign-bit.md)
