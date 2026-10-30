# 276: why sorting costs more than one pass over the data
builds on: [275 merge sort, split down to single items, then merge back up](./275-merge-sort-split-down-to-single-items-then-merge-back-up.md), [274 merging two sorted lists into one](./274-merging-two-sorted-lists-into-one.md), [273 binary search, finding one item in sorted data by halving](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md), [271 curving up, when 10 times the data means 100 times the steps](./271-curving-up-when-10-times-the-data-means-100-times-the-steps.md), [270 flat and straight line, the two shapes of growth](./270-flat-and-straight-line-the-two-shapes-of-growth.md), [117 ORDER BY, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md)
section: tricks that make data fast, part 8, ~2 min read

a merge ([274](./274-merging-two-sorted-lists-into-one.md), combining two sorted lists into one) is one pass, meaning each item looked at once. so is sorting just one pass? no.

merge sort ([275](./275-merge-sort-split-down-to-single-items-then-merge-back-up.md)) merges pairs of lists in a round, then again, until one list is left. cost is a pass per round, and the rounds are how many times you can halve the list ([273](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md)) down to single items, rounded up.

the shop, the imaginary gujarati snack store these notes run on, has 6 products, each starting as a list of one. a placement is a price copied into a merged list.

| round | lists before | lists after | prices placed |
| --- | --- | --- | --- |
| 1 | 6 | 3 | 6 |
| 2 | 3 | 2 | 4 |
| 3 | 2 | 1 | 6 |

16 placements in total, against 6 for one pass. round 2 placed 4 because the last list had no partner and waited. so at most 3 x 6 = 18.

now pretend the shop has more orders to sort, 10 times each row. the last column is every one against every one ([271](./271-curving-up-when-10-times-the-data-means-100-times-the-steps.md)), the ceiling for a sort made of a loop inside a loop.

| orders | one pass | sorting, at most | every one against every one |
| --- | --- | --- | --- |
| 7 | 7 | 3 x 7 = 21 | 49 |
| 70 | 70 | 7 x 70 = 490 | 4900 |
| 700 | 700 | 10 x 700 = 7000 | 490000 |
| 7000 | 7000 | 13 x 7000 = 91000 | 49000000 |

from 700 to 7000, 10 times the orders cost sorting at most 13 times the steps, worse than the straight line ([270](./270-flat-and-straight-line-the-two-shapes-of-growth.md)) but nowhere near 100 times.

i assumed sorting was either cheap or expensive, but it sits in between. doubling the orders adds just one round.

Postgres, a popular database server, says an index (a lookup shortcut) can hand rows back already in order, so the sort for an ORDER BY ([117](./117-order-by-sorting-by-one-or-more-columns.md), SQL sorting) is skipped ([docs](https://www.postgresql.org/docs/current/indexes-ordering.html)). only some kinds of index can.

---
prev: [275 merge sort, split down to single items, then merge back up](./275-merge-sort-split-down-to-single-items-then-merge-back-up.md) | next: [277 hash functions, turning anything into a number in a fixed range](./277-hash-functions-turning-anything-into-a-number-in-a-fixed-range.md)
