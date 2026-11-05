# checks for notes/326-running-a-python-script-from-the-terminal.md
import os, sys, subprocess, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
price = dict(con.execute("SELECT name, price FROM products").fetchall())
assert float(price["dhokla"]) == 6.0 and float(price["masala chai"]) == 3.0
assert 6.00 * 2 == 12.0 and 3.00 * 2 == 6.0
src = ('import sys\nPRICES = {"dhokla": 6.00, "masala chai": 3.00}\nprint(sys.argv)\n'
       'print(PRICES[sys.argv[1]] * int(sys.argv[2]))\n')
with tempfile.TemporaryDirectory() as d:
    open(os.path.join(d, "total.py"), "w").write(src)
    def run(*args):
        return subprocess.run([sys.executable, "total.py", *args], cwd=d, capture_output=True, text=True)
    assert run("dhokla", "2").stdout == "['total.py', 'dhokla', '2']\n12.0\n"
    assert run("masala chai", "2").stdout == "['total.py', 'masala chai', '2']\n6.0\n"
    open(os.path.join(d, "total.py"), "w").write(src.replace("int(sys.argv[2])", "sys.argv[2]"))
    r = run("dhokla", "2")
    assert r.returncode != 0 and "TypeError" in r.stderr, r.stderr
# source: https://docs.python.org/3/library/sys.html
#   confirmed (opened this run): sys.argv is the list of command line arguments passed to a Python script, argv[0] is the script name
# source: https://en.wikipedia.org/wiki/Cron
#   confirmed (opened this run): cron is a time-based job scheduler
# source: https://docs.python.org/3/library/argparse.html
#   confirmed (opened this run): argparse is the standard library module for command line interfaces, parsing sys.argv, with a type option on add_argument
# audit: python3 is the linux and mac command, so the note now says on windows the word is usually py
# source: https://docs.python.org/3/using/windows.html
#   confirmed (opened this run): the python3 command on Windows "is intended to catch accidental uses of the typical POSIX command on Windows, but is not meant to be widely used or recommended"
# source: https://pip.pypa.io/en/stable/cli/pip/
#   confirmed (opened this run): usage is "Unix/macOS python -m pip <command>" and "Windows py -m pip <command>"
