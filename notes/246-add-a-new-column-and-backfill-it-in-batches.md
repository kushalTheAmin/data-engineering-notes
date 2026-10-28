# 246: changing a column type without downtime, add a new column and backfill it in batches
builds on: [245 changing a column type, the table rewrite and the lock](./245-changing-a-column-type-the-table-rewrite-and-the-lock.md), [243 SELECT FOR UPDATE, locking on purpose](./243-select-for-update-locking-on-purpose.md), [242 row locks and table locks](./242-row-locks-and-table-locks.md), [225 ALTER TABLE, adding a column to a table that already has rows](./225-alter-table-adding-a-column-to-a-table-with-rows.md), [112 BETWEEN, ranges that include both ends](./112-between-ranges-that-include-both-ends.md), [222 UPDATE, changing rows and why the WHERE matters](./222-update-changing-rows-and-why-the-where-matters.md)
section: changing data safely, part 39, ~2 min read

[245](./245-changing-a-column-type-the-table-rewrite-and-the-lock.md) ended with orders stuck behind one big lock (a mark that makes others wait) while the whole table was copied. what if you never change the old column at all, and just put a second one next to it?

a backfill fills a new column for the rows that already exist, a small batch at a time. this is Postgres, the database that runs as its own server. the shop, the imaginary gujarati snack store these notes run on, wants BIGINT (the 8 byte integer) ids. so we add order_id_big, which starts as [NULL](./031-null.md) (no value) on every row, then copy order_id into it, 3 rows per UPDATE (a statement that changes values in existing rows):

```python
orders = [{"order_id": i, "order_id_big": None} for i in range(101, 108)]
for start in range(0, len(orders), 3):
    batch = orders[start:start + 3]
    for row in batch:
        row["order_id_big"] = row["order_id"]
    empty = sum(row["order_id_big"] is None for row in orders)
    print("batch", start // 3 + 1, [row["order_id"] for row in batch], "still empty:", empty)
```

```output
batch 1 [101, 102, 103] still empty: 4
batch 2 [104, 105, 106] still empty: 1
batch 3 [107] still empty: 0
```

in Postgres each batch is one statement, a slice picked by key ([BETWEEN](./112-between-ranges-that-include-both-ends.md), a test for a range of values):

```text
-- Postgres
ALTER TABLE orders ADD COLUMN order_id_big BIGINT;
UPDATE orders SET order_id_big = order_id WHERE order_id BETWEEN 101 AND 103;
UPDATE orders SET order_id_big = order_id WHERE order_id BETWEEN 104 AND 106;
```

i expected the safe way to be one careful command, but its lots of small ones. the [ADD COLUMN](./225-alter-table-adding-a-column-to-a-table-with-rows.md) needs no copy of the table (just a brief lock), and each UPDATE takes [row locks](./242-row-locks-and-table-locks.md) (marks on single rows, so others wait) only on its own rows, held until the statement finishes, since a lone statement is its own transaction ([243](./243-select-for-update-locking-on-purpose.md)). so anyone changing those same rows waits at most one batch.

a retry is safe too. order_id_big = order_id gives the same answer run twice, unlike the price + 1 trap in [222](./222-update-changing-rows-and-why-the-where-matters.md), where a second run adds again. with a billion rows and 10000 per batch thats 100000 UPDATEs.

### check yourself

1. all 3 batches have run. Esha then places order 108. what does SELECT count(*) FROM orders WHERE order_id_big IS NULL return?

<details><summary>answer</summary>

it returns 1. order 108 was inserted after the copy, and nothing in this setup fills order_id_big for it. the tempting 0 assumes the column keeps itself up to date.

</details>

2. a teammate backfills with one UPDATE over every order instead of batches. Esha tries to change order 106 while the backfill runs. when can the single UPDATE make her wait, compared to batches of 3?

<details><summary>answer</summary>

the single UPDATE keeps every row it has reached locked until it ends, so once it passes 106 she waits for the whole thing. with batches she waits only while 106 is in the batch running right now. the tempting answer is that nothing changes because both do the same total work.

</details>

---
prev: [245 changing a column type, the table rewrite and the lock](./245-changing-a-column-type-the-table-rewrite-and-the-lock.md) | next: not written yet
