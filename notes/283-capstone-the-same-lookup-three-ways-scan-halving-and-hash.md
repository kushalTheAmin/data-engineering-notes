# 283: capstone, the same lookup three ways, scan, halving and hash
builds on: [269 big O in plain words, how work grows as data grows](./269-big-o-in-plain-words-how-work-grows-as-data-grows.md), [270 flat and straight line, the two shapes of growth](./270-flat-and-straight-line-the-two-shapes-of-growth.md), [271 curving up, when 10 times the data means 100 times the steps](./271-curving-up-when-10-times-the-data-means-100-times-the-steps.md), [272 a loop inside a loop, the steps are one list times the other](./272-a-loop-inside-a-loop-the-steps-are-one-list-times-the-other.md), [273 binary search, finding one item in sorted data by halving](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md), [274 merging two sorted lists into one](./274-merging-two-sorted-lists-into-one.md), [275 merge sort, split down to single items, then merge back up](./275-merge-sort-split-down-to-single-items-then-merge-back-up.md), [276 why sorting costs more than one pass over the data](./276-why-sorting-costs-more-than-one-pass-over-the-data.md), [277 hash functions, turning anything into a number in a fixed range](./277-hash-functions-turning-anything-into-a-number-in-a-fixed-range.md), [278 hash tables, how a dictionary finds a key without searching](./278-hash-tables-how-a-dictionary-finds-a-key-without-searching.md), [279 collisions, when two keys land in the same spot](./279-collisions-when-two-keys-land-in-the-same-spot.md), [280 trees, data that branches](./280-trees-data-that-branches.md), [281 balanced trees, why the depth stays small](./281-balanced-trees-why-the-depth-stays-small.md), [282 the trade off, faster reads usually mean slower writes](./282-the-trade-off-faster-reads-usually-mean-slower-writes.md)
section: tricks that make data fast, wrap up, ~3 min read

finding one order id among 7000 can take 7000 looks, 13 looks or 1, depending on the method. [282](./282-the-trade-off-faster-reads-usually-mean-slower-writes.md) ended on a bill, faster lookups get paid for when rows are added, so which fast read is worth buying?

a look is checking one id, and i count the worst case, the unluckiest id. the shop, the imaginary gujarati snack store these notes run on, has 7 orders, ids 101 to 107, so the longer lists are pretend. scan walks the ids one by one ([269](./269-big-o-in-plain-words-how-work-grows-as-data-grows.md), counting steps as data grows). halving ([273](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md), dropping half the sorted ids per look) needs order. hash ([278](./278-hash-tables-how-a-dictionary-finds-a-key-without-searching.md), id divided by the slot count, the remainder picks a numbered slot) needs neither.

```python
def scan(ids, w):
    n = 0
    for i in ids:
        n += 1
        if i == w:
            return n
    return n

def halve(ids, w):
    lo, hi, n = 0, len(ids) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        n += 1
        if ids[mid] == w:
            return n
        if ids[mid] < w:
            lo = mid + 1
        else:
            hi = mid - 1
    return n

def hash_find(slots, w):
    n = 0
    for i in slots[w % len(slots)]:
        n += 1
        if i == w:
            return n
    return n

for n in [7, 70, 700, 7000]:
    ids = list(range(101, 101 + n))
    slots = [[] for _ in range(n)]
    for i in ids:
        slots[i % n].append(i)
    print(n, "orders | scan", max(scan(ids, w) for w in ids),
          "| halving", max(halve(ids, w) for w in ids),
          "| hash", max(hash_find(slots, w) for w in ids))
```

```output
7 orders | scan 7 | halving 3 | hash 1
70 orders | scan 70 | halving 7 | hash 1
700 orders | scan 700 | halving 10 | hash 1
7000 orders | scan 7000 | halving 13 | hash 1
```

do the scan once per order and it becomes the curving up of [271](./271-curving-up-when-10-times-the-data-means-100-times-the-steps.md) and [272](./272-a-loop-inside-a-loop-the-steps-are-one-list-times-the-other.md). scan is the straight line of [270](./270-flat-and-straight-line-the-two-shapes-of-growth.md) (steps grow as fast as the data), halving adds one look per doubling, and the hash stays flat. but each row asks the data for something and charges for it:

| way | looks at 7000 | it needs | the price | notes |
|---|---|---|---|---|
| scan | 7000 | nothing | nothing | [269](./269-big-o-in-plain-words-how-work-grows-as-data-grows.md) [270](./270-flat-and-straight-line-the-two-shapes-of-growth.md) [271](./271-curving-up-when-10-times-the-data-means-100-times-the-steps.md) [272](./272-a-loop-inside-a-loop-the-steps-are-one-list-times-the-other.md) |
| halving | 13 | ids kept sorted | sorting costs more than one pass, and writes shove ids over | [273](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md) [274](./274-merging-two-sorted-lists-into-one.md) [275](./275-merge-sort-split-down-to-single-items-then-merge-back-up.md) [276](./276-why-sorting-costs-more-than-one-pass-over-the-data.md) [282](./282-the-trade-off-faster-reads-usually-mean-slower-writes.md) |
| hash | 1 | a good spread over slots | no order, shared slots add looks | [277](./277-hash-functions-turning-anything-into-a-number-in-a-fixed-range.md) [278](./278-hash-tables-how-a-dictionary-finds-a-key-without-searching.md) [279](./279-collisions-when-two-keys-land-in-the-same-spot.md) |
| balanced tree (branching boxes) | about 13 | a tree kept even (halving drawn as boxes) | far less than shifting a list, still not free ([282](./282-the-trade-off-faster-reads-usually-mean-slower-writes.md)) | [280](./280-trees-data-that-branches.md) [281](./281-balanced-trees-why-the-depth-stays-small.md) |

that 1 is the friendly case. ids in a row spread over the slots with no sharing, while real keys sometimes land in the same slot, a collision ([279](./279-collisions-when-two-keys-land-in-the-same-spot.md)), and cost an extra look now and then. a real hash scatters neighbors on purpose, so "ids 500 to 600" has nowhere to start. sorted ids do, since halving finds where 500 would sit and you walk from there.

i assumed these three would rank best to worst, but each one wins somewhere, and what separates them is what they ask the data to be. the next section opens up Postgres, a popular database, where lookup shortcuts called indexes build on these ideas.

### check yourself

1. the shop grows from 7000 to 7 million orders, ids sorted. worst case, how many looks does scan need, and how many does halving?

<details><summary>answer</summary>

scan needs 7000000. halving needs 23, since 7 million sits between 22 and 23 doublings of 1. the tempting answer is 13000 for halving, from multiplying 13 by the 1000 times growth, but halving adds a look per doubling.

</details>

2. a page asks only "is this order id taken?" thousands of times a second, and new orders arrive all day in no particular order. halving on a kept-sorted list or a hash, and what do you give up?

<details><summary>answer</summary>

hash. a yes or no needs no order, and writes drop an id into a slot instead of shoving a sorted list over, which mixed up arrivals do on most writes. you give up ranges like "ids 500 to 600". the tempting answer is halving, because 13 looks sounds tiny, but the sorted list pays on those writes.

</details>

---
prev: [282 the trade off, faster reads usually mean slower writes](./282-the-trade-off-faster-reads-usually-mean-slower-writes.md) | next: [284 how Postgres keeps a table on disk, rows packed into pages](./284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md)
