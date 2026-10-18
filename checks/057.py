# checks for notes/057-standard-input-and-output.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
n = con.execute("SELECT count(*) FROM orders").fetchone()[0]
assert n + 1 == 8                                         # 7 orders plus header = the 8 wc printed in 055
assert "delivered" in "order 101 delivered" and "delivered" not in "shipped"
# source: https://man7.org/linux/man-pages/man1/grep.1.html
#   confirmed: "nonrecursive searches read standard input" when no FILE is given
# source: https://man7.org/linux/man-pages/man1/wc.1.html
#   confirmed: "With no FILE, or when FILE is -, read standard input."
# source: https://en.wikipedia.org/wiki/Standard_streams
#   confirmed: "preconnected input and output communication channels", typically connected to the text terminal the shell runs in
# source: https://docs.python.org/3/library/functions.html#print
#   confirmed: print writes to sys.stdout when file is not given
# source: https://en.wikipedia.org/wiki/Standard_streams
#   confirmed: a program starts with three connections, "standard input (stdin), standard output (stdout) and standard error (stderr)"; the note names only the two that matter here
# source: https://man7.org/linux/man-pages/man3/isatty.3.html
#   confirmed: "tests whether fd is an open file descriptor referring to a terminal", so a program can check, which is why the note says usually
# source: https://en.wikipedia.org/wiki/End-of-file
#   confirmed: unix "converts a Control-D character at the start of a line into an end-of-file indicator"; on windows ctrl+z is the usual marker, so the note says linux and mac
print("057 ok")
