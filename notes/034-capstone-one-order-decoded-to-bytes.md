# 034: capstone, one shop order decoded down to bytes
builds on: [001 data is facts written down, and a computer only keeps numbers](./001-data-is-facts-and-numbers.md), [002 bits, everything is a tiny switch](./002-bits.md), [003 counting in binary](./003-counting-in-binary.md), [004 bytes, 8 bits and 256 possible values](./004-bytes.md), [005 hexadecimal, counting with sixteen digits](./005-hexadecimal.md), [006 one byte, two hex digits](./006-one-byte-two-hex-digits.md), [007 text is numbers, one character and one number](./007-text-is-numbers.md), [008 ascii runs out, 128 spots isnt enough for the world](./008-ascii-runs-out.md), [009 unicode, one number for every character](./009-unicode.md), [010 utf-8, storing those numbers in 1 to 4 bytes](./010-utf-8.md), [011 why a gujarati letter takes 3 bytes and g takes 1](./011-why-gujarati-takes-3-bytes.md), [012 combining marks, when one letter on screen is two numbers](./012-combining-marks.md), [013 negative numbers, the sign bit idea](./013-negative-numbers-sign-bit.md), [014 twos complement, how computers really store a minus](./014-twos-complement.md), [015 integer sizes, 8, 16, 32 and 64 bit numbers](./015-integer-sizes.md), [016 overflow, what happens when a count goes past the top](./016-overflow.md), [017 fractions in binary, halves, quarters, eighths](./017-fractions-in-binary.md), [018 why 0.1 has no exact binary form](./018-why-0-1-has-no-exact-binary-form.md), [019 floating point, digits plus where the point sits](./019-floating-point.md), [020 why 0.1 + 0.2 is not exactly 0.3](./020-why-0-1-plus-0-2-is-not-0-3.md), [021 storing money as whole cents](./021-storing-money-as-whole-cents.md), [022 exact decimal types](./022-exact-decimal-types.md), [023 true and false, the boolean](./023-true-and-false-the-boolean.md), [024 UTC, the worlds reference clock](./024-utc.md), [025 unix time, counting seconds from 1970](./025-unix-time.md), [026 seconds, milliseconds, microseconds: one moment, three numbers](./026-seconds-milliseconds-microseconds.md), [027 dates without times, and times without dates](./027-dates-and-times-apart.md), [028 time zones, offsets from UTC](./028-time-zone-offsets.md), [029 daylight saving, the hour that happens twice](./029-daylight-saving.md), [030 store in UTC, show in local time](./030-store-utc-show-local.md), [031 null, a marker for a missing value](./031-null.md), [032 null is not zero and not empty text](./032-null-is-not-zero-or-empty-text.md), [033 kilobytes to terabytes, how big data gets](./033-kilobytes-to-terabytes.md)
section: data at the atom level, wrap up, ~3 min read

one shop order is 35 bytes. can you say what every one of them means, and which earlier note explains it?

the shop, the imaginary gujarati snack store these notes run on, can write order 101 as one line of text. a byte is a group of 8 bits, switches that are on or off. this section was about that one line, so here it is cut at the commas, with each piece as hex, two digits per byte:

```python
line = "101,1,2026-04-01 09:15:00,delivered"
for field in line.split(","):
    b = field.encode()
    print(f"{field:<21}{len(b):>2} bytes  {b.hex(' ')}")
```

```output
101                   3 bytes  31 30 31
1                     1 bytes  31
2026-04-01 09:15:00  19 bytes  32 30 32 36 2d 30 34 2d 30 31 20 30 39 3a 31 35 3a 30 30
delivered             9 bytes  64 65 6c 69 76 65 72 65 64
```

3 + 1 + 19 + 9 is 32, plus 3 commas is 35, the size [033](./033-kilobytes-to-terabytes.md) scaled up to terabytes. the 101 is not the number 101, it is the three bytes 31 30 31, the characters 1, 0, 1. as a real number, 101 would be a 32 bit integer, 65 in hex padded to 00 00 00 65 (many machines keep those bytes in reverse), and the time, read as New York time, would be the count 1775049300 seconds. every piece of the line sits on top of an idea from this section:

