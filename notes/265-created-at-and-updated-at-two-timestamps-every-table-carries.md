# 265: created_at and updated_at, two timestamps every table carries
builds on: [264 naming conventions, names people can guess](./264-naming-conventions-names-people-can-guess.md), [222 UPDATE, changing rows and why the WHERE matters](./222-update-changing-rows-and-why-the-where-matters.md), [215 NOT NULL and DEFAULT, required columns and fallback values](./215-not-null-and-default-required-columns-and-fallback-values.md), [030 store in UTC, show in local time](./030-store-utc-show-local.md)
section: designing tables, part 12, ~2 min read

order 104 in the shop (the imaginary gujarati snack store these notes run on) says cancelled. cancelled when? the orders table (a grid of rows) has one timestamp, a date plus a time, called ordered_at, so it cant tell you.

the fix is two columns on every table. created_at is the moment the row was inserted (added), set once and never touched again. updated_at is the moment the row last changed, so it starts equal to created_at and moves on every [UPDATE](./222-update-changing-rows-and-why-the-where-matters.md). the shop keeps them in order_tracking (a slice of 3 orders, stored in [UTC](./030-store-utc-show-local.md), the one reference clock):

```sql
SELECT order_id, status, created_at, updated_at FROM order_tracking WHERE order_id IN (104, 105, 106) ORDER BY order_id
```

```result
order_id | status | created_at | updated_at
104 | cancelled | 2026-04-04 08:30:00 | 2026-04-04 08:45:00
105 | delivered | 2026-04-06 19:10:00 | 2026-04-06 20:15:00
106 | pending | 2026-04-08 10:00:00 | 2026-04-08 10:00:00
```

104 was cancelled 15 minutes after it was placed. 106 has two equal times, so nothing has touched it since. created_at stays put, updated_at is the one that moves.

the catch i didnt expect: the database wont move updated_at for you. a [DEFAULT](./215-not-null-and-default-required-columns-and-fallback-values.md) (a value filled in on insert) can fill both at insert, but an UPDATE only changes what its SET names:

```text
UPDATE order_tracking SET status = 'delivered', updated_at = current_timestamp WHERE order_id = 106
```

MySQL can do it in the column with ON UPDATE CURRENT_TIMESTAMP, and in Postgres the usual way is a trigger, code the database runs on every change.

so what: a nightly job that copies only rows changed since its last run asks WHERE updated_at > that time. one writer that forgets the column and its changes are invisible to that job.

i assumed updated_at worked like a files modified time, kept by the system, but nothing moves it unless somebody writes to it.

### check yourself

1. a nightly job copies every order_tracking row with updated_at after 2026-04-06 00:00:00. which order ids does it copy? (107 was last updated 2026-04-09 14:30:00, 104 on the 4th.)
```sql
SELECT order_id FROM order_tracking WHERE updated_at > TIMESTAMP '2026-04-06 00:00:00' ORDER BY order_id
```
<details><summary>answer</summary>

```result
order_id
105
106
107
```

106 is copied even though nothing changed it, because updated_at starts equal to created_at and a new row counts as changed. the tempting answer is 105 and 107 only.

</details>

2. someone fixes order 106 by typing UPDATE order_tracking SET status = 'delivered' WHERE order_id = 106 in a console. the nightly job from question 1 runs again. does the copy learn 106 is delivered?
<details><summary>answer</summary>

no. the row changed but updated_at is still 2026-04-08 10:00:00, so if the job already copied 106 it sees nothing new. the tempting answer is yes, since the database knows the row changed, but it only records what the statement says.

</details>

---
prev: [264 naming conventions, names people can guess](./264-naming-conventions-names-people-can-guess.md) | next: not written yet
