# checks for notes/040-folders-and-paths.md
import os
import sys
from pathlib import PurePosixPath

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
p = PurePosixPath("/shop/exports/orders.csv")
# the walk: root, then shop, exports, orders.csv, so 3 steps
assert p.parts == ("/", "shop", "exports", "orders.csv")
assert len(p.parts) - 1 == 3
assert str(p.parent) == "/shop/exports" and str(p.parent.parent) == "/shop"
q = PurePosixPath("/shop/backup/orders.csv")
# same name, different path, so different files
assert p.name == q.name and p != q
assert not PurePosixPath("orders.csv").is_absolute() and p.is_absolute()
# source: https://docs.python.org/3/library/functions.html#open
#   confirmed: a relative path given to open() is resolved against the current working directory
# source: https://en.wikipedia.org/wiki/Root_directory
#   confirmed: on unix-like systems the root directory is the first or top-most directory in a hierarchy
# source: https://en.wikipedia.org/wiki/Path_(computing)
#   confirmed: windows paths can start with a drive letter and use backslashes, e.g. C:\user\docs\Letter.txt, unix ones use /
print("040 ok")
