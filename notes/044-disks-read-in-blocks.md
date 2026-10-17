# 044: disks read in blocks, never single bytes
builds on: [004 bytes, 8 bits and 256 possible values](./004-bytes.md), [033 kilobytes to terabytes, how big data gets](./033-kilobytes-to-terabytes.md), [039 a file is a named list of bytes](./039-a-file-is-a-named-list-of-bytes.md), [043 reading start to end vs jumping to a spot](./043-reading-start-to-end-vs-jumping.md)
section: memory, disks and files, part 10, ~2 min read

you ask a file for one single byte, say the one at position 70. does the disk hand you exactly one byte? [043](./043-reading-start-to-end-vs-jumping.md) showed a jump, asking for a position directly, and this is what happens underneath it.

no. a disk hands over a block, a fixed chunk of bytes ([bytes](./004-bytes.md) being groups of 8 bits), and the disk side only deals in whole blocks. on linux the default block size for most file systems, the layer organizing files on disk, is 4096 bytes. the drive itself uses sectors, chunks of 512 or 4096 bytes, so 4096 is usual, not a law.

here is a [file](./039-a-file-is-a-named-list-of-bytes.md) cut into blocks, with positions counted from 0:

```text
| block 0: bytes 0-4095 | block 1: bytes 4096-8191 | block 2: bytes 8192-12287 |
   ^ position 70                ^ position 4096
ask 1 byte at 70        -> all of block 0
ask 1 byte at 4095      -> all of block 0
ask 2 bytes at 4095     -> block 0 AND block 1
```

the block number is the position divided by 4096, dropping the remainder, which is what // does in python:

```python
BLOCK = 4096

for start, length in [(70, 1), (4095, 1), (4096, 1), (4095, 2)]:
    first = start // BLOCK
    last = (start + length - 1) // BLOCK
    got = (last - first + 1) * BLOCK
    print(f"ask {length} at {start}: blocks {first} to {last}, disk hands over {got}")
```

```output
ask 1 at 70: blocks 0 to 0, disk hands over 4096
ask 1 at 4095: blocks 0 to 0, disk hands over 4096
ask 1 at 4096: blocks 1 to 1, disk hands over 4096
ask 2 at 4095: blocks 0 to 1, disk hands over 8192
```

the shops 7 line file from 043 adds up to 96 bytes, so one block read covers every line. a million orders is the 35 MB of [033](./033-kilobytes-to-terabytes.md), 35,000,000 bytes, and a partly filled last block still counts whole, so rounding up gives 8545 blocks.

i kept picturing the disk as a list of bytes i could poke one at a time. that picture is only how a file looks from python. the smallest thing you can fetch is a block, so asking for 2 bytes that cross a block boundary costs two whole blocks.

a 1 byte file usually uses a full block on disk too.

---
prev: [043 reading start to end vs jumping to a spot](./043-reading-start-to-end-vs-jumping.md) | next: not written yet
