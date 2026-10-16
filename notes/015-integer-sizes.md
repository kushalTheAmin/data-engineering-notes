# 015: integer sizes, 8, 16, 32 and 64 bit numbers
builds on: [004 bytes, 8 bits and 256 possible values](./004-bytes.md), [014 twos complement, how computers really store a minus](./014-twos-complement.md)
section: data at the atom level, part 15, ~2 min read

the shop, the imaginary snack store these notes run on, has order ids 101 to 107 so far. if order_id were stored in one [byte](./004-bytes.md), a group of 8 bits, what would you guess happens at order 128?

an integer size is how many bits a whole number gets. the bits decide the range, because [twos complement](./014-twos-complement.md), where the leftmost place is negative, splits the patterns between minus and plus, with one extra on the minus side. in code, thats this:

```python
for bits in [8, 16, 32, 64]:
    low = -(2 ** (bits - 1))
    high = 2 ** (bits - 1) - 1
    print(bits, bits // 8, low, high)
```

```output
8 1 -128 127
16 2 -32768 32767
32 4 -2147483648 2147483647
64 8 -9223372036854775808 9223372036854775807
```

columns: bits, bytes, lowest, highest. so at 8 bits the shop dies at order 128, since 127 is the top. i assumed the sizes would be some careful choice, but its just doubling the bits again and again, and each doubling squares the number of values, which is why 32 to 64 jumps from billions to nine quintillion.

the shops order_id is declared INTEGER, which is 32 bit in both Postgres, a server database, and DuckDB, the database these notes use. DuckDB refuses to fit 2147483648 into an INTEGER, and its own name for the 64 bit type is BIGINT. same idea in Postgres, where smallint, integer and bigint are 2, 4 and 8 bytes: https://www.postgresql.org/docs/current/datatype-numeric.html

one gotcha: the size is fixed per column, not per value. a 3 stored in a Postgres bigint column still takes 8 bytes (DuckDB compresses on disk, but the range stays fixed), and python ints dont have this limit, which is why a script can look fine and a database column still overflows.

---
prev: [014 twos complement, how computers really store a minus](./014-twos-complement.md) | next: [016 overflow, what happens when a count goes past the top](./016-overflow.md)
