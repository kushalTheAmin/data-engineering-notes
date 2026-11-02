# 300: merge join, walk two sorted lists side by side
builds on: [299 hash join, build a hash table then look up each row](./299-hash-join-build-a-hash-table-then-look-up-each-row.md), [298 nested loop join, for each outer row search the inner side](./298-nested-loop-join-for-each-outer-row-search-the-inner-side.md), [296 the query planner, picking the cheapest plan](./296-the-query-planner-picking-the-cheapest-plan.md), [286 index, a sorted shortcut to rows](./286-index-a-sorted-shortcut-to-rows.md), [276 why sorting costs more than one pass over the data](./276-why-sorting-costs-more-than-one-pass-over-the-data.md), [274 merging two sorted lists into one](./274-merging-two-sorted-lists-into-one.md)
section: inside a database server, part 17, ~2 min read

in [299](./299-hash-join-build-a-hash-table-then-look-up-each-row.md) a hash table let every order jump to its customer. but what if both tables already come out in customer order, do you still need the table?

no. a merge join, one way to pair rows of two tables, is the [merge](./274-merging-two-sorted-lists-into-one.md) (combine two sorted lists by comparing their fronts) used as a join. Postgres, the database server these notes use, puts both sides in order on the join column, then walks them side by side with one marker (a position in the list) each ([docs](https://www.postgresql.org/docs/16/planner-optimizer.html)).

the shop, the imaginary gujarati snack store these notes run on, with its real 5 customers and 7 orders. the orders are already sorted by customer id:

```python
customers = [(1, "Asha"), (2, "Bhavin"), (3, "Chirag"), (4, "Disha"), (5, "Esha")]
orders = [(101, 1), (103, 1), (106, 1), (102, 2), (107, 2), (104, 3), (105, 4)]

i = j = steps = 0
while i < len(customers) and j < len(orders):
    cid, name = customers[i]
    order_id, order_cid = orders[j]
    steps += 1
    if cid < order_cid:
        print("customer", cid, "is behind, move customers on")
        i += 1
    else:
        print("order", order_id, "->", name)
        j += 1

print("steps:", steps)
print("customers never reached:", [n for c, n in customers[i + 1:]])
```

```output
order 101 -> Asha
order 103 -> Asha
order 106 -> Asha
customer 1 is behind, move customers on
order 102 -> Bhavin
order 107 -> Bhavin
customer 2 is behind, move customers on
order 104 -> Chirag
customer 3 is behind, move customers on
order 105 -> Disha
steps: 10
customers never reached: ['Esha']
```

i figured a join had to look things up, but nothing is. the sorted order does the finding, and the walk stops when the orders run out, so Esha is never touched. here the markers only move forward because the toy assumes unique customer ids; with repeats Postgres steps one back to a saved spot.

the catch: the 7 orders in order_id order carry customer ids 1, 2, 1, 3, 4, 1, 2, so someone pays for the sort ([276](./276-why-sorting-costs-more-than-one-pass-over-the-data.md)). unless an [index](./286-index-a-sorted-shortcut-to-rows.md) (a sorted list of values and row addresses) on customer_id hands the rows over already in order, which the docs say is one way to get it. like a hash join it needs an equality test (match when values are equal) ([docs](https://www.postgresql.org/docs/16/xoper-optimization.html)). the [planner](./296-the-query-planner-picking-the-cheapest-plan.md) prices it like any other plan.

---
prev: [299 hash join, build a hash table then look up each row](./299-hash-join-build-a-hash-table-then-look-up-each-row.md) | next: not written yet
