# 110: NOT, flipping a condition
builds on: [031 null, a marker for a missing value](./031-null.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [107 comparisons, equal, not equal, bigger, smaller](./107-comparisons-equal-not-equal-bigger-smaller.md), [108 AND and OR, combining two tests](./108-and-or-combining-two-tests.md), [109 parentheses, and AND runs before OR](./109-parentheses-and-runs-before-or.md)
section: asking questions with SQL, part 10, ~2 min read

i asked the shop for customers not in Jersey City, expecting the 3 who are left, and got 2. NOT looks like the easy one.

NOT flips a condition (a test that comes out true, false or unknown), so a row that failed now passes [WHERE](./106-where-keeping-only-the-rows-that-match.md) (the filter clause). it goes in front of a test like a [comparison](./107-comparisons-equal-not-equal-bigger-smaller.md), and `NOT price = 6` means the same as `price <> 6` (not equal). the shop, the imaginary gujarati snack store these notes run on, has 5 customers, and Esha has no city, her city is [null](./031-null.md) (a missing value). python first:

```python
rows = [("Asha", "Jersey City"), ("Bhavin", "Edison"), ("Chirag", "Jersey City"), ("Disha", "Hoboken"), ("Esha", None)]
print([name for name, city in rows if not city == "Jersey City"])
```

```output
['Bhavin', 'Disha', 'Esha']
```

python keeps Esha: None is not Jersey City, so the `not` makes it true. now the same ask in SQL:

```sql
SELECT name FROM customers WHERE NOT city = 'Jersey City'
```

```result
name
Bhavin
Disha
```

Esha is gone. 107 said a null row fails every test; fails meant not true. python answers False for None == a city, but SQL says unknown, NOT unknown is still unknown, and WHERE keeps only true. the row is in neither the Jersey City answer nor its opposite.

i assumed NOT was a clean mirror where every row lands on one side, and a null row lands on neither.

this bites in real reports: "orders where status is not delivered" quietly loses rows with a null status, if the column allows nulls (the shops doesnt). nothing errors.

NOT also grabs only the one test right after it, and runs before [AND](./108-and-or-combining-two-tests.md), so you flip a group with [parentheses](./109-parentheses-and-runs-before-or.md). the Postgres docs (a popular server database) list NOT above AND.

### check yourself

1. products slice: dhokla snack 6.00, jalebi sweet 5.00, kaju katli sweet 12.00, masala chai drink 3.00, fafda snack 4.50. predict the rows, then say what you would get if the NOT covered the whole condition instead.

```sql
SELECT name FROM products WHERE NOT category = 'snack' AND price < 6
```
<details><summary>answer</summary>

```result
name
jalebi
masala chai
```

NOT flips only the category test, then AND applies the price test, so non-snacks under 6 come back. the tempting reading is NOT (snack AND under 6), which would return everything except fafda, 4 of those 5 rows, but that needs parentheses written in.

</details>

2. the shop has 5 customers. how many rows does this return?

```sql
SELECT count(*) AS n FROM customers WHERE city = 'Jersey City' OR NOT city = 'Jersey City'
```
<details><summary>answer</summary>

```result
n
4
```

the answer is 4. a test or its opposite feels like it must cover every row, but Eshas null city makes both sides unknown, and OR of two unknowns is unknown, so she is kept by neither. guessing 5 assumes every row is either true or false.

</details>

---
prev: [109 parentheses, and AND runs before OR](./109-parentheses-and-runs-before-or.md) | next: [111 IN, matching against a list](./111-in-matching-against-a-list.md)
