# 166: joining on columns that can be NULL
builds on: [031 null, a marker for a missing value](./031-null.md), [114 three valued logic, true, false and unknown](./114-three-valued-logic-true-false-and-unknown.md), [156 inner join traced by hand](./156-inner-join-traced-by-hand.md), [157 ON, how a join decides which rows match](./157-on-how-a-join-decides-which-rows-match.md), [164 fan out, when a join multiplies rows](./164-fan-out-when-a-join-multiplies-rows.md)
section: combining tables with joins, part 12, ~2 min read

a lookup table (one you look values up in) has a row for the missing city, and Esha has no city. so why does she still vanish from the join?

NULL never matches NULL in a join. [ON](./157-on-how-a-join-decides-which-rows-match.md) keeps a pair only when its test is true, and by [three valued logic](./114-three-valued-logic-true-false-and-unknown.md) NULL = NULL is unknown, not true. the shop, the imaginary gujarati snack store these notes run on, now has delivery_zones: a zone per city, plus a catch-all row whose city is [NULL](./031-null.md) (a missing value). an [inner join](./156-inner-join-traced-by-hand.md) (keeps only matching pairs) on the city:

```sql
SELECT c.name, z.zone FROM customers c JOIN delivery_zones z ON c.city = z.city ORDER BY c.customer_id
```

```result
name | zone
Asha | north
Bhavin | south
Chirag | north
Disha | north
```

4 rows, Esha is gone, and no error. the catch-all row sits right there and nothing ever pairs with it. i expected a NULL to at least match its twin, and it doesnt, even in python None == None is True, so a hand written loop would have fooled me. the fix is IS NOT DISTINCT FROM, an equals that treats two NULLs as the same:

```sql
SELECT c.name, z.zone FROM customers c JOIN delivery_zones z ON c.city IS NOT DISTINCT FROM z.city ORDER BY c.customer_id
```

```result
name | zone
Asha | north
Bhavin | south
Chirag | north
Disha | north
Esha | unassigned
```

now 5 rows. one caution: if the zones table had two NULL rows, Esha would match both and [fan out](./164-fan-out-when-a-join-multiplies-rows.md) (a row kept once per match) into two.

you will hit this when a join key has gaps, like an optional customer_id on an event table. rows quietly drop out of a report and nobody sees an error. Postgres and DuckDB both have IS NOT DISTINCT FROM.

### check yourself

1. a teammate swaps the inner join for a LEFT JOIN (keeps every customer) on `c.city = z.city` and says Esha now gets the catch-all zone. what zone does Esha get?

```sql
SELECT c.name, z.zone FROM customers c LEFT JOIN delivery_zones z ON c.city = z.city WHERE c.name = 'Esha'
```

<details><summary>answer</summary>

```result
name | zone
Esha | NULL
```

the left join keeps Esha, but the ON test is still unknown for her, so no partner is found and the zone is filled in as NULL. the tempting answer is unassigned, from thinking the left join finds the NULL row.

</details>

2. delivery_zones has 4 rows, one with a NULL city. without running it, how many rows does this return?

```sql
SELECT count(*) AS n FROM delivery_zones a JOIN delivery_zones b ON a.city = b.city
```

<details><summary>answer</summary>

```result
n
3
```

each of the 3 named cities pairs with itself. the NULL row pairs with nothing, not even its own copy. the tempting answer is 4, because every row looks equal to itself.

</details>

---
prev: [165 double counting, why sums after a fan out lie](./165-double-counting-why-sums-after-a-fan-out-lie.md) | next: [167 anti join, rows with no match](./167-anti-join-rows-with-no-match.md)
