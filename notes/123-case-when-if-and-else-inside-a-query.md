# 123: CASE WHEN, if and else inside a query
builds on: [031 null, a marker for a missing value](./031-null.md), [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [107 comparisons, equal, not equal, bigger, smaller](./107-comparisons-equal-not-equal-bigger-smaller.md), [114 three valued logic, true, false and unknown](./114-three-valued-logic-true-false-and-unknown.md), [122 computed columns and AS](./122-computed-columns-and-as.md)
section: asking questions with SQL, part 23, ~2 min read

can a query label every product cheap, regular or treat, with no new column in the table? [122](./122-computed-columns-and-as.md) made a column out of arithmetic (a computed column), this one makes it out of a decision.

CASE WHEN is an if, elif, else that runs on every row and hands back one value. in python, `if price < 5: "cheap" elif price < 8: "regular" else: "treat"`, once per row. here it is on the products [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows) of the shop, the imaginary gujarati snack store these notes run on, using [comparisons](./107-comparisons-equal-not-equal-bigger-smaller.md) (tests like price < 5) as the tests:

```sql
SELECT name, price, CASE WHEN price < 5 THEN 'cheap' WHEN price < 8 THEN 'regular' ELSE 'treat' END AS tier FROM products ORDER BY product_id
```

```result
name | price | tier
dhokla | 6.00 | regular
khandvi | 7.50 | regular
jalebi | 5.00 | regular
kaju katli | 12.00 | treat
masala chai | 3.00 | cheap
fafda | 4.50 | cheap
```

the tests run top to bottom and the first true one wins, the rest are skipped. thats why the second one only says price < 8: jalebi at 5.00 already failed price < 5 above it, so there is no need for "between 5 and 8". i expected CASE to look at every branch and pick the best fit, and it just takes the first true one, so the order you write them in is part of the answer.

ELSE is optional. leave it off and a row that matches nothing gets a [null](./031-null.md) (a missing value), not an error:

```sql
SELECT name, CASE WHEN price < 5 THEN 'cheap' END AS tier FROM products ORDER BY product_id
```

```result
name | tier
dhokla | NULL
khandvi | NULL
jalebi | NULL
kaju katli | NULL
masala chai | cheap
fafda | cheap
```

this is how reports turn raw numbers into labels people can group by. it is standard SQL, and the Postgres docs say the same two things, first true wins and no ELSE means null.

### check yourself

1. swap the two tests, so price < 8 comes first. without running it, what tier do masala chai (3.00) and fafda (4.50) get?

```sql
SELECT name, CASE WHEN price < 8 THEN 'regular' WHEN price < 5 THEN 'cheap' ELSE 'treat' END AS tier FROM products WHERE name IN ('masala chai', 'fafda') ORDER BY product_id
```
<details><summary>answer</summary>

```result
name | tier
masala chai | regular
fafda | regular
```

both regular. 3.00 and 4.50 are under 8, so the first test is true and the cheap test is never reached. the tempting answer is cheap, from reading each test on its own instead of in order.

</details>

2. Esha has no city. what does she get from this, local, far or NULL?

```sql
SELECT name, CASE WHEN city = 'Jersey City' THEN 'local' ELSE 'far' END AS area FROM customers WHERE name IN ('Bhavin', 'Esha') ORDER BY customer_id
```
<details><summary>answer</summary>

```result
name | area
Bhavin | far
Esha | far
```

far. her test is unknown ([114](./114-three-valued-logic-true-false-and-unknown.md)), and only a true test wins a branch, so she falls through to ELSE. the tempting answer is NULL, from thinking an unknown test makes the whole result unknown. it also means she is called far with no evidence, so test for the null on purpose if it matters.

</details>

---
prev: [122 computed columns and AS](./122-computed-columns-and-as.md) | next: not written yet
