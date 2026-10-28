# 245: changing a column type, the table rewrite and the lock
builds on: [242 row locks and table locks](./242-row-locks-and-table-locks.md), [225 ALTER TABLE, adding a column to a table that already has rows](./225-alter-table-adding-a-column-to-a-table-with-rows.md), [015 integer sizes, 8, 16, 32 and 64 bit numbers](./015-integer-sizes.md)
section: changing data safely, part 38, ~2 min read

the shops order_id is an INTEGER, and [015](./015-integer-sizes.md) showed a 32 bit integer tops out at 2147483647. one day you want BIGINT instead. its one line of SQL, so why do people dread it on a big table?

ALTER TABLE ... ALTER COLUMN ... TYPE changes the type of a column that already holds data. this is Postgres, the database that runs as its own server. [225](./225-alter-table-adding-a-column-to-a-table-with-rows.md) added a column cheaply in Postgres, but here every stored value changes shape. a slice of the shop, three order ids as bytes (a byte is a group of 8 bits):

```python
for order_id in [101, 102, 103]:
    print(order_id, list(order_id.to_bytes(4, "big")), "->", list(order_id.to_bytes(8, "big")))
```

```output
101 [0, 0, 0, 101] -> [0, 0, 0, 0, 0, 0, 0, 101]
102 [0, 0, 0, 102] -> [0, 0, 0, 0, 0, 0, 0, 102]
103 [0, 0, 0, 103] -> [0, 0, 0, 0, 0, 0, 0, 103]
```

same number, wider slot. i assumed widening would be free, like making a box bigger, but the size is fixed per column, so every row has to be stored again. Postgres writes a whole new copy of the table and its indexes (extra lookup copies kept for speed), then swaps it in. the docs say a type change normally does this, and that it can need up to double the disk space meanwhile.

the lock is the other half. the docs say ALTER TABLE takes an ACCESS EXCLUSIVE lock unless noted, the strongest [table lock](./242-row-locks-and-table-locks.md) (a mark on a whole table, the kind DROP TABLE takes), and that one blocks even a plain SELECT (a read). with 7 orders you never notice. with a billion, queries on orders wait for the whole copy.

one caveat: if the stored bytes dont change at all, the docs say no rewrite is needed. here they do change.

### check yourself

1. the type change on orders is running. Esha meanwhile reads from customers, a different shop table. does she wait?

<details><summary>answer</summary>

no. the lock lands on orders and on tables pointing at its order_id, like order_items, but customers has no such link, so it is untouched. the tempting yes assumes the whole database freezes. a plain read of order 106 would wait.

</details>

2. orders takes 50 GB on disk. how much free space should you have before the change?

<details><summary>answer</summary>

up to another 50 GB (a ceiling, counting indexes), since the docs say up to double while old and new copies coexist. the tempting answer is none, as if it changed in place.

</details>

---
prev: [244 deadlocks, two transactions waiting on each other](./244-deadlocks-two-transactions-waiting-on-each-other.md) | next: [246 changing a column type without downtime, add a new column and backfill it in batches](./246-add-a-new-column-and-backfill-it-in-batches.md)
