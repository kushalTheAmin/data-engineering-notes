# 291: the leftmost prefix rule, which questions a composite index can answer
builds on: [290 composite indexes, sorted by the first column, then the second](./290-composite-indexes-sorted-by-the-first-column-then-the-second.md), [286 index, a sorted shortcut to rows](./286-index-a-sorted-shortcut-to-rows.md)
section: inside a database server, part 8, ~2 min read

i assumed an index on (customer_id, ordered_at) would speed up any question about either column. does a search on ordered_at alone get the same jump?

the leftmost prefix rule says a [composite index](./290-composite-indexes-sorted-by-the-first-column-then-the-second.md), one [index](./286-index-a-sorted-shortcut-to-rows.md) sorted on two columns, only jumps (finds the first match, then reads on) for a question that starts at its first column. an exact match on the first column, alone or followed by a condition on the second, hits one unbroken run of entries. a condition on a later column alone usually doesnt.

here is the index for the shop, the imaginary gujarati snack store these notes run on, entries numbered from 0, each one (customer_id, ordered_at, order_id):

```python
index = [
    (1, "2026-04-01 09:15:00", 101), (1, "2026-04-03 12:05:00", 103),
    (1, "2026-04-08 10:00:00", 106), (2, "2026-04-01 18:40:00", 102),
    (2, "2026-04-09 13:45:00", 107), (3, "2026-04-04 08:30:00", 104),
    (4, "2026-04-06 19:10:00", 105),
]

def hits(test):
    return [i for i, e in enumerate(index) if test(e)]

print("customer_id = 1:", hits(lambda e: e[0] == 1))
print("customer_id = 1 and ordered_at from 04-03:", hits(lambda e: e[0] == 1 and e[1] >= "2026-04-03"))
print("ordered_at from 04-06 alone:", hits(lambda e: e[1] >= "2026-04-06"))
```

```output
customer_id = 1: [0, 1, 2]
customer_id = 1 and ordered_at from 04-03: [1, 2]
ordered_at from 04-06 alone: [2, 4, 6]
```

the first two are one run, so the index finds the start and reads until the run ends. the third is scattered, entries 2, 4 and 6 with others between, so there is no start to jump to. i expected the second column to be a second way in, but its only a tiebreaker, and a tiebreaker means nothing until you know the first value.

Postgres, a database server, can still read the whole index for the third question, but its docs say it would usually rather scan the table. version 18 added a skip scan, which helps when the first column has few different values.

so the order you pick decides which questions get the shortcut.

### check yourself

1. imagine an index on order_items (product_id, order_id), a made up one for this question. a query asks WHERE order_id = 105. how many of its 13 entries does it have to look at, and why not 3?

```sql
SELECT product_id, order_id FROM order_items ORDER BY product_id, order_id;
```

<details><summary>answer</summary>

```result
product_id | order_id
1 | 101
1 | 104
1 | 107
2 | 103
2 | 106
3 | 102
3 | 105
3 | 107
4 | 102
4 | 105
5 | 101
5 | 103
5 | 105
```

all 13. order 105 sits under products 3, 4 and 5 with other orders between, and the index is sorted by product first. the tempting answer is 3, from counting the matches instead of the entries it must pass.

</details>

2. flip it: an index on (order_id, product_id), and the query is WHERE order_id = 105 AND product_id >= 4. how many entries does the run cover?

```sql
SELECT order_id, product_id FROM order_items WHERE order_id = 105 AND product_id >= 4 ORDER BY product_id;
```

<details><summary>answer</summary>

```result
order_id | product_id
105 | 4
105 | 5
```

two. order is the first column, so the index jumps to order 105 and product 4, then reads to the last 105. the tempting answer is 3, which counts the entry for product 3 that the second condition already rules out.

</details>

---
prev: [290 composite indexes, sorted by the first column, then the second](./290-composite-indexes-sorted-by-the-first-column-then-the-second.md) | next: [292 covering index, when the index alone has the answer](./292-covering-index-when-the-index-alone-has-the-answer.md)
