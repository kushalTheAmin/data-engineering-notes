# checks for notes/046-writing-safely.md
import os, tempfile
rows = ["101,delivered", "102,delivered", "103,delivered", "104,cancelled",
        "105,delivered", "106,pending", "107,delivered"]
old = ("\n".join(rows) + "\n").encode()
rows[5] = "106,delivered"
new = ("\n".join(rows) + "\n").encode()
assert (len(old), len(new)) == (96, 98)
# 32 of 98 bytes is two whole 16 byte blocks, a partial copy, 5 blocks of 16 is 80 bytes
assert 32 < len(new) and 5 * 16 == 80 < len(new)
assert old.split(b"\n")[5] == b"106,pending"
# the python block: replace leaves one file with the new text
d = tempfile.mkdtemp()
p = os.path.join(d, "orders.csv")
open(p, "w").write("106,pending\n")
t = p + ".tmp"
with open(t, "w") as f:
    f.write("106,delivered\n"); f.flush(); os.fsync(f.fileno())
os.replace(t, p)
assert open(p).read() == "106,delivered\n" and os.listdir(d) == ["orders.csv"]
# q1: delete then rename leaves a gap with no orders.csv
os.remove(p)
assert not os.path.exists(p)
# source: https://man7.org/linux/man-pages/man2/rename.2.html
#   confirmed: existing newpath is atomically replaced, no point at which another process finds newpath missing; EXDEV when not on the same mounted filesystem
# source: https://docs.python.org/3/library/os.html
#   confirmed: os.replace renames src to dst, atomic if successful (POSIX requirement), may fail across filesystems; os.fsync forces write of the file to disk after f.flush()
# source: https://docs.python.org/3/library/shutil.html
#   confirmed: shutil.move uses os.rename on the same filesystem, otherwise copies then removes the source
# source: https://man7.org/linux/man-pages/man2/fsync.2.html
#   confirmed: fsync() does not necessarily ensure that the entry in the directory containing the file has also reached disk; for that an explicit fsync() on a file descriptor for the directory is also needed
print("046 ok")
