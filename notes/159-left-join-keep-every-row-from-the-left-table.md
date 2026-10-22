# 159: left join, keep every row from the left table
builds on: [031 null, a marker for a missing value](./031-null.md), [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md), [155 why joins, the answer lives in more than one table](./155-why-joins-the-answer-lives-in-more-than-one-table.md), [156 inner join traced by hand](./156-inner-join-traced-by-hand.md), [157 ON, how a join decides which rows match](./157-on-how-a-join-decides-which-rows-match.md), [158 table aliases, short nicknames for tables](./158-table-aliases-short-nicknames-for-tables.md)
section: combining tables with joins, part 5, ~2 min read

Esha is a customer in the shop (the imaginary gujarati snack store these notes run on), and every join so far lost her. how do you ask for customers and their orders without losing the ones who ordered nothing?

a left join is an [inner join](./156-inner-join-traced-by-hand.md) (keeps only pairs where the match holds) that also keeps every row of the left table. the left table is the one written before the word JOIN. here is the loop from [155](./155-why-joins-the-answer-lives-in-more-than-one-table.md), with one extra step, on a slice of two customers:

```python
customers = [{"customer_id": 4, "name": "Disha"}, {"customer_id": 5, "name": "Esha"}]
orders = [{"order_id": 105, "customer_id": 4}]
for c in customers:
    found = False
    for o in orders:
        if o["customer_id"] == c["customer_id"]:
            print(c["name"], o["order_id"])
            found = True
    if not found:
        print(c["name"], None)
```

```output
Disha 105
Esha None
```

the `if not found` is the whole idea. a customer who matched nothing still gets a row, with a blank where the order would be. in SQL that blank is [NULL](./031-null.md) (a marker for a missing value), on all 5 customers, with [aliases](./158-table-aliases-short-nicknames-for-tables.md) c and o:

```sql
SELECT c.name, o.order_id FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id ORDER BY c.name, o.order_id
```

```result
name | order_id
Asha | 101
Asha | 103
Asha | 106
Bhavin | 102
Bhavin | 107
Chirag | 104
Disha | 105
Esha | NULL
```

8 rows, one more than the 7 an inner join gave. i expected the missing partner to stop the row from existing, but the row stays and only the order side is empty.

left means first in the query text, not the left of the screen. write `orders o LEFT JOIN customers c` and you get 7 rows, because every order has a customer. the Postgres docs call it a LEFT OUTER JOIN, and OUTER is optional.

this is how a report keeps customers with zero orders, and those NULLs need handling, which is the next problem.

### check yourself

1. the shop adds a sixth customer who ordered nothing. how many rows does the query above return now? and how many if you swap the tables to `orders o LEFT JOIN customers c`?
<details><summary>answer</summary>

9 for the first, since the new customer adds one row like Esha. 7 for the swapped one, since the left table is now orders and still has 7 rows. the tempting answer is 9 for both, from thinking a left join always grows the result. it only guarantees every left row appears at least once.

</details>

2. Asha has 3 orders, so she appears 3 times in the result above. a teammate says a left join should give one row per customer. is that right?
<details><summary>answer</summary>

no. a left join keeps every left row at least once, and a customer with 3 matches gets 3 rows. only unmatched customers get a single row with NULL. one row per customer needs a [GROUP BY](./143-group-by-one-group-per-value.md) (one row per group) on top, the tempting answer comes from mixing up "at least one" with "exactly one".

</details>

---
prev: [158 table aliases, short nicknames for tables](./158-table-aliases-short-nicknames-for-tables.md) | next: [160 the nulls a left join creates](./160-the-nulls-a-left-join-creates.md)
