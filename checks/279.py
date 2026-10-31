# checks for notes/279-collisions-when-two-keys-land-in-the-same-spot.md
def slot_of(name):
    return sum(name.encode()) % 8

names = ["dhokla", "khandvi", "jalebi", "kaju katli", "masala chai", "fafda", "ladoo"]
slots = [[] for _ in range(8)]
for n in names:
    slots[slot_of(n)].append(n)
assert slots[7] == ["jalebi", "ladoo"] and slot_of("ladoo") == 7
assert [len(s) for s in slots] == [1, 0, 1, 1, 1, 1, 0, 2]
# 9 names cannot fit 8 slots without sharing
assert 9 > 8
assert slot_of("kholda") == 3 and slot_of("thepla") == 6 and slots[6] == []
# check 2: buggy hash, 6 products in one chain, thepla compares all 6
assert len(names[:6]) == 6
# source: https://docs.python.org/3/builtins/time-complexity.html
# confirmed: dict get item is O(1) average, worst case O(n)
# source: https://github.com/python/cpython/blob/main/Objects/dictobject.c
# confirmed: comment says open addressing is preferred over chaining in CPython dicts
# 278 shows 6 names in 8 slots with no collision, so collisions are not always unavoidable
six = [[] for _ in range(8)]
for n in names[:6]:
    six[slot_of(n)].append(n)
assert max(len(s) for s in six) == 1
# check 2 simulated: every name in slot 0, a miss walks all 6
chain = list(names[:6])
assert len(chain) == 6 and "thepla" not in chain
