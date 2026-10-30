# 271: curving up, when 10 times the data means 100 times the steps
builds on: [269 big O in plain words, how work grows as data grows](./269-big-o-in-plain-words-how-work-grows-as-data-grows.md), [270 flat and straight line, the two shapes of growth](./270-flat-and-straight-line-the-two-shapes-of-growth.md)
section: tricks that make data fast, part 3, ~2 min read

the shop wants to know if any order id shows up twice, so a dev compares every order with every order. 7 orders is 49 looks. what does 700 cost?

[270](./270-flat-and-straight-line-the-two-shapes-of-growth.md) had flat and the straight line. the third shape curves up: 10 times the data, 100 times the steps.

the shop, the imaginary gujarati snack store these notes run on, has orders 101 to 107, and the longer lists are pretend. a step is now one comparison of two ids.

```python
def look_at_every_pair(order_ids):
    steps = 0
    for i, a in enumerate(order_ids):
        for j, b in enumerate(order_ids):
            steps += 1
            if i != j and a == b:
                return steps
    return steps

for n in [7, 70, 700]:
    order_ids = list(range(101, 101 + n))
    print(n, "orders | straight line:", n, "| curving up:", look_at_every_pair(order_ids))
```

```output
7 orders | straight line: 7 | curving up: 49
70 orders | straight line: 70 | curving up: 4900
700 orders | straight line: 700 | curving up: 490000
```

read the last column. 7 to 70 is 10 times the orders, 49 to 4900 is 100 times the steps. 70 to 700 does it again. at 700 orders a straight line is 700 looks and this is 490000.

every id meets every id, so n orders cost n times n. skipping repeat pairs halves it, still about 100 times.

the gotcha is that you never have to write the second loop. if oid in seen, with seen a list of ids so far, inside a for loop is the same shape, because in walks the list one id at a time, the hidden loop from 270.

it can show up in joins ([155](./155-why-joins-the-answer-lives-in-more-than-one-table.md), matching rows of two tables). Postgres, a popular database, says in its docs that a nested loop join scans the right table once per left row, which can be very slow.

i assumed slow code was just more of the same, but 49 looks turning into 490000 feels like a different program.

### check yourself

1. at 70 orders the pair check takes 4900 looks. the shop grows 100 times, to 7000 orders. how many looks now?

<details><summary>answer</summary>

it is 49000000, 7000 times 7000. data grew 100 times, so steps grew 100 times 100, which is 10000 times. the tempting answer is 490000, from letting the steps grow only as fast as the data, which is the straight line.

</details>

2. a dev builds seen = [] and loops over 7000 different order ids, checking if oid in seen before each seen.append(oid). straight line or curving up, and roughly how many looks?

<details><summary>answer</summary>

curving up, about 24.5 million looks. the first id checks an empty list, the last checks 6999 ids, and the checks add up to 0 + 1 + 2 and so on up to 6999, which is 24496500. the tempting answer is straight line, because only one loop is written.

</details>

---
prev: [270 flat and straight line, the two shapes of growth](./270-flat-and-straight-line-the-two-shapes-of-growth.md) | next: not written yet
