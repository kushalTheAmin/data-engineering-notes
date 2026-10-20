# 112: BETWEEN, ranges that include both ends
builds on: [027 dates without times, and times without dates](./027-dates-and-times-apart.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [107 comparisons, equal, not equal, bigger, smaller](./107-comparisons-equal-not-equal-bigger-smaller.md), [108 AND and OR, combining two tests](./108-and-or-combining-two-tests.md)
section: asking questions with SQL, part 12, ~2 min read

which products cost between 4.50 and 6.00? in plain english i would say the ends count, but does the database agree?

BETWEEN keeps a row when its value is at least the low end and at most the high end, both ends included. it is two [comparisons](./107-comparisons-equal-not-equal-bigger-smaller.md) joined by [AND](./108-and-or-combining-two-tests.md), written once. the shop, the imaginary gujarati snack store these notes run on, has 6 products:

```sql
SELECT name, price FROM products WHERE price BETWEEN 4.50 AND 6.00
```

```result
name | price
dhokla | 6.00
jalebi | 5.00
fafda | 4.50
```

dhokla, a steamed savory cake, costs exactly 6.00 and fafda, a crunchy gram flour snack, exactly 4.50, and both are in. so `price BETWEEN 4.50 AND 6.00` is the same as `price >= 4.50 AND price <= 6.00`. the low end goes first, and NOT BETWEEN flips the test.

i kept reading BETWEEN like a loop with range(), where the last number is left out. here nothing is left out, so you can trust the ends, and dates are the place it bites. a [date with no time](./027-dates-and-times-apart.md) in a range is read as midnight that day:

```sql
SELECT order_id, ordered_at FROM orders WHERE ordered_at BETWEEN '2026-04-01' AND '2026-04-03'
```

```result
order_id | ordered_at
101 | 2026-04-01 09:15:00
102 | 2026-04-01 18:40:00
```

order 103 was placed at 12:05 on 3 April, after the high end of 3 April at 00:00, so it vanishes with no error. reports that count "everything up to the 3rd" lose a whole day this way. a safer shape for timestamps is `>= '2026-04-01' AND < '2026-04-04'`, which returns all 3 orders.

### check yourself

1. the shop has dhokla 6.00, khandvi 7.50, jalebi 5.00, kaju katli 12.00, masala chai 3.00, fafda 4.50. how many rows does this return, and which product is the edge case?

```sql
SELECT name FROM products WHERE price NOT BETWEEN 4.50 AND 6.00
```
<details><summary>answer</summary>

```result
name
khandvi
kaju katli
masala chai
```

3 rows. dhokla and fafda sit exactly on the ends, BETWEEN keeps them, so NOT BETWEEN drops them. the tempting answer is 5, from thinking the ends are outside the range.

</details>

2. customers joined on these dates: Asha 2026-01-05, Bhavin 2026-01-20, Chirag 2026-02-11, Disha 2026-03-02, Esha 2026-03-15. who comes back?

```sql
SELECT name FROM customers WHERE joined_on BETWEEN DATE '2026-02-11' AND DATE '2026-03-02'
```
<details><summary>answer</summary>

```result
name
Chirag
Disha
```

both ends are real join dates, and both rows are kept. guessing only Chirag or only Disha treats one end as excluded. a pure date has no time of day, so the midnight trap from the timestamp query cannot happen here.

</details>

---
prev: [111 IN, matching against a list](./111-in-matching-against-a-list.md) | next: not written yet