| layer | what it settled | notes |
|---|---|---|
| facts to numbers | a computer keeps only numbers | [001](./001-data-is-facts-and-numbers.md) |
| switches | bits, binary, bytes, hex | [002](./002-bits.md) [003](./003-counting-in-binary.md) [004](./004-bytes.md) [005](./005-hexadecimal.md) [006](./006-one-byte-two-hex-digits.md) |
| text | characters, ASCII, Unicode, UTF-8, marks | [007](./007-text-is-numbers.md) [008](./008-ascii-runs-out.md) [009](./009-unicode.md) [010](./010-utf-8.md) [011](./011-why-gujarati-takes-3-bytes.md) [012](./012-combining-marks.md) |
| whole numbers | minus signs, sizes, overflow | [013](./013-negative-numbers-sign-bit.md) [014](./014-twos-complement.md) [015](./015-integer-sizes.md) [016](./016-overflow.md) |
| fractions and money | floats, cents, decimals | [017](./017-fractions-in-binary.md) [018](./018-why-0-1-has-no-exact-binary-form.md) [019](./019-floating-point.md) [020](./020-why-0-1-plus-0-2-is-not-0-3.md) [021](./021-storing-money-as-whole-cents.md) [022](./022-exact-decimal-types.md) |
| yes or no | the boolean | [023](./023-true-and-false-the-boolean.md) |
| time | UTC, unix time, zones, daylight saving | [024](./024-utc.md) [025](./025-unix-time.md) [026](./026-seconds-milliseconds-microseconds.md) [027](./027-dates-and-times-apart.md) [028](./028-time-zone-offsets.md) [029](./029-daylight-saving.md) [030](./030-store-utc-show-local.md) |
| missing | null, and not 0 or empty text | [031](./031-null.md) [032](./032-null-is-not-zero-or-empty-text.md) |
| size | KB to TB | [033](./033-kilobytes-to-terabytes.md) |

i expected the line to carry its own meaning. it carries none, 31 30 31 only reads as 101 because everyone agreed on the rule, which is the catch from [001](./001-data-is-facts-and-numbers.md) showing up again at the end. so the wrong unit, the wrong zone and a 0 standing in for missing are all the same bug: two sides using different rules.

### check yourself

1. the 35 bytes are order 101. predict the line size for orders 104 and 106, where the line is order_id, customer_id, ordered_at and status, glued with commas. SELECT picks columns, FROM names the table, WHERE keeps matching rows, IN matches any id in a list, strlen counts bytes, || glues text together and ::VARCHAR turns a number into text.
```sql
SELECT order_id, strlen(order_id::VARCHAR || ',' || customer_id::VARCHAR || ',' || ordered_at::VARCHAR || ',' || status) AS line_bytes FROM orders WHERE order_id IN (104, 106);
```
<details><summary>answer</summary>

```result
order_id | line_bytes
104 | 35
106 | 33
```
cancelled is 9 bytes like delivered, but pending is 7, so 106 is 2 bytes shorter. the tempting answer is 35 for both, from thinking a line is a fixed size. text lines vary with their words.

</details>

2. a loader reads the stored count 1775049300 as milliseconds, not seconds. epoch_ms turns a millisecond count into a timestamp. what moment does it show?
```sql
SELECT epoch_ms(1775049300) AS shown;
```
<details><summary>answer</summary>

```result
shown
1970-01-21 13:04:09.300000
```
1775049300 thousandths of a second is only about 20 days, so it lands in January 1970. the tempting answer is 1 April 2026, from trusting that the number already means seconds. the bytes never say which unit.

</details>

---
prev: [033 kilobytes to terabytes, how big data gets](./033-kilobytes-to-terabytes.md) | next: [035 the processor, the part that does the work](./035-the-processor.md)
