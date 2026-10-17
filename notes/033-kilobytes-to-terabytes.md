# 033: kilobytes to terabytes, how big data gets
builds on: [004 bytes, 8 bits and 256 possible values](./004-bytes.md), [011 why a gujarati letter takes 3 bytes and g takes 1](./011-why-gujarati-takes-3-bytes.md)
section: data at the atom level, part 33, ~2 min read

how big is a million shop orders? a billion? guess first, then look, you might be surprised.

a kilobyte (KB) is 1000 [bytes](./004-bytes.md), each a group of 8 on/off switches called bits. a megabyte (MB) is 1000 KB, a gigabyte (GB) is 1000 MB, a terabyte (TB) is 1000 GB. kilo, mega, giga and tera are metric prefixes, like in kilometre.

the shop, the imaginary gujarati snack store these notes run on, can write one order as a line of text: order id, customer id, time, status. text is stored as numbers, one per character. english letters, digits and commas take 1 byte each ([011](./011-why-gujarati-takes-3-bytes.md)), so the size is just the length:

```python
size = len("101,1,2026-04-01 09:15:00,delivered".encode())
units = ["bytes", "KB", "MB", "GB", "TB"]
for step in range(5):
    print(f"{1000 ** step:>17,} orders = {size} {units[step]}")
```

```output
                1 orders = 35 bytes
            1,000 orders = 35 KB
        1,000,000 orders = 35 MB
    1,000,000,000 orders = 35 GB
1,000,000,000,000 orders = 35 TB
```

order 101 is 35 bytes, and the shops other six orders land between 33 and 35. every row below is 1000 times the one above, so the 35 never moves, only the label does. i expected a trillion rows to need a whole different kind of thinking, but its the same 35 with a bigger word on it.

two gotchas. a capital B is bytes and a lowercase b is bits, so 100 megabits a second is 12.5 megabytes a second. and some tools count 1024 per step, not 1000, which makes the same file look a bit different. a later note sorts it out.

this is only the text size, real systems store it differently, but multiplying it out is a fast way to check if something fits.

next up, one order decoded all the way down.

---
prev: [032 null is not zero and not empty text](./032-null-is-not-zero-or-empty-text.md) | next: [034 capstone, one shop order decoded down to bytes](./034-capstone-one-order-decoded-to-bytes.md)
