# 041: text files vs binary files
builds on: [004 bytes, 8 bits and 256 possible values](./004-bytes.md), [010 utf-8, storing those numbers in 1 to 4 bytes](./010-utf-8.md), [015 integer sizes, 8, 16, 32 and 64 bit numbers](./015-integer-sizes.md), [034 capstone, one shop order decoded down to bytes](./034-capstone-one-order-decoded-to-bytes.md), [039 a file is a named list of bytes](./039-a-file-is-a-named-list-of-bytes.md)
section: memory, disks and files, part 7, ~2 min read

the shop, the imaginary gujarati snack store these notes run on, has order id 101. stored as a number it takes 4 bytes, stored as text it takes 3. so is text the small one?

a file is just [bytes](./004-bytes.md), groups of 8 bits, as [039](./039-a-file-is-a-named-list-of-bytes.md) said. a text file is one whose bytes decode as characters, usually with [UTF-8](./010-utf-8.md), which stores each character in 1 to 4 bytes. a binary file is any other layout, like a number packed into a fixed [integer size](./015-integer-sizes.md), here 4 bytes, the way [034](./034-capstone-one-order-decoded-to-bytes.md) showed it:

```python
import struct
for n in [101, 100000]:
    as_text = str(n).encode("utf-8")
    as_int = struct.pack("<i", n)
    print(n, as_text.hex(" "), len(as_text), as_int.hex(" "), len(as_int))
try:
    as_int.decode("utf-8")
except UnicodeDecodeError:
    print("cant be read as text")
```

```output
101 31 30 31 3 65 00 00 00 4
100000 31 30 30 30 30 30 6 a0 86 01 00 4
cant be read as text
```

each row is the number, its text bytes and count, then its 4 byte integer and count. the text grows with every digit, the integer stays at 4. i assumed binary always meant smaller, but for 101 text wins.

the last line is the catch. a0 on its own isnt valid UTF-8, so a text editor opening this file shows junk or gives up. and nothing in a file says which kind it is. 65 00 00 00, the integer for 101, happens to decode as an e followed by three invisible empty characters, so a tool can only guess.

this bites with tools like Parquet, a file format analytics tools read. it is binary, and starts with the 4 bytes PAR1. open it in a text editor and you see mostly junk, not neat rows. a csv you can read with your eyes.

line endings are next, the invisible characters that quietly break text files.

---
prev: [040 folders and paths](./040-folders-and-paths.md) | next: [042 line endings](./042-line-endings.md)
