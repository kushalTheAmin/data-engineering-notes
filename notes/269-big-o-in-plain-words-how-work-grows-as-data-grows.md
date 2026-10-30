# 269: big O in plain words, how work grows as data grows
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md)
section: tricks that make data fast, part 1, ~2 min read

the reviews table in [268](./268-capstone-modeling-product-reviews-for-the-shop.md) had 4 rows, and a lookup there feels instant. would it with 4 million?

big O answers that without a stopwatch: count the steps your code takes, then ask how the count grows when the data does. steps, not seconds, because seconds change with the laptop.

below, the loop hiding inside [WHERE](./106-where-keeping-only-the-rows-that-match.md) hunts for an order id. a table is a list of rows ([079](./079-a-table-rows-are-records-columns-are-fields.md)), and the shop, the imaginary gujarati snack store these notes run on, has 7 orders, ids 101 to 107. the longer lists are pretend. a step is one look at one id.

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
    print(n, "orders | first one:", find(order_ids, 101), "| last one:", find(order_ids, 100 + n))
```

```output
7 orders | first one: 1 | last one: 7
70 orders | first one: 1 | last one: 70
700 orders | first one: 1 | last one: 700
7000 orders | first one: 1 | last one: 7000
```

read the last column. 10 times the orders, 10 times the steps. big O keeps that and throws the exact count away, because "about as many steps as rows" is what survives when data gets huge. the first-one column is why it usually quotes the worst case, the unlucky one where the thing is last or missing. luck gives 1 step at any size, but you cant plan on luck.

a database with nothing to help it does this loop, never stopping early. [Postgres](./211-a-database-server-postgres-where-most-app-data-lives.md), a popular database server, docs say that with no index (a lookup shortcut) it has to scan the entire table, row by row. at 7 million rows that is 7 million steps for every lookup.

i expected the interesting number to be how fast one lookup is, but the useful one is what happens to the steps when the data gets 10 times bigger.

### check yourself

1. predict what this prints. the second list is almost a thousand times longer.

```python
def find(order_ids, wanted):
    steps = 0
    for oid in order_ids:
        steps += 1
        if oid == wanted:
            return steps
    return steps

print(find(list(range(101, 108)), 104), find(list(range(101, 7001)), 104))
```

<details><summary>answer</summary>

it prints 4 4

the loop stops at 104, the 4th id, whatever comes after it. the tempting answer is 4 and about 6900, from thinking a longer list always costs more. size only bites when the thing is far down the list.

</details>

2. a customer mistypes an order id as 9999. with the same find, how many steps for the 7 shop orders and for a list of 7000?

<details><summary>answer</summary>

it prints 7 7000

a missing id is the worst case, the loop has to look at every id before it can say no. the tempting answer is 1 or 0, from thinking nothing to find means nothing to do.

</details>

---
prev: [268 capstone, modeling product reviews for the shop](./268-capstone-modeling-product-reviews-for-the-shop.md) | next: [270 flat and straight line, the two shapes of growth](./270-flat-and-straight-line-the-two-shapes-of-growth.md)
