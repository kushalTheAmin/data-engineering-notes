# 109: parentheses, and AND runs before OR
builds on: [101 SQL, you describe the result, the database figures out how](./101-sql-you-describe-the-result.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [107 comparisons, equal, not equal, bigger, smaller](./107-comparisons-equal-not-equal-bigger-smaller.md), [108 AND and OR, combining two tests](./108-and-or-combining-two-tests.md)
section: asking questions with SQL, part 9, ~2 min read

i asked for snacks or sweets under 6, wrote it the way i would say it out loud, and khandvi at 7.50 came back anyway. the query ran fine.

when a WHERE mixes [AND and OR](./108-and-or-combining-two-tests.md) (the words that join two tests), AND goes first, like multiplication before addition. that rule is called precedence (which operator runs first), and parentheses overrule it. the shop, the imaginary gujarati snack store these notes run on, has 6 products, each in a category with a price.

```sql
SELECT name, category, price FROM products WHERE category = 'snack' OR category = 'sweet' AND price < 6
```

```result
name | category | price
dhokla | snack | 6.00
khandvi | snack | 7.50
jalebi | sweet | 5.00
fafda | snack | 4.50
```

the database grouped it as snack OR (sweet AND under 6). so every snack gets in at any price, and only the sweets face the price test. python does the same with `a or b and c`. now the grouping i meant:

```sql
SELECT name, category, price FROM products WHERE (category = 'snack' OR category = 'sweet') AND price < 6
```

```result
name | category | price
jalebi | sweet | 5.00
fafda | snack | 4.50
```

the parentheses make the OR happen first, then the price test applies to what survives. 4 rows became 2.

i expected the database to read left to right like i do, and it quietly grabs the AND first.

neither query errors, so the only warning is a result that looks a bit too big. the Postgres docs say the precedence is fixed and to add parentheses when you want another grouping. so whenever AND and OR share a WHERE, put the parentheses in, even where they change nothing.

### check yourself

1. without running it, which products come back, and why not only kaju katli (the 12.00 sweet)?

```sql
SELECT name FROM products WHERE category = 'drink' OR category = 'sweet' AND price > 10
```
<details><summary>answer</summary>

```result
name
kaju katli
masala chai
```

AND goes first, so it is drink OR (sweet AND over 10). masala chai is a drink, so it gets in at 3.00. the tempting answer, kaju katli alone, comes from reading left to right as (drink OR sweet) AND over 10.

</details>

2. customers Asha and Chirag live in Jersey City, Bhavin in Edison. Chirag joined on 2026-02-11. how many rows does this return, and would parentheses around the two city tests change it?

```sql
SELECT name FROM customers WHERE city = 'Jersey City' OR city = 'Edison' AND joined_on < DATE '2026-02-01'
```
<details><summary>answer</summary>

```result
name
Asha
Bhavin
Chirag
```

3 rows. Chirag is in because the Jersey City test stands alone, so his join date is never checked. with parentheses around the two city tests it drops to 2 rows, Asha and Bhavin, because Chirag joined after February 1.

</details>

---
prev: [108 AND and OR, combining two tests](./108-and-or-combining-two-tests.md) | next: [110 NOT, flipping a condition](./110-not-flipping-a-condition.md)
