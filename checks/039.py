# checks for notes/039-a-file-is-a-named-list-of-bytes.md
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
content = "101,delivered"
b = content.encode()
assert len(b) == 13
assert b.hex(" ") == "31 30 31 2c 64 65 6c 69 76 65 72 65 64"
assert [chr(x) for x in b] == list(content)
# position 4 is the d, 64 in hex, 100 as a number
assert content[4] == "d" and b[4] == 100 and format(b[4], "02x") == "64"
# the positions row has 13 entries, 0 to 12
assert len(range(13)) == 13
# the rename changes no bytes
d = tempfile.mkdtemp()
p = os.path.join(d, "order101.csv")
with open(p, "w") as f:
    f.write(content)
before = open(p, "rb").read()
os.rename(p, p.replace(".csv", ".jpg"))
after = open(p.replace(".csv", ".jpg"), "rb").read()
assert (len(before), before[4], before == after) == (13, 100, True)
# the shop row: order 101 is delivered
from _shop import shop
assert shop().execute("SELECT status FROM orders WHERE order_id = 101").fetchone()[0] == "delivered"
# source: https://en.wikipedia.org/wiki/Filename_extension
#   confirmed: a filename extension is a suffix to the name of a file (.txt, .mp3) that indicates a characteristic of the contents
# source: https://en.wikipedia.org/wiki/List_of_file_signatures
#   confirmed: file signatures (magic bytes) sit at the start of a file, and jpg/jpeg files start with FF D8 FF
print("039 ok")
