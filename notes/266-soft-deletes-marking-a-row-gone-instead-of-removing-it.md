# 266: soft deletes, marking a row gone instead of removing it
builds on: [265 created_at and updated_at, two timestamps every table carries](./265-created-at-and-updated-at-two-timestamps-every-table-carries.md), [223 DELETE, removing rows and what still points at them](./223-delete-removing-rows-and-what-still-points-at-them.md), [222 UPDATE, changing rows and why the WHERE matters](./222-update-changing-rows-and-why-the-where-matters.md), [115 IS NULL and IS NOT NULL](./115-is-null-and-is-not-null.md), [114 three valued logic, true, false and unknown](./114-three-valued-logic-true-false-and-unknown.md), [216 UNIQUE, no two rows may share a value](./216-unique-no-two-rows-may-share-a-value.md)
section: designing tables, part 13, ~2 min read

Disha closes her account at the shop, the imaginary gujarati snack store these notes run on. if you DELETE her row, how does the nightly copy job from [265](./265-created-at-and-updated-at-two-timestamps-every-table-carries.md) (it copies rows changed since its last run) ever hear about it? it asks for rows with a new updated_at, and a row that is gone has no updated_at.

a soft delete skips the [DELETE](./223-delete-removing-rows-and-what-still-points-at-them.md). the table gets a deleted_at column that stays NULL (empty) while the account is live, and leaving means an [UPDATE](./222-update-changing-rows-and-why-the-where-matters.md) that fills it in. the real DELETE is the hard delete, the row physically removed. here is Disha both ways, in customer_accounts, which holds 4 accounts:

```text
DELETE FROM customer_accounts WHERE customer_id = 4
UPDATE customer_accounts SET deleted_at = TIMESTAMP '2026-04-10 09:00:00', updated_at = TIMESTAMP '2026-04-10 09:00:00' WHERE customer_id = 4
```

| after Disha leaves | hard delete | soft delete |
|---|---|---|
| rows in the table | 3 | 4 |
| copy job, updated_at after 2026-04-10 00:00:00 | finds nothing | finds Disha |
| when she left | gone | deleted_at says 09:00 |

the hard delete column is what the table would show after the DELETE. with the soft one the row stays, so the copy job sees an ordinary change, as long as the UPDATE sets updated_at too like in 265. the price is that every query now has to remember the extra test. this one counts rows twice and stacks the two results with UNION ALL:

```sql
SELECT 'no filter' AS query, count(*) AS accounts FROM customer_accounts
UNION ALL SELECT 'live only', count(*) FROM customer_accounts WHERE deleted_at IS NULL
```

```result
query | accounts
no filter | 4
live only | 3
```

forget `WHERE deleted_at IS NULL` (the test for empty, `= NULL` never matches) once and a report counts people who left. it also keeps her email, so it isnt erasure if someone asks you to forget them.

i expected a delete to be its own kind of thing, but this one is an UPDATE and the row carries on like any other.

### check yourself

1. a report wants every account that was NOT soft deleted at exactly 2026-04-10 09:00:00. how many rows does this return?

```sql
SELECT count(*) AS n FROM customer_accounts WHERE deleted_at <> TIMESTAMP '2026-04-10 09:00:00'
```
<details><summary>answer</summary>

```result
n
0
```

the three live rows have a NULL deleted_at, so the test is [unknown](./114-three-valued-logic-true-false-and-unknown.md) for them (neither true nor false), and WHERE only keeps true. Disha fails it as well. the tempting answer is 3. live rows only show up if the test says IS NULL.

</details>

2. email is [UNIQUE](./216-unique-no-two-rows-may-share-a-value.md) (no two rows share a value) in customer_accounts. Disha comes back a month later and signs up with disha@example.com again. does the INSERT work after a hard delete? after a soft delete?

<details><summary>answer</summary>

after the hard delete it works, the old row is gone. after the soft delete it is refused, because her old row still holds that email. the tempting answer is that both work, since she left. a soft delete needs a plan for this, like reviving the old row.

</details>

---
prev: [265 created_at and updated_at, two timestamps every table carries](./265-created-at-and-updated-at-two-timestamps-every-table-carries.md) | next: [267 schemas as namespaces, folders for tables](./267-schemas-as-namespaces-folders-for-tables.md)
