# 016: overflow, what happens when a count goes past the top
builds on: [003 counting in binary](./003-counting-in-binary.md), [014 twos complement, how computers really store a minus](./014-twos-complement.md), [015 integer sizes, 8, 16, 32 and 64 bit numbers](./015-integer-sizes.md)
section: data at the atom level, part 16, ~2 min read

[015](./015-integer-sizes.md) gave every integer a top, 127 for 8 bits. the shop, the imaginary snack store these notes run on, counts dhokla, a steamed savory cake, in an 8 bit counter reading 127. one more sale. what does it read?

overflow is when an answer needs more bits than its size has. watch the counter add 1 in [binary](./003-counting-in-binary.md), counting with only 0 and 1:

| sale | pattern | reads as |
|---|---|---|
| before | 01111110 | 126 |
| +1 | 01111111 | 127 |
| +1 | 10000000 | -128 |
| +1 | 10000001 | -127 |

the add did nothing odd, the 1s just carried left until they hit the leftmost place, which in [twos complement](./014-twos-complement.md) is worth negative. i kept picturing an alarm going off, but every pattern is valid, so nothing complains.

thats the quiet kind of bug, and you can hit it in any language that wraps. in 2014 YouTube said "Gangnam Style" passed 2147483647 views, the top of a 32 bit integer, and moved to 64 bit: https://en.wikipedia.org/wiki/Gangnam_Style

databases are stricter. DuckDB, the database these notes use, raises an error instead, and Postgres, a popular server database, does too. TINYINT is DuckDBs 8 bit integer:

```sql
-- fails on purpose
SELECT 127::TINYINT + 1::TINYINT AS next_count
```

### check yourself

1. the shops highest order_id is 107, and it fits in a TINYINT. the shop then gets 21 more orders. what does this do in DuckDB, and what would a silent wrapping counter show?
```sql
-- fails on purpose
SELECT max(order_id)::TINYINT + 21::TINYINT AS newest FROM orders
```
<details><summary>answer</summary>

107 + 21 is 128, one past the top of 127, so DuckDB raises an out of range error. a wrapping counter would show -128, not 128, since 128 has no 8 bit signed pattern. the tempting answer is 128, from forgetting the top is 127.

</details>

2. a signed 8 bit counter wrapped silently and now shows -56. what could it really have counted?
<details><summary>answer</summary>

200, or 456, or any 200 plus a multiple of 256, because every full lap of 256 patterns looks the same. you cannot tell which from the pattern. the tempting answer is that it counted 56 refunds, but wrapping creates the minus, nobody subtracted anything.

</details>

---
prev: [015 integer sizes, 8, 16, 32 and 64 bit numbers](./015-integer-sizes.md) | next: not written yet
