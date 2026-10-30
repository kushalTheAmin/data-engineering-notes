# 275: merge sort, split down to single items, then merge back up
builds on: [274 merging two sorted lists into one](./274-merging-two-sorted-lists-into-one.md), [273 binary search, finding one item in sorted data by halving](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md), [270 flat and straight line, the two shapes of growth](./270-flat-and-straight-line-the-two-shapes-of-growth.md), [117 ORDER BY, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md)
section: tricks that make data fast, part 7, ~2 min read

the merge in [274](./274-merging-two-sorted-lists-into-one.md) needs two lists that are already sorted. so where does the first sorted list come from?

a list with one item in it is already sorted, nothing to be out of order with. merge sort treats every item as its own list of one, merges neighbours in pairs (a merge takes the smaller front each time), then merges the results, until one list is left. it is one way to do the sorting a SQL [ORDER BY](./117-order-by-sorting-by-one-or-more-columns.md) asks for.

the shop, the imaginary gujarati snack store these notes run on, has 6 products. their prices in id order: dhokla 6.00, khandvi 7.50, jalebi 5.00, kaju katli 12.00, masala chai 3.00, fafda 4.50.

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

lists = [[6.0], [7.5], [5.0], [12.0], [3.0], [4.5]]
print(lists)
while len(lists) > 1:
    merged = [merge(lists[k], lists[k + 1]) for k in range(0, len(lists) - 1, 2)]
    if len(lists) % 2 == 1:
        merged.append(lists[-1])
    lists = merged
    print(lists)
```

```output
[[6.0], [7.5], [5.0], [12.0], [3.0], [4.5]]
[[6.0, 7.5], [5.0, 12.0], [3.0, 4.5]]
[[5.0, 6.0, 7.5, 12.0], [3.0, 4.5]]
[[3.0, 4.5, 5.0, 6.0, 7.5, 12.0]]
```

round 1 merges three pairs, round 2 the first two, and the last one had no partner so it just waited. every round touches each price at most once, so a round is a straight line ([270](./270-flat-and-straight-line-the-two-shapes-of-growth.md), steps grow in step with the data). the rounds are how many times you can halve 6 down to ones, rounding up, a cousin of [273](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md) but nothing gets thrown away.

i expected sorting to need a brand new trick, but it is the same merge run again and again, starting from lists too small to be wrong.

Python sorts with [Timsort](https://en.wikipedia.org/wiki/Timsort), derived from merge sort, though it starts from runs already in order. the total steps are the next note.

### check yourself

1. the shop grows from 6 products to 12. how many rounds of merging now, if it pairs up the lists the same way?

<details><summary>answer</summary>

4 rounds. 12 lists become 6, then 3, then 2, then 1. doubling the items adds one round, 6 needed 3. the tempting answer is 6, from thinking twice the items means twice the rounds.

</details>

2. someone skips the splitting and merges the two halves of the prices once. what prints?

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

print(merge([6.0, 7.5, 5.0], [12.0, 3.0, 4.5]))
```

<details><summary>answer</summary>

```output
[6.0, 7.5, 5.0, 12.0, 3.0, 4.5]
```

neither half is sorted, so the merge trusts them and nothing moves: 6.0, 7.5 and 5.0 all beat 12.0, then the right side is just tacked on. the tempting answer is a sorted list. only lists of one are sorted for free.

</details>

---
prev: [274 merging two sorted lists into one](./274-merging-two-sorted-lists-into-one.md) | next: [276 why sorting costs more than one pass over the data](./276-why-sorting-costs-more-than-one-pass-over-the-data.md)
