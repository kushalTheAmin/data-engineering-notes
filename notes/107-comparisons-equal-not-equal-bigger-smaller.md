# 107: comparisons, equal, not equal, bigger, smaller
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [101 SQL, you describe the result, the database figures out how](./101-sql-you-describe-the-result.md), [104 SELECT and FROM, picking columns](./104-select-and-from-picking-columns.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md)
section: asking questions with SQL, part 7, ~2 min read

which products cost at least 6? i assumed one obvious answer, and one character decides whether dhokla is in it.

a comparison is a column, a test and a value, like price >= 6 (price at least 6). it is what [WHERE](./106-where-keeping-only-the-rows-that-match.md) (the clause that keeps rows passing a check) usually runs, written in [SQL](./101-sql-you-describe-the-result.md), the language for asking a database for rows. the shop, the imaginary gujarati snack store these notes run on, has a products [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows). the tests are the same ones python has, with two spelling differences:

| SQL | python | keeps rows where the column is |
|---|---|---|
| = | == | equal to the value |
| <> | != | not equal (DuckDB and Postgres also take !=) |
| > | > | bigger |
| < | < | smaller |
| >= | >= | bigger or equal |
| <= | <= | smaller or equal |

```sql
SELECT name, price FROM products WHERE price >= 6
```

```result
name | price
dhokla | 6.00
khandvi | 7.50
kaju katli | 12.00
```

it is the loop with an if again, `if row["price"] >= 6`, then [SELECT](./104-select-and-from-picking-columns.md) picks the columns and FROM names the table. dhokla (a steamed savory cake) costs exactly 6.00, so it made it in, and kaju katli is a cashew sweet. change one character:

```sql
SELECT name, price FROM products WHERE price > 6
```

```result
name | price
khandvi | 7.50
kaju katli | 12.00
```

dhokla is gone, with no error. the row did not break anything, the line you drew just stopped including it.

i kept feeling that a single = must be assigning something, and in a WHERE it only asks "equal?".

landing exactly on the line is a classic quiet bug. a report of "orders over 100" skips every order of exactly 100 and nobody notices, so decide up front whether the exact value counts.

one caveat: a row where the column is [null](./031-null.md) (a missing value) fails every one of these tests, = and <> included.

---
prev: [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md) | next: [108 AND and OR, combining two tests](./108-and-or-combining-two-tests.md)
