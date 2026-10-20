# 111: IN, matching against a list
builds on: [031 null, a marker for a missing value](./031-null.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [107 comparisons, equal, not equal, bigger, smaller](./107-comparisons-equal-not-equal-bigger-smaller.md), [108 AND and OR, combining two tests](./108-and-or-combining-two-tests.md), [110 NOT, flipping a condition](./110-not-flipping-a-condition.md)
section: asking questions with SQL, part 11, ~2 min read

city = 'Jersey City' OR city = 'Hoboken' is fine for two cities. what do you write when the list grows to ten?

IN is the shortcut: `city IN ('Jersey City', 'Hoboken')` keeps a row if its value equals any item in the list, the same as pythons `in`. the shop, the imaginary gujarati snack store these notes run on, has 5 customers. here is what [WHERE](./106-where-keeping-only-the-rows-that-match.md) does to each one:

```text
name   | city        | equals Jersey City | equals Hoboken | kept
Asha   | Jersey City | true               | false          | yes
Bhavin | Edison      | false              | false          | no
Chirag | Jersey City | true               | false          | yes
Disha  | Hoboken     | false              | true           | yes
Esha   | null        | unknown            | unknown        | no
```

```sql
SELECT name FROM customers WHERE city IN ('Jersey City', 'Hoboken')
```

```result
name
Asha
Chirag
Disha
```

IN is just the [OR](./108-and-or-combining-two-tests.md) chain (a row passes if either test is true) written once, so it returns the same 3 rows. Esha has a [null](./031-null.md) city (a missing value), the tests say unknown, and WHERE drops her, same as in [110](./110-not-flipping-a-condition.md).

i expected a list to be forgiving about nulls, and a null in the list is where it bites. NOT IN is a chain of not-equal tests joined by AND, so one unknown ruins the whole row:

```sql
SELECT name FROM customers WHERE city NOT IN ('Edison', NULL)
```

```result
name
```

zero rows, even though Asha, Chirag and Disha are clearly not in Edison. you rarely type a NULL by hand, but a list pulled from a column with a missing value does the same thing. the Postgres docs say NOT IN gives null, not true, when a null sits in the list.

---
prev: [110 NOT, flipping a condition](./110-not-flipping-a-condition.md) | next: [112 BETWEEN, ranges that include both ends](./112-between-ranges-that-include-both-ends.md)
