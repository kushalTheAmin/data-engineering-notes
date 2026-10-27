# 238: phantoms
builds on: [237 non repeatable reads](./237-non-repeatable-reads.md), [231 isolation, two people at the same time](./231-isolation-two-people-at-the-same-time.md), [227 transactions, all or nothing](./227-transactions-all-or-nothing.md), [228 COMMIT and ROLLBACK, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md), [220 INSERT, adding rows and matching values to columns](./220-insert-adding-rows-and-matching-values-to-columns.md)
section: changing data safely, part 31, ~2 min read

Asha lists the pending orders inside one transaction and gets one row. she runs the exact same query again and gets two. no row she read changed, so where did the second one come from?

thats a phantom read: you re-run a query in one [transaction](./227-transactions-all-or-nothing.md) (a group of changes that all happen or none do) and the set of rows matching it is different, because someone [committed](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md) (made permanent) a change in between. [237](./237-non-repeatable-reads.md) was one row changing its value, this is a row joining the results. here is the shop, the imaginary gujarati snack store these notes run on, as a list of rows, with a loop and an if standing in for the WHERE (the filter). the three rows are a slice, and order 108 is imagined, the shop only has 7:

```python
orders = [
    {"order_id": 105, "status": "delivered"},
    {"order_id": 106, "status": "pending"},
    {"order_id": 107, "status": "delivered"},
]

def pending():
    return [o["order_id"] for o in orders if o["status"] == "pending"]

print("asha, first look:", pending())
orders.append({"order_id": 108, "status": "pending"})  # esha commits
print("asha, second look:", pending())
```

```output
asha, first look: [106]
asha, second look: [106, 108]
```

order 108 is the phantom. i assumed a changed row was the only thing that could move under me, but the group of rows a WHERE picks can change shape too. an [INSERT](./220-insert-adding-rows-and-matching-values-to-columns.md) that matches does it, and so does a delete or an edit.

in Postgres, a database that runs as its own server, the docs say phantoms are possible at read committed, the default [isolation](./231-isolation-two-people-at-the-same-time.md) level (each query sees whats committed when it starts). a stricter level, repeatable read, can stop them in Postgres.

so what: a report that prints a count and then lists the rows can show a count that disagrees with its own list.

### check yourself

1. at read committed, Asha runs the query below as her first step. Esha then commits order 108 as pending, and Asha runs it again. what are her two numbers?

```sql
SELECT count(*) AS pending_now FROM orders WHERE status = 'pending'
```

<details><summary>answer</summary>

```result
pending_now
1
```

that 1 is her first number, and the second is 2. the tempting 1 twice assumes a transaction freezes what you see, but at this level the second query sees the new commit.

</details>

2. Esha adds a new snack called thepla to products and commits, between two reads by Asha. one read is `WHERE name = 'dhokla'`, the other counts rows `WHERE category = 'snack'`. which one can show a phantom?

```sql
SELECT count(*) AS snacks FROM products WHERE category = 'snack'
```

<details><summary>answer</summary>

```result
snacks
3
```

the snack count can go from 3 to 4. the dhokla read returns the same single row both times. the tempting answer is both, since a row was added, but a phantom only shows in a query whose matching set the new row joins.

</details>

---
prev: [237 non repeatable reads](./237-non-repeatable-reads.md) | next: [239 isolation levels, read committed](./239-isolation-levels-read-committed.md)
