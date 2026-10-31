# checks for notes/278-hash-tables-how-a-dictionary-finds-a-key-without-searching.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()

rows = con.execute("SELECT name, price FROM products ORDER BY product_id").fetchall()
assert [(n, float(p)) for n, p in rows] == [("dhokla", 6.0), ("khandvi", 7.5), ("jalebi", 5.0), ("kaju katli", 12.0), ("masala chai", 3.0), ("fafda", 4.5)]

def slot_of(name):
    return sum(name.encode()) % 8

slots = [None] * 8
for n, p in rows:
    assert slots[slot_of(n)] is None
    slots[slot_of(n)] = n
assert slots == ["kaju katli", None, "fafda", "dhokla", "masala chai", "khandvi", None, "jalebi"]
assert slot_of("jalebi") == 7 and slot_of("thepla") == 6 and slots[6] is None
assert slot_of("kholda") == 3 and slots[3] == "dhokla"
# check 1
assert sum("ladoo".encode()) == 527 and 527 % 8 == 7 and slots[7] == "jalebi"
assert slots.count(None) == 2
# check 2
assert sum("barfi".encode()) == 516 and 516 % 8 == 4 and slots[4] == "masala chai"
# source: https://docs.python.org/3/builtins/time-complexity.html
# confirmed: dict get item is O(1) as an average-case time, assuming collisions are uncommon; worst case O(n) when every key hashes the same
# python dicts can collide, so a miss is about one look, not always exactly one (O(1) is the average case, source above)
assert slot_of('kholda') == slot_of('dhokla')
