# checks for notes/044-disks-read-in-blocks.md
import math

BLOCK = 4096
cases = [(70, 1), (4095, 1), (4096, 1), (4095, 2)]
expect = [(0, 0, 4096), (0, 0, 4096), (1, 1, 4096), (0, 1, 8192)]
for (start, length), (f, l, got) in zip(cases, expect):
    first = start // BLOCK
    last = (start + length - 1) // BLOCK
    assert (first, last, (last - first + 1) * BLOCK) == (f, l, got)
# block ranges in the diagram
assert (0, 4095) == (0 * BLOCK, 1 * BLOCK - 1)
assert (4096, 8191) == (1 * BLOCK, 2 * BLOCK - 1)
assert (8192, 12287) == (2 * BLOCK, 3 * BLOCK - 1)
# the 7 line shop file from 043 is 96 bytes, all inside block 0
sizes = [14, 14, 14, 14, 14, 12, 14]
assert sum(sizes) == 96 and 96 - 1 < BLOCK
# a million orders at 35 bytes each
assert 1_000_000 * 35 == 35_000_000
assert math.ceil(35_000_000 / BLOCK) == 8545 and 35_000_000 // BLOCK == 8544
# source: https://en.wikipedia.org/wiki/Block_(data_storage)
#   confirmed: blocked data is read or written a whole block at a time; on Linux the default block size for most file systems is 4096 bytes
# source: https://en.wikipedia.org/wiki/Disk_sector
#   confirmed: sectors traditionally 512 bytes on HDDs, newer HDDs and SSDs use 4096 byte sectors; files are stored in whole sectors
# source: https://en.wikipedia.org/wiki/Disk_sector
#   confirmed: partitioning schemes are generally designed so files occupy a whole number of sectors, regardless of their actual size; a cluster is the smallest logical amount of disk space that can be allocated to hold a file (so a 1 byte file usually takes a whole block; on ext4 here, a 1 byte file shows 8 blocks of 512 = 4096 bytes)
print("044 ok")
