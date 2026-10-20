# 114: three valued logic, true, false and unknown
builds on: [023 true and false, the boolean](./023-true-and-false-the-boolean.md), [031 null, a marker for a missing value](./031-null.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [107 comparisons, equal, not equal, bigger, smaller](./107-comparisons-equal-not-equal-bigger-smaller.md), [108 AND and OR, combining two tests](./108-and-or-combining-two-tests.md), [110 NOT, flipping a condition](./110-not-flipping-a-condition.md), [113 LIKE, matching text patterns](./113-like-matching-text-patterns.md)
section: asking questions with SQL, part 14, ~2 min read

Esha has no city. so is `city = 'Hoboken'` true or false for her? neither, and that third answer has rules.

three valued logic means a test comes out true, false or unknown, and a [null](./031-null.md) (a missing value) makes it unknown. [110](./110-not-flipping-a-condition.md) and [113](./113-like-matching-text-patterns.md) lost Esha this way, so here are the rules. you know python skips the rest of `False and anything`, and unknown works alike: it means could be either, so if both give one answer, that answer is known. for [AND and OR](./108-and-or-combining-two-tests.md), the rows with an unknown:

```text
a       | b       | a AND b | a OR b
unknown | true    | unknown | true
unknown | false   | false   | unknown
unknown | unknown | unknown | unknown
```

a false settles an AND, a true settles an OR. the shop, the imaginary gujarati snack store these notes run on, has 5 customers, and here are two, with a [comparison](./107-comparisons-equal-not-equal-bigger-smaller.md) each side of an AND:

```sql
SELECT name, city = 'Hoboken' AS in_hoboken, joined_on < DATE '2026-03-01' AS before_march, city = 'Hoboken' AND joined_on < DATE '2026-03-01' AS both_tests FROM customers WHERE name IN ('Disha', 'Esha') ORDER BY customer_id
```

```result
name | in_hoboken | before_march | both_tests
Disha | true | false | false
Esha | NULL | false | false
```

Esha joined on March 15, so her both_tests is false even though her city is unknown. NOT of false is true, so `WHERE NOT (city = 'Hoboken' AND joined_on < DATE '2026-03-01')` keeps her, where NOT on the city alone dropped her.

i assumed unknown would spread like a stain through everything it touches, and it only spreads when the other side cant settle it.

a missing-row bug can come and go here. an OR on a column that is null in some rows keeps those rows when the other test is true and drops them when it is false, with no error, because [WHERE](./106-where-keeping-only-the-rows-that-match.md) keeps only true. the next one is how to ask for the unknown rows on purpose.

### check yourself

1. predict the count, and say what you would guess if Esha dropped out like she did in 110.

```sql
SELECT count(*) AS n FROM customers WHERE NOT (city = 'Hoboken' AND joined_on < DATE '2026-03-01')
```
<details><summary>answer</summary>

```result
n
5
```

all 5. Disha is true AND false, which is false, and Esha is unknown AND false, which is also false, so NOT makes both true. the tempting answer is 4, from assuming any null row is dropped.

</details>

2. Disha lives in Hoboken, Esha has no city and joined 2026-03-15. which rows does this return? what changes if `>` becomes `>=`?

```sql
SELECT name FROM customers WHERE city = 'Hoboken' OR joined_on > DATE '2026-03-15'
```
<details><summary>answer</summary>

```result
name
Disha
```

Disha only. Esha joined exactly on 2026-03-15, so her date test is false, and unknown OR false is unknown, which WHERE drops. with `>=` her date test is true, unknown OR true is true, and she comes back. the tempting answer is Disha and Esha, from thinking OR ignores the unknown side.

</details>

---
prev: [113 LIKE, matching text patterns](./113-like-matching-text-patterns.md) | next: [115 IS NULL and IS NOT NULL](./115-is-null-and-is-not-null.md)
