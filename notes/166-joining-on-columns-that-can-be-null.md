# 166: joining on columns that can be NULL
builds on: [031 null, a marker for a missing value](./031-null.md), [114 three valued logic, true, false and unknown](./114-three-valued-logic-true-false-and-unknown.md), [115 IS NULL and IS NOT NULL](./115-is-null-and-is-not-null.md), [155 why joins, the answer lives in more than one table](./155-why-joins-the-answer-lives-in-more-than-one-table.md), [156 inner join traced by hand](./156-inner-join-traced-by-hand.md), [157 ON, how a join decides which rows match](./157-on-how-a-join-decides-which-rows-match.md)
section: combining tables with joins, part 12, ~2 min read

the shop (the imaginary gujarati snack store these notes run on) has a delivery_zones table with a row for "no city". Esha has no city. so why does she vanish when i join them?

a join on a column that can be [NULL](./031-null.md) (a missing value) never pairs two NULLs, because the [ON test](./157-on-how-a-join-decides-which-rows-match.md) (the rule that pairs rows) comes out unknown, not true, and a join keeps a pair only on true. here is the loop from [155](./155-why-joins-the-answer-lives-in-more-than-one-table.md) on city, in python, where None == None is True:

```python
cities = [("Asha", "Jersey City"), ("Esha", None)]
zones = [("Jersey City", "east"), (None, "no city")]
for name, c in cities:
    for z, zone in zones:
        if c == z:
            print(name, zone)
```

```output
Asha east
Esha no city
```

SQL treats unknown like false in a join, as in [114](./114-three-valued-logic-true-false-and-unknown.md), so the same join on all 5 customers is an [inner join](./156-inner-join-traced-by-hand.md) (keeps only matching pairs) that loses her:

```sql
SELECT c.name, z.zone FROM customers c JOIN delivery_zones z ON c.city = z.city ORDER BY c.customer_id
```

```result
name | zone
Asha | east
Bhavin | central
Chirag | east
Disha | east
```

the fix is IS NOT DISTINCT FROM, an equals that counts two NULLs as the same (the Postgres docs, a server database, say it never returns null):

```sql
SELECT c.name, z.zone FROM customers c JOIN delivery_zones z ON c.city IS NOT DISTINCT FROM z.city ORDER BY c.customer_id
```

```result
name | zone
Asha | east
Bhavin | central
Chirag | east
Disha | east
Esha | no city
```

i expected SQL to behave like my python loop, and it doesnt. a [left join](./159-left-join-keep-every-row-from-the-left-table.md) (keeps every left row, matched or not) hides it worse: Esha stays, with a NULL zone, which looks like a zone nobody filled in.

so if you join on a key that allows NULL, you silently lose those rows. [115](./115-is-null-and-is-not-null.md) only hinted at this family of tests, and this is where it pays.

### check yourself

1. a teammate says "orders.customer_id is NOT NULL in the shop, so joining orders to customers on it can never lose a row to this". is that enough to be safe? what about customers.city?

<details><summary>answer</summary>

the NOT NULL column cant hit this problem, since no NULL ever reaches the comparison, and the orders join in 155 gave 7 of 7 rows. city can: Esha has none, so joining on it with = loses her, as above. the tempting answer is "NULL joins are always risky", but only a nullable key on a side that has NULLs bites.

</details>

2. you switch that join to a LEFT JOIN, still with plain =. predict the count, and what count(*) would have said instead.

```sql
SELECT count(z.zone) AS n FROM customers c LEFT JOIN delivery_zones z ON c.city = z.city
```

<details><summary>answer</summary>

```result
n
4
```

Esha is kept with a NULL zone and count(z.zone) skips NULL, so 4. count(*) would say 5 and hide the problem. the tempting answer is 5, from thinking the left join fixed it.

</details>

---
prev: [165 double counting, why sums after a fan out lie](./165-double-counting-why-sums-after-a-fan-out-lie.md) | next: not written yet
