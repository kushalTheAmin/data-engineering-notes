# 247: changing a column type without downtime, keeping the new column in sync with new writes
builds on: [246 changing a column type without downtime, add a new column and backfill it in batches](./246-add-a-new-column-and-backfill-it-in-batches.md), [220 INSERT, adding rows and matching values to columns](./220-insert-adding-rows-and-matching-values-to-columns.md), [222 UPDATE, changing rows and why the WHERE matters](./222-update-changing-rows-and-why-the-where-matters.md), [031 null, a marker meaning there is no value](./031-null.md)
section: changing data safely, part 40, ~2 min read

to move a column to a bigger type without freezing the table, [246](./246-add-a-new-column-and-backfill-it-in-batches.md) added a second column, order_id_big, and copied old values in. an order 108 placed after the copy would keep a [NULL](./031-null.md) (no value) there. who fills the new column for orders that dont exist yet?

a trigger is a rule the database runs by itself every time a row is written. this is Postgres. the shop, the imaginary gujarati snack store these notes run on, uses one to copy order_id into order_id_big on every [INSERT](./220-insert-adding-rows-and-matching-values-to-columns.md) (adding a row) and [UPDATE](./222-update-changing-rows-and-why-the-where-matters.md) (changing a row). read it as: before a row is stored, set order_id_big to order_id.

```text
-- Postgres
CREATE FUNCTION copy_order_id() RETURNS trigger AS $$
BEGIN
  NEW.order_id_big := NEW.order_id;
  RETURN NEW;
END $$ LANGUAGE plpgsql;

CREATE TRIGGER orders_sync BEFORE INSERT OR UPDATE ON orders
FOR EACH ROW EXECUTE FUNCTION copy_order_id();
```

NEW is the row about to be stored. it has to be BEFORE, because only then does changing NEW change what lands in the table. i found it odd that the order of two steps decides the result, creating the trigger and backfilling. Esha places order 108 between them:

| step | trigger first | backfill first |
| --- | --- | --- |
| 1 | create the trigger | backfill orders 101 to 107 |
| 2 | Esha places 108, trigger fills it | Esha places 108, nothing fills it |
| 3 | backfill orders 101 to 107 | create the trigger |
| NULLs left | 0 | 1 |

a trigger never goes back for old rows. thats why the [backfill](./246-add-a-new-column-and-backfill-it-in-batches.md) (filling old rows in batches) is still needed, and why the trigger goes in first. backfill first, and you need a second pass to catch 108.

why not just change the app to write both columns? any other writer skips that, a one-off script, a hand typed INSERT, an old copy of the app still running mid deploy. the trigger sees them all. drop it after the swap, it slows every write.

### check yourself

1. the backfill finished for orders 101 to 107. then Esha places 108 and 109, and only after that you create the trigger. what does SELECT count(*) FROM orders WHERE order_id_big IS NULL return, and what fixes it?

<details><summary>answer</summary>

it returns 2 (orders 108 and 109). the trigger only runs on writes after it exists, so it never fills them. running the backfill again over those ids fixes it. the tempting 0 treats a trigger as a fix for existing rows.

</details>

2. a teammate says skip the trigger, the app is the only thing that writes orders, so just make the app set both columns. name one way this still leaves a NULL.

<details><summary>answer</summary>

anyone writing outside the app: a one-off script, a manual INSERT in a database console, another service. the trigger runs inside the database, so every writer goes through it. the tempting answer is that the app covers everything.

</details>

---
prev: [246 changing a column type without downtime, add a new column and backfill it in batches](./246-add-a-new-column-and-backfill-it-in-batches.md) | next: [248 changing a column type without downtime, the swap in one short transaction](./248-the-swap-renaming-two-columns-in-one-transaction.md)
