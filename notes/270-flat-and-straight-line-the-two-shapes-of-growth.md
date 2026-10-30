# 270: flat and straight line, the two shapes of growth
builds on: [269 big O in plain words, how work grows as data grows](./269-big-o-in-plain-words-how-work-grows-as-data-grows.md), [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md)
section: tricks that make data fast, part 2, ~2 min read

the shop wants a page showing its newest order, and there are two ways to write it. at 7 orders you cant tell them apart, at 7000 you can.

[269](./269-big-o-in-plain-words-how-work-grows-as-data-grows.md) counted steps, one per id looked at. when the data gets 10 times bigger, the steps either stay the same (flat) or grow 10 times too (straight line).

the shop, the imaginary gujarati snack store these notes run on, has orders 101 to 107. a table is a list of rows ([079](./079-a-table-rows-are-records-columns-are-fields.md)), so the longer lists are pretend. the newest id is the last one.

```python
def find(order_ids, wanted):
    steps = 0
    for oid in order_ids:
        steps += 1
        if oid == wanted:
            return steps
    return steps

for n in [7, 70, 700, 7000]:
    order_ids = list(range(101, 101 + n))
    newest = order_ids[-1]
    print(n, "orders | jump to the end: 1 | hunt for it:", find(order_ids, newest))
```

```output
7 orders | jump to the end: 1 | hunt for it: 7
70 orders | jump to the end: 1 | hunt for it: 70
700 orders | jump to the end: 1 | hunt for it: 700
7000 orders | jump to the end: 1 | hunt for it: 7000
```

the hunt column is the loop from 269, so it grows with the data, a straight line. the jump column never moves. a python list is a row of numbered slots, so order_ids[-1] goes straight to the last one. the python docs say that costs the same at any size.

the gotcha: no loop in the line doesnt mean flat. 104 in order_ids is one short line, but a missing id makes it walk the whole list, a straight line in disguise.

this is why databases bother with indexes, lookup shortcuts. the docs of Postgres, a popular database, say that with one it might walk only a few levels of a search tree, instead of scanning every row.

i expected the flat shape to need a clever trick, but it is just knowing where to jump.

the next one is the shape that looks harmless at 7 rows and isnt.

### check yourself

1. the shop keeps ids in order, newest last. dev A writes order_ids[-1], dev B writes max(order_ids). orders go from 7 to 7000. what happens to each?

<details><summary>answer</summary>

A stays at one look. B looks at every id, so it goes from about 7 to about 7000 looks. max cant know the list is sorted, so it has to check them all. the tempting answer is that both stay put because both return the same id.

</details>

2. a teammate says 104 in order_ids is flat because it has no loop. what do you tell them?

<details><summary>answer</summary>

in walks the list comparing each id until it finds 104 or runs out, so a missing id costs a look per order, a straight line. the tempting answer is flat, from counting lines of code instead of ids looked at.

</details>

3. hunting for a missing id takes 700 steps on 700 orders. the shop doubles three times. how many steps for the hunt, and for order_ids[-1]?

<details><summary>answer</summary>

5600 steps for the hunt, since 700 doubled three times is 700 times 8. order_ids[-1] is still 1 look. the tempting answer is 2100, from tripling 700 instead of doubling it three times.

</details>

---
prev: [269 big O in plain words, how work grows as data grows](./269-big-o-in-plain-words-how-work-grows-as-data-grows.md) | next: [271 curving up, when 10 times the data means 100 times the steps](./271-curving-up-when-10-times-the-data-means-100-times-the-steps.md)
