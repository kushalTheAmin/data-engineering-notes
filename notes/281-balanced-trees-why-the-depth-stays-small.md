# 281: balanced trees, why the depth stays small
builds on: [280 trees, data that branches](./280-trees-data-that-branches.md), [273 binary search, finding one item in sorted data by halving](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md), [269 big O in plain words, how work grows as data grows](./269-big-o-in-plain-words-how-work-grows-as-data-grows.md)
section: tricks that make data fast, part 13, ~2 min read

in [280](./280-trees-data-that-branches.md) the order ids 101 to 107 made a tree where finding 107 took 3 looks, a look being one node checked. but real orders arrive as 101, 102, 103, in order. would you expect the tree to stay small?

a balanced tree keeps its depth, the number of levels from the root down, as small as its size allows. a plain tree makes no promise: each new id hangs off the first free spot, so the shape comes from the arrival order.

the shop, the imaginary gujarati snack store these notes run on, has orders 101 to 107. same ids, two arrival orders. a node here is a list: the id, its smaller side, its bigger side.

```python
def add(root, v):
    if root is None:
        return [v, None, None]
    node = root
    while True:
        side = 1 if v < node[0] else 2
        if node[side] is None:
            node[side] = [v, None, None]
            return root
        node = node[side]

def looks(root, v):
    n = 0
    while root is not None:
        n += 1
        if v == root[0]:
            return n
        root = root[1] if v < root[0] else root[2]
    return n

def build(ids):
    root = None
    for v in ids:
        root = add(root, v)
    return root

print("101 to 107 in order:", looks(build([101, 102, 103, 104, 105, 106, 107]), 107))
print("104 102 106 101 103 105 107:", looks(build([104, 102, 106, 101, 103, 105, 107]), 107))
print("700 orders in order:", looks(build(range(101, 801)), 800))
```

```output
101 to 107 in order: 7
104 102 106 101 103 105 107: 3
700 orders in order: 700
```

arriving in order, every new id is bigger than all before it, so it always goes right. the tree is one long chain, which is just the walk from [269](./269-big-o-in-plain-words-how-work-grows-as-data-grows.md) wearing a tree costume.

a balanced tree fixes this while ids arrive. when one side gets too deep, it moves a middle node up:

```text
101                 102
  102      -->     /   \
    103          101   103
```

now 700 orders need at most 10 looks, the same as the halving in [273](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md).

Postgres docs call its btree index a multi-way balanced tree ([docs](https://www.postgresql.org/docs/current/btree.html)), so the repair is built in.

i figured the tree itself was the fast part, but the speed is how even it is.

### check yourself

1. ids 105, 106, 107 go into an empty plain tree. how many looks to find 107 if they arrive in that order, and if they arrive as 106, 105, 107?

<details><summary>answer</summary>

3 looks, then 2. arriving 105, 106, 107 makes a chain, 106 first puts 105 on one side and 107 on the other. the tempting answer is the same for both, because the ids are the same.

</details>

2. 700 orders arrive in id order. how many looks for the last one in a plain tree, and at most in a balanced one?

<details><summary>answer</summary>

700 looks in the plain tree, at most 10 in a balanced one. the plain tree is a chain here. the tempting answer is 10 for both, because both are called trees.

</details>

---
prev: [280 trees, data that branches](./280-trees-data-that-branches.md) | next: not written yet
