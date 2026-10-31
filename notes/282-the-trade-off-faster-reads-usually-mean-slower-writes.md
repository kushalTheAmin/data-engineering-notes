# 282: the trade off, faster reads usually mean slower writes
builds on: [281 balanced trees, why the depth stays small](./281-balanced-trees-why-the-depth-stays-small.md), [273 binary search, finding one item in sorted data by halving](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md), [269 big O in plain words, how work grows as data grows](./269-big-o-in-plain-words-how-work-grows-as-data-grows.md), [220 INSERT, adding rows and matching values to columns](./220-insert-adding-rows-and-matching-values-to-columns.md)
section: tricks that make data fast, part 14, ~2 min read

if a sorted list or a balanced tree makes finding things so fast, why not keep every table sorted, always? the bill shows up when new orders arrive.

the trade off: anything that makes reads (lookups) fast has to be kept in shape as writes arrive, a write being a change like an [INSERT](./220-insert-adding-rows-and-matching-values-to-columns.md), adding a row. reads get cheaper, writes cost more.

the shop, the imaginary gujarati snack store these notes run on, gets orders. i keep the same ids two ways: a loose list where a new id goes on the end, and a tidy list kept sorted, so [halving](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md) works. a look is checking one id, a write step is placing or moving one id. orders arrive mixed up, and i search for the last one in.

```python
def run(ids, want):
    loose, tidy = [], []
    w_loose = w_tidy = 0
    for v in ids:
        loose.append(v)
        w_loose += 1
        pos = 0
        while pos < len(tidy) and tidy[pos] < v:
            pos += 1
        w_tidy += 1 + (len(tidy) - pos)
        tidy.insert(pos, v)
    r_loose = loose.index(want) + 1
    lo, hi, r_tidy = 0, len(tidy) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        r_tidy += 1
        if tidy[mid] == want:
            break
        if tidy[mid] < want:
            lo = mid + 1
        else:
            hi = mid - 1
    return w_loose, w_tidy, r_loose, r_tidy

for n, ids in [(7, [104, 102, 106, 101, 103, 105, 107]),
               (700, [101 + (i * 37) % 700 for i in range(700)])]:
    wl, wt, rl, rt = run(ids, ids[-1])
    print(n, "orders: loose", wl, "writes,", rl, "looks | tidy", wt, "writes,", rt, "looks")
```

```output
7 orders: loose 7 writes, 7 looks | tidy 14 writes, 3 looks
700 orders: loose 700 writes, 700 looks | tidy 118348 writes, 10 looks
```

the tidy list wins the search, 3 looks against 7, and 10 against 700, the [growth](./269-big-o-in-plain-words-how-work-grows-as-data-grows.md) again. but each id that lands near the front shoves the rest over, so 700 arrivals cost 118348 write steps against 700. ids arriving in order dodge this, see question 1.

a [balanced tree](./281-balanced-trees-why-the-depth-stays-small.md) pays far less than shifting a list, but it still pays.

in Postgres, once an index exists (a lookup shortcut to rows, a later note builds it), the docs say keeping it synchronized with the table slows writes ([docs](https://www.postgresql.org/docs/current/indexes-intro.html)).

i assumed keeping data sorted was a free upgrade, but the cost lands on the insert, not the read. would you pay it on a write heavy table?

### check yourself

1. the shop orders 101 to 107 arrive in id order into the tidy list. how many write steps in total?

<details><summary>answer</summary>

seven, one per order. every new id is the biggest so far and lands on the end, so nothing moves. the tempting answer is 14, copied from the mixed up arrival, but the cost depends on where each new id lands, and here it is always the end.

</details>

2. the shop saves every page view, thousands a day, in a list kept sorted by visitor name, and someone looks up one visitor a week. loose or tidy, and why?

<details><summary>answer</summary>

loose. visitor names arrive in no order, so the tidy list shoves items over on most writes and saves looks only on the rare search. the tempting answer is tidy because fast lookups sound better, but the writes add up far more often.

</details>

---
prev: [281 balanced trees, why the depth stays small](./281-balanced-trees-why-the-depth-stays-small.md) | next: not written yet
