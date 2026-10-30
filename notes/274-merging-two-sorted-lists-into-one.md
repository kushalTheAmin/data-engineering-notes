# 274: merging two sorted lists into one
builds on: [273 binary search, finding one item in sorted data by halving](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md), [269 big O in plain words, how work grows as data grows](./269-big-o-in-plain-words-how-work-grows-as-data-grows.md), [270 flat and straight line, the two shapes of growth](./270-flat-and-straight-line-the-two-shapes-of-growth.md), [155 why joins, the answer lives in more than one table](./155-why-joins-the-answer-lives-in-more-than-one-table.md), [117 ORDER BY, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md)
section: tricks that make data fast, part 6, ~2 min read

[273](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md) only works on sorted ids, so somebody has to pay for the sort. how do you sort without comparing everything with everything? start with an easier job: you already have two sorted lists, and you want one.

that is a merge. look at the front of each list, take the smaller one, repeat. a list is a row of numbered slots, so each list just needs a marker for where its front is.

the shop, the imaginary gujarati snack store these notes run on, has 6 products. i split them into two lists, each already sorted by price ([117](./117-order-by-sorting-by-one-or-more-columns.md)): fafda 4.50, dhokla 6.00, khandvi 7.50 on one side, and masala chai 3.00, jalebi 5.00, kaju katli 12.00 on the other.

```python
left = [("fafda", 4.50), ("dhokla", 6.00), ("khandvi", 7.50)]
right = [("masala chai", 3.00), ("jalebi", 5.00), ("kaju katli", 12.00)]
out = []
i = j = 0
while i < len(left) and j < len(right):
    a, b = left[i], right[j]
    if a[1] <= b[1]:
        out.append(a)
        i += 1
    else:
        out.append(b)
        j += 1
    print(a[1], "vs", b[1], "-> take", out[-1][0])
out += left[i:] + right[j:]
print([name for name, price in out])
```

```output
4.5 vs 3.0 -> take masala chai
4.5 vs 5.0 -> take fafda
6.0 vs 5.0 -> take jalebi
6.0 vs 12.0 -> take dhokla
7.5 vs 12.0 -> take khandvi
['masala chai', 'fafda', 'jalebi', 'dhokla', 'khandvi', 'kaju katli']
```

once left ran out, kaju katli just got tacked on, nobody was left to compare it with. and the markers only ever move forward. 5 comparisons for 6 items, never going back, so the work is about one step per item, a straight line ([270](./270-flat-and-straight-line-the-two-shapes-of-growth.md)) in the sense of [269](./269-big-o-in-plain-words-how-work-grows-as-data-grows.md). i expected combining two lists to need a nested loop, but the sorted order is what lets one pass do it.

this shows up for real: Postgres has a merge join, one way to run a [join](./155-why-joins-the-answer-lives-in-more-than-one-table.md), pairing up rows of two tables. it sorts both on the shared column, then scans them side by side once ([docs](https://www.postgresql.org/docs/current/planner-optimizer.html)).

### check yourself

1. merge the sorted lists fafda 4.50, dhokla 6.00 and khandvi 7.50, kaju katli 12.00 with the code above. how many comparisons happen?

<details><summary>answer</summary>

two comparisons. 4.50 vs 7.50 takes fafda, 6.00 vs 7.50 takes dhokla, then the left list is empty and the other two are tacked on. the tempting answer is 3, from 4 items minus 1, but that is the worst case, the unluckiest input.

</details>

2. someone merges two lists where the first is not sorted. what prints?

```python
def merge(left, right):
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    return out + left[i:] + right[j:]

print(merge([6.0, 4.5], [3.0, 5.0]))
```

<details><summary>answer</summary>

```output
[3.0, 5.0, 6.0, 4.5]
```

6.0 vs 3.0 takes 3.0, 6.0 vs 5.0 takes 5.0, then the right list is empty so 6.0 and 4.5 are tacked on in their old order. a merge trusts both lists, like halving trusted its ids. the tempting answer is a sorted list, from assuming merging also fixes order.

</details>

---
prev: [273 binary search, finding one item in sorted data by halving](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md) | next: [275 merge sort, split down to single items, then merge back up](./275-merge-sort-split-down-to-single-items-then-merge-back-up.md)
