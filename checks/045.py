# checks for notes/045-torn-writes.md
rows = ["101,delivered", "102,delivered", "103,delivered", "104,cancelled",
        "105,delivered", "106,pending", "107,delivered"]
old = ("\n".join(rows) + "\n").encode()
rows[5] = "106,delivered"
new = ("\n".join(rows) + "\n").encode()
B = 16
assert (len(old), len(new)) == (96, 98)
assert -(-len(old) // B) == 6 and -(-len(new) // B) == 7
blk = lambda b, i: b[i * B:(i + 1) * B]
# blocks 0 to 3 identical
assert all(blk(old, i) == blk(new, i) for i in range(4))
assert blk(old, 4) != blk(new, 4)
disk = new[:5 * B] + old[5 * B:]
exp = {4: (b"vered\n106,pendin", b"vered\n106,delive", b"vered\n106,delive"),
       5: (b"g\n107,delivered\n", b"red\n107,delivere", b"g\n107,delivered\n"),
       6: (b"", b"d\n", b"")}
for i, (o, n, d) in exp.items():
    assert (blk(old, i), blk(new, i), blk(disk, i)) == (o, n, d)
assert len(disk) == 96
assert disk.split(b"\n")[5] == b"106,deliveg"
# q1: tear after block 3 leaves old file; block 3 is the same in both
assert blk(old, 3) == blk(new, 3) == b"ncelled\n105,deli"
assert new[:4 * B] + old[4 * B:] == old
# q2: block 5 lands, block 4 does not
d2 = old[:5 * B] + new[5 * B:6 * B]
assert d2.decode().split("\n")[5:] == ["106,pendinred", "107,delivere"]
assert not d2.endswith(b"\n")
# source: https://www.sqlite.org/atomiccommit.html
#   confirmed: power failure mid write can leave part modified and part unchanged; in rollback mode (not WAL) SQLite writes the original content of pages to a rollback journal before changing the database file
# source: https://www.sqlite.org/onefile.html
#   confirmed: "A database in SQLite is a single disk file"
print("045 ok")
