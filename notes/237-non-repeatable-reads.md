# 237: non repeatable reads
builds on: [236 dirty reads](./236-dirty-reads.md), [231 isolation, two people at the same time](./231-isolation-two-people-at-the-same-time.md), [227 transactions, all or nothing](./227-transactions-all-or-nothing.md), [228 COMMIT and ROLLBACK, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md), [222 UPDATE, changing rows and why the WHERE matters](./222-update-changing-rows-and-why-the-where-matters.md)
section: changing data safely, part 30, ~2 min read

Asha reads the price of dhokla twice inside one transaction and gets 6.00, then 7.00. nobody rolled anything back, so which number was lying?

neither. a non repeatable read is when you read the same row twice in one [transaction](./227-transactions-all-or-nothing.md) (a group of changes that all happen or none do) and get different values, because someone else [committed](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md) (made permanent) a change in between. [236](./236-dirty-reads.md) was about reading drafts, this one is about reading real, finished data that moves under you. here is the shop, the imaginary gujarati snack store these notes run on, in Postgres (a database that runs as its own server) at its default isolation level, the setting for how much of others work you see. two people, Asha and Esha, take turns in the order listed:

```text
-- Postgres, default read committed level
asha:  BEGIN;
asha:  SELECT price FROM products WHERE name = 'dhokla';   -- 6.00
esha:  UPDATE products SET price = 7.00 WHERE name = 'dhokla';
esha:  COMMIT;
asha:  SELECT price FROM products WHERE name = 'dhokla';   -- 7.00
asha:  COMMIT;
```

the shop table has 6.00 before Esha touches it, as in [222](./222-update-changing-rows-and-why-the-where-matters.md):

```sql
SELECT name, price FROM products WHERE name = 'dhokla'
```

```result
name | price
dhokla | 6.00
```

i expected a changed number to mean something broke, but both reads were honest committed prices. [isolation](./231-isolation-two-people-at-the-same-time.md) (simultaneous users dont see half done work) only hid unfinished work, and Eshas change was finished. the Postgres docs list this as possible at read committed, because each query there sees whatever was committed when that query started.

so what: a report that totals prices at the start and again at the end of one transaction can disagree with itself, and the bug only shows when someone edits in the middle of the report, so it looks random. a stricter level fixes it, a later note covers that.

### check yourself

1. at read committed, Asha totals every price (the query below) at the start of her transaction. Esha then raises dhokla to 7.00 and commits. Asha totals again in the same transaction. what is her second total?

```sql
SELECT sum(price) AS total_before FROM products
```

<details><summary>answer</summary>

```result
total_before
38.00
```

the first total is the 38.00 above, and the second is 38.00 plus the 1.00 raise, so 39.00. the tempting 38.00 assumes a transaction freezes what you see, but at this level it doesnt.

</details>

2. Esha raises dhokla to 7.00 and commits, then sets it back to 6.00 and commits, both between Ashas two reads. Asha reads 6.00 then 6.00. did she get a non repeatable read?

<details><summary>answer</summary>

no. both reads returned the same value, so nothing non repeatable showed up. yes is tempting because the row changed in between, but the problem is a different value in your reads, not a change you never saw.

</details>

---
prev: [236 dirty reads](./236-dirty-reads.md) | next: not written yet
