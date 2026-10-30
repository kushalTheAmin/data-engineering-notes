# 273: binary search, finding one item in sorted data by halving
builds on: [269 big O in plain words, how work grows as data grows](./269-big-o-in-plain-words-how-work-grows-as-data-grows.md), [270 flat and straight line, the two shapes of growth](./270-flat-and-straight-line-the-two-shapes-of-growth.md), [272 a loop inside a loop, the steps are one list times the other](./272-a-loop-inside-a-loop-the-steps-are-one-list-times-the-other.md), [117 ORDER BY, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md), [003 counting in binary](./003-counting-in-binary.md)
section: tricks that make data fast, part 5, ~2 min read

walking the order ids one by one to reach the last one took 7 looks in [269](./269-big-o-in-plain-words-how-work-grows-as-data-grows.md), and 7000 looks at 7000 orders. a look is checking one id. what if you could skip most of them?

[272](./272-a-loop-inside-a-loop-the-steps-are-one-list-times-the-other.md) said sorted data lets you dodge the inner loop, the second walk through a list. this is how. binary search: on ids sorted ([117](./117-order-by-sorting-by-one-or-more-columns.md), smallest first), look at the middle one, keep the half that could hold your id, throw the other half away, repeat. binary here means two halves, not the 0 and 1 counting of [003](./003-counting-in-binary.md).

the shop, the imaginary gujarati snack store these notes run on, has orders 101 to 107, already in order. hunting for 107:

```text
wanted 107, in [101, 102, 103, 104, 105, 106, 107]
look 1: middle is 104, 107 is bigger, drop 101 to 104
        left: [105, 106, 107]
look 2: middle is 106, 107 is bigger, drop 105 and 106
        left: [107]
look 3: middle is 107, found it
```

what is left goes 7, 3, 1. grabbing the middle is one look, because a list is a row of numbered slots ([270](./270-flat-and-straight-line-the-two-shapes-of-growth.md)). the longer lists below are pretend, and the table shows the worst case, the unluckiest id.

| orders | the walk from 269 | halving, worst case |
|---|---|---|
| 7 | 7 | 3 |
| 70 | 70 | 7 |
| 700 | 700 | 10 |
| 7000 | 7000 | 13 |

doubling the orders adds one look. 7000 orders need 13, 14000 need 14. would you have guessed that?

the catch is that it trusts the order. on unsorted ids it can say missing for an id that is there, with no error. python ships this as its bisect module, which its docs say uses a bisection algorithm on a sorted list.

i assumed throwing half away was a gamble, but the sort order is what makes it safe: a middle that is too small means everything before it is too.

### check yourself

1. the shop grows from 7000 to 56000 orders, ids still in order, worst case. how many more looks does halving need, and how many more does the walk from 269 need?

<details><summary>answer</summary>

halving goes from 13 to 16 looks, 3 more. the walk goes from 7000 to 56000, 49000 more. 56000 is 7000 doubled three times, so three extra looks. the tempting answer is 8 times as many looks for halving too.

</details>

2. someone loads the ids in arrival order and halves on them. what does this print?

```python
def halve(ids, wanted):
    lo, hi = 0, len(ids) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if ids[mid] == wanted:
            return True
        if ids[mid] < wanted:
            lo = mid + 1
        else:
            hi = mid - 1
    return False

ids = [104, 101, 107, 102, 106, 103, 105]
print(halve(ids, 106), halve(sorted(ids), 106))
```

<details><summary>answer</summary>

```output
False True
```

106 is in the list, but after the first look the right part is 106, 103, 105. its middle 103 is smaller than 106, so halving drops everything before it, and that takes 106 along. sorting first fixes it. the tempting answer is True True, from thinking a search just finds what is there.

</details>

---
prev: [272 a loop inside a loop, the steps are one list times the other](./272-a-loop-inside-a-loop-the-steps-are-one-list-times-the-other.md) | next: not written yet
