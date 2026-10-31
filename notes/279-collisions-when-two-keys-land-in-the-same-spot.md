# 279: collisions, when two keys land in the same spot
builds on: [278 hash tables, how a dictionary finds a key without searching](./278-hash-tables-how-a-dictionary-finds-a-key-without-searching.md), [277 hash functions, turning anything into a number in a fixed range](./277-hash-functions-turning-anything-into-a-number-in-a-fixed-range.md), [270 flat and straight line, the two shapes of growth](./270-flat-and-straight-line-the-two-shapes-of-growth.md)
section: tricks that make data fast, part 11, ~2 min read

in [278](./278-hash-tables-how-a-dictionary-finds-a-key-without-searching.md), a hash table (numbered slots, a name hashed to pick its slot), ladoo, a round sweet, wanted slot 7 where jalebi already sits, and the code just overwrote it. does a dictionary really lose a product whenever two names collide?

a collision is two different keys getting the same slot from the [hash function](./277-hash-functions-turning-anything-into-a-number-in-a-fixed-range.md). you cant prevent it, because 9 names never fit into 8 slots without sharing. the common fix is chaining: each slot holds a small list of names, not one.

the shop, the imaginary gujarati snack store these notes run on, with the same 8 slots as 278 (ladoo is a what-if, not a shop product):

```python
def slot_of(name):
    return sum(name.encode()) % 8

slots = [[] for _ in range(8)]
for name in ["dhokla", "khandvi", "jalebi", "kaju katli", "masala chai", "fafda", "ladoo"]:
    slots[slot_of(name)].append(name)

def find(name):
    compared = 0
    for n in slots[slot_of(name)]:
        compared += 1
        if n == name:
            return "found", compared
    return "not here", compared

print(slots)
for wanted in ["jalebi", "ladoo", "kholda", "thepla"]:
    print(wanted, find(wanted))
```

```output
[['kaju katli'], [], ['fafda'], ['dhokla'], ['masala chai'], ['khandvi'], [], ['jalebi', 'ladoo']]
jalebi ('found', 1)
ladoo ('found', 2)
kholda ('not here', 1)
thepla ('not here', 0)
```

nothing got lost. slot 7 now holds both, and finding ladoo means one jump, then comparing names down a chain of 2. kholda still lands on dhokla and compares once.

i assumed a collision was an error the table had to avoid, but its normal and the table is built to expect it.

so the lookup stays flat ([270](./270-flat-and-straight-line-the-two-shapes-of-growth.md), the same few steps however big the data) only while chains stay short. if every name hashed to one slot, a lookup would walk them all, which is the slow worst case the python docs list for a dictionary ([docs](https://docs.python.org/3/builtins/time-complexity.html)). python handles collisions differently (it probes for another free slot, [source](https://github.com/python/cpython/blob/main/Objects/dictobject.c)), but chaining shows the idea.

### check yourself

1. after ladoo is added, which costs more compares, finding jalebi or finding ladoo, and by how many?

<details><summary>answer</summary>

ladoo costs 1 more, 2 compares against 1. both live in slot 7, but jalebi was added first so it sits at the front of the chain. the tempting answer is a tie, because they share a slot.

</details>

2. a buggy hash always returns slot 0 for the 6 shop products. how many names does a miss like thepla compare?

<details><summary>answer</summary>

all 6, since every name sits in one chain, so a miss walks all of it, the straight line shape, not a jump. the tempting answer is 1, because the hash still jumps to one slot.

</details>

---
prev: [278 hash tables, how a dictionary finds a key without searching](./278-hash-tables-how-a-dictionary-finds-a-key-without-searching.md) | next: [280 trees, data that branches](./280-trees-data-that-branches.md)
