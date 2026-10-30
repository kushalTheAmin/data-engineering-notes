# 269: big O in plain words, how work grows as data grows
builds on: [268 capstone, modeling product reviews for the shop](./268-capstone-modeling-product-reviews-for-the-shop.md)
section: tricks that make data fast, part 1, ~2 min read

the reviews table in [268](./268-capstone-modeling-product-reviews-for-the-shop.md) had 4 rows, so a lookup was nothing. if the shop, the imaginary gujarati snack store these notes run on, grows to 4 million reviews, how much slower is the same lookup?

big O is a way to say how the number of steps a piece of code takes grows when the data grows. steps, not seconds, because seconds change with the machine and steps dont.

find() below walks a list of reviews, each one a dictionary, and counts every row it looks at. the rows are made up, one per customer_id.

```python
def find(rows, wanted):
    steps = 0
    for row in rows:
        steps += 1
        if row["customer_id"] == wanted:
            break
    return steps

for n in (1000, 2000, 4000):
    reviews = [{"customer_id": i, "rating": 5} for i in range(1, n + 1)]
    print(n, "rows: first", find(reviews, 1), "| last", find(reviews, n), "| missing", find(reviews, 0))
```

```output
1000 rows: first 1 | last 1000 | missing 1000
2000 rows: first 1 | last 2000 | missing 2000
4000 rows: first 1 | last 4000 | missing 4000
```

double the rows, double the steps. the lucky first row costs 1 at any size, but luck isnt a plan, so big O looks at the worst case, where the wanted row is last or isnt there at all. the missing one surprised me: it costs as much as the last row, because you only know its missing after looking at everything.

this shape is written O(n), say "big O of n", where n is the row count.

the docs of Postgres, a popular database, say that with no advance preparation the system has to scan the entire table, row by row, to find matching entries. so at 4 million rows, one lookup is up to 4 million looks.

i figured slow was about the computer, but its the shape of the loop, and the same loop has that shape on any machine. doubling is one shape, the next one has more.

### check yourself

1. a search for a customer who never wrote a review runs over 500 reviews. how many rows does it look at, and how many if the table grows to 5000?
<details><summary>answer</summary>

500, then 5000. the loop can only say "not here" after seeing every row. the tempting answer is "few, it gives up early", but stopping early is only possible when it finds a match.

</details>

2. a loop scans order_items, sorted by order_id then product_id, for the row (105, 4) and stops at the match. how many rows does it look at, out of 13?

```sql
SELECT n AS steps FROM (
    SELECT order_id, product_id, row_number() OVER (ORDER BY order_id, product_id) AS n
    FROM order_items
) WHERE order_id = 105 AND product_id = 4
```

<details><summary>answer</summary>

```result
steps
9
```

9, the match is the 9th row. the tempting 13 treats every scan as the worst case, but the worst case needs the match to be last or missing.

</details>

---
prev: [268 capstone, modeling product reviews for the shop](./268-capstone-modeling-product-reviews-for-the-shop.md) | next: not written yet
