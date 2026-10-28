# 239: isolation levels, read committed
builds on: [238 phantoms](./238-phantoms.md), [237 non repeatable reads](./237-non-repeatable-reads.md), [236 dirty reads](./236-dirty-reads.md), [231 isolation, two people at the same time](./231-isolation-two-people-at-the-same-time.md), [227 transactions, all or nothing](./227-transactions-all-or-nothing.md), [228 COMMIT and ROLLBACK, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md)
section: changing data safely, part 32, ~2 min read

Asha types BEGIN Esha commits order 108, then Asha runs her first query. does she see 108? i guessed no, because BEGIN felt like the moment she gets her view. would you?

she does see it. an isolation level is how much of other peoples work a [transaction](./227-transactions-all-or-nothing.md) (a group of changes that all happen or none do) can see. [231](./231-isolation-two-people-at-the-same-time.md) said [isolation](./231-isolation-two-people-at-the-same-time.md) is the promise that simultaneous users dont see half done work. read committed, the default in Postgres (a database that runs as its own server), has one rule for reading: each SELECT sees only what was committed before that SELECT began. at this level the picture, a frozen view of the data, is taken per query, never per transaction.

the shop, the imaginary gujarati snack store these notes run on, has 7 orders. order 108 is imagined:

```sql
SELECT count(*) AS orders_now FROM orders
```

```result
orders_now
7
```

```text
-- Postgres, read committed
step  who    does                          ashas count
1     asha   BEGIN
2     asha   SELECT count(*) FROM orders   7
3     esha   INSERT order 108
4     asha   SELECT count(*) FROM orders   7
5     esha   COMMIT
6     asha   SELECT count(*) FROM orders   8
```

step 4 still says 7, because 108 is a draft until [COMMIT](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md) (make the changes permanent), so a [dirty read](./236-dirty-reads.md) (reading an uncommitted change) never happens here. step 6 says 8 because a new query is a new picture. at this level thats the source of a [non repeatable read](./237-non-repeatable-reads.md) (one row, two different values) and a [phantom](./238-phantoms.md) (a different set of rows): they are not bugs, just this rule showing up.

the Postgres docs say one SELECT never sees changes committed while it runs. i found that comforting.

so what: a report running five queries in one transaction can get five pictures, so its totals may not add up.

### check yourself

1. at read committed, Asha does BEGIN and waits. Esha commits an imagined change, order 107 set to cancelled. only then does Asha run the query below as her first query. what does she get?

```sql
SELECT count(*) AS delivered FROM orders WHERE status = 'delivered'
```

<details><summary>answer</summary>

on the real table it gives 5, since 107 is delivered today. after Eshas change the table gives 4 (<> means not equal):

```sql
SELECT count(*) AS delivered FROM orders WHERE status = 'delivered' AND order_id <> 107
```

```result
delivered
4
```

the tempting 5 assumes BEGIN freezes the picture, but the picture is taken when the query starts.

</details>

2. Asha runs one slow query that totals every order item, and it takes a minute. halfway through, Esha commits a new order with items. does the total include it?

<details><summary>answer</summary>

no. the query got its one picture at the start and keeps it until it ends. the tempting yes thinks the query might read the new rows, but changes committed during a query never show up in it.

</details>

---
prev: [238 phantoms](./238-phantoms.md) | next: [240 repeatable read, rows dont change under you mid transaction](./240-repeatable-read-rows-dont-change-under-you-mid-transaction.md)
