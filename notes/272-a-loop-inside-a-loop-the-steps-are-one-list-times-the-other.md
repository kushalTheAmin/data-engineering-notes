# 272: a loop inside a loop, the steps are one list times the other
builds on: [269 big O in plain words, how work grows as data grows](./269-big-o-in-plain-words-how-work-grows-as-data-grows.md), [270 flat and straight line, the two shapes of growth](./270-flat-and-straight-line-the-two-shapes-of-growth.md), [271 curving up, when 10 times the data means 100 times the steps](./271-curving-up-when-10-times-the-data-means-100-times-the-steps.md)
section: tricks that make data fast, part 4, ~2 min read

two loops, one inside the other. does that always mean the curving up shape, where 10 times the data is 100 times the steps ([271](./271-curving-up-when-10-times-the-data-means-100-times-the-steps.md))? it doesnt.

with no early exit, the inner loop runs all the way through for every pass of the outer one, so the steps are the outer length times the inner length. 271 had orders against orders, but the second list can be another one.

the shop, the imaginary gujarati snack store these notes run on, has orders 101 to 107 and 6 products, ids 1 to 6. longer order lists are pretend, and a step is one trip around the inner loop.

```python
def nested(outer, inner):
    steps = 0
    for a in outer:
        for b in inner:
            steps += 1
    return steps

product_ids = [1, 2, 3, 4, 5, 6]
for n in [7, 70, 700]:
    order_ids = list(range(101, 101 + n))
    print(n, "orders | against 6 products:", nested(order_ids, product_ids), "| against orders:", nested(order_ids, order_ids))
```

```output
7 orders | against 6 products: 42 | against orders: 49
70 orders | against 6 products: 420 | against orders: 4900
700 orders | against 6 products: 4200 | against orders: 490000
```

same two loops, two shapes. against 6 products the steps grow 10 times when orders do, a [straight line](./270-flat-and-straight-line-the-two-shapes-of-growth.md), because the product list stays at 6. against orders both lists grow, so it curves up.

so ask which list grows. a small list that never grows just multiplies the steps by a fixed number.

a database can run a join ([155](./155-why-joins-the-answer-lives-in-more-than-one-table.md), pairing rows of two tables) is exactly this. Postgres calls it a nested loop join, and its docs say the right table is read once for every left row. that costs left rows times right rows, unless a lookup shortcut helps.

i assumed any loop inside a loop was the slow shape, but it only curves when both lists grow.

you can dodge the inner loop on sorted data, and the next one shows how.

### check yourself

1. the shop keeps its 6 products and goes from 7 orders to 7000. a nested loop runs orders on the outside, product ids on the inside. how many steps now, and which shape?

<details><summary>answer</summary>

42000 steps, 7000 times 6. only the orders list grew, so it is a straight line. the tempting answer is curving up, from seeing two loops and stopping there.

</details>

2. a dev loops customers inside orders: 5 customers, 7 orders, 35 steps. both tables grow 100 times, to 500 customers and 700 orders. how many steps?

<details><summary>answer</summary>

350000, 700 times 500. that is 10000 times the 35 steps, since each list grew 100 times. the tempting answer is 3500, from growing the 35 by 100 once.

</details>

---
prev: [271 curving up, when 10 times the data means 100 times the steps](./271-curving-up-when-10-times-the-data-means-100-times-the-steps.md) | next: [273 binary search, finding one item in sorted data by halving](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md)
