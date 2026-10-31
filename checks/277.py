# checks for notes/277-hash-functions-turning-anything-into-a-number-in-a-fixed-range.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()

names = [n for (n,) in con.execute("SELECT name FROM products ORDER BY product_id").fetchall()]
assert names == ["dhokla", "khandvi", "jalebi", "kaju katli", "masala chai", "fafda"]

def toy(s, slots):
    return sum(s.encode()) % slots

# trace
assert list("dhokla".encode()) == [100, 104, 111, 107, 108, 97]
assert sum("dhokla".encode()) == 627 and 627 == 78 * 8 + 3 and 627 % 8 == 3
# table
assert [sum(n.encode()) for n in names] == [627, 741, 615, 992, 1060, 498]
assert [toy(n, 8) for n in names] == [3, 5, 7, 0, 4, 2]
assert len(set(toy(n, 8) for n in names)) == 6
# same input same number
assert toy("dhokla", 8) == toy("dhokla", 8)
# anagram collides
assert sum("kholda".encode()) == 627 and toy("kholda", 8) == 3
# check 1
assert toy("dhokla", 10) == 7
assert [toy(n, 10) for n in names] == [7, 1, 5, 2, 0, 8]
assert all(toy(n, 10) != toy(n, 8) for n in names)
# check 3
assert ord(" ") == 32 and 32 == 4 * 8
assert sum("fafda ".encode()) == 530 and toy("fafda ", 8) == 2
# python salts str hashes per process, constant within a process
import subprocess
outs = {subprocess.run([sys.executable, "-c", "print(hash('dhokla'))"], capture_output=True, text=True, env={**os.environ, "PYTHONHASHSEED": "random"}).stdout for _ in range(3)}
assert len(outs) > 1
assert hash("dhokla") == hash("dhokla")
# source: https://docs.python.org/3/using/cmdline.html#envvar-PYTHONHASHSEED
# confirmed: hash randomization is on by default, str and bytes hashes are salted, constant within one process but not predictable between runs
# python does not add bytes: its hash differs from the toy sum and kholda does not collide with dhokla
assert hash("dhokla") != 627 and hash("kholda") != hash("dhokla")
# half truth: one byte per character holds only for plain english letters
assert len('fafda'.encode()) == 5 and len('é'.encode()) == 2
