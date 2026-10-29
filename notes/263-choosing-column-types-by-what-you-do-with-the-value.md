# 263: choosing column types, ask what you do with the value
builds on: [262 denormalization, copying data on purpose](./262-denormalization-copying-data-on-purpose.md), [256 one to one, when two tables share a key](./256-one-to-one-when-two-tables-share-a-key.md), [132 CAST, changing a values type](./132-cast-changing-a-values-type.md), [080 every column holds one type](./080-every-column-holds-one-type.md), [140 sum and avg, adding up and averaging](./140-sum-and-avg-adding-up-and-averaging.md), [015 integer sizes, 8, 16, 32 and 64 bit numbers](./015-integer-sizes.md)
section: designing tables, part 10, ~2 min read

the shop (the imaginary gujarati snack store these notes run on) has support confirm a caller by the last 4 digits of their phone. store those 4 digits as a number instead of text and what does Bhavin read out?

in [262](./262-denormalization-copying-data-on-purpose.md) the choice was where a fact lives. the other choice per column is its [type](./080-every-column-holds-one-type.md) (the kind of value allowed), and the rule is to pick it by what you do with the value, not by what it looks like. add or average it: number. only show and compare it: text.

phones sit in customer_contacts from [256](./256-one-to-one-when-two-tables-share-a-key.md) as VARCHAR (text). right(phone, 4) keeps the last 4 characters, and [CAST](./132-cast-changing-a-values-type.md) (turn a value into another type) makes them a number. all 3 rows:

```sql
SELECT right(phone, 4) AS as_text, CAST(right(phone, 4) AS INTEGER) AS as_number FROM customer_contacts ORDER BY customer_id
```

```result
as_text | as_number
0101 | 101
0102 | 102
0104 | 104
```

Bhavin reads out 0102 and the system holds 102. the leading zero (a 0 in front of the other digits) is gone, because a number only has a size, and 102 is the same number as 0102. casting back gives 102, not 0102.

sniff test: [average](./140-sum-and-avg-adding-up-and-averaging.md) those 3 and you get 102.33, which means nothing. if avg is nonsense on a column, it holds digits but isnt a number.

numbers also have a size limit. a 32 bit [INTEGER](./015-integer-sizes.md) tops out at 2147483647, so a made up phone like 9876543210 doesnt fit, and DuckDB, the database these notes run in, errors on that cast.

i assumed a column full of digits was a number column, but the test is whether adding two of them means anything.

### check yourself

1. the shop stores last4 as a number, then converts back to text to compare with what the caller typed. predict how many of the 3 rows survive the round trip unchanged.
```sql
SELECT count(*) AS matches FROM customer_contacts WHERE CAST(CAST(right(phone, 4) AS INTEGER) AS VARCHAR) = right(phone, 4)
```
<details><summary>answer</summary>

```result
matches
0
```

0, because all 3 start with a zero and 0101 comes back as 101. the tempting answer is 3, since turning something into a number and back feels like it should return the original.

</details>

2. the shop adds a discount_code column holding values like 007 and a loyalty_points column holding values like 40. which gets text and which gets a number, and why?
<details><summary>answer</summary>

discount_code is text, 007 would become 7 as a number, and nobody adds two codes. loyalty_points is a number, you add and compare it. the tempting answer is number for both, since both are only digits.

</details>

---
prev: [262 denormalization, copying data on purpose](./262-denormalization-copying-data-on-purpose.md) | next: [264 naming conventions, names people can guess](./264-naming-conventions-names-people-can-guess.md)
