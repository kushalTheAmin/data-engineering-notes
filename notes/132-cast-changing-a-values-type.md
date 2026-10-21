# 132: CAST, changing a values type
builds on: [007 text is numbers, one character, one number](./007-text-is-numbers.md), [022 exact decimal types](./022-exact-decimal-types.md), [080 every column holds one type](./080-every-column-holds-one-type.md), [122 computed columns and AS](./122-computed-columns-and-as.md), [131 integer division, when 7 / 2 gives 3](./131-integer-division-when-7-divided-by-2-gives-3.md)
section: asking questions with SQL, part 32, ~2 min read

khandvi costs 7.50. turn that price into a whole number, and do you get 7 or 8?

CAST(value AS type) takes a value and gives you the same thing as a different type. every [column holds one type](./080-every-column-holds-one-type.md) (all values the same kind), and CAST is how you ask for another kind, like text to number or decimal to whole number. in [131](./131-integer-division-when-7-divided-by-2-gives-3.md) i dodged it by writing 2.0, CAST is the proper way.

in python, int() on a decimal chops the end off. the shop, the imaginary gujarati snack store these notes run on, has prices in a slice of 3 products, stored as [exact decimals](./022-exact-decimal-types.md) (exact digits, fixed after the point):

```python
from decimal import Decimal
for name, p in [("dhokla", Decimal("6.00")), ("khandvi", Decimal("7.50")), ("fafda", Decimal("4.50"))]:
    print(name, p, int(p))
```

```output
dhokla 6.00 6
khandvi 7.50 7
fafda 4.50 4
```

same three prices through CAST in DuckDB, plus a cast to text:

```sql
SELECT name, price, CAST(price AS INTEGER) AS whole, CAST(price AS VARCHAR) AS as_text FROM products WHERE product_id IN (1, 2, 6) ORDER BY product_id
```

```result
name | price | whole | as_text
dhokla | 6.00 | 6 | 6.00
khandvi | 7.50 | 8 | 7.50
fafda | 4.50 | 5 | 4.50
```

i assumed casting to integer chopped off the decimals like python does, and in DuckDB it rounds. 7.50 becomes 8, 4.50 becomes 5. VARCHAR (text) keeps every digit, it just stops being a number.

this bites with text that looks like numbers, which CSV exports are full of. as text, '9' is less than '10' comes out false, because text compares one [character](./007-text-is-numbers.md) at a time and 9 beats 1:

```sql
SELECT '9' < '10' AS as_text, CAST('9' AS INTEGER) < CAST('10' AS INTEGER) AS as_numbers
```

```result
as_text | as_numbers
false | true
```

so if a number column sorts weirdly, check its type first. what happens when the text isnt a number at all? the next one covers it.

---
prev: [131 integer division, when 7 / 2 gives 3](./131-integer-division-when-7-divided-by-2-gives-3.md) | next: [133 casts that fail, and TRY_CAST](./133-casts-that-fail-and-try-cast.md)
