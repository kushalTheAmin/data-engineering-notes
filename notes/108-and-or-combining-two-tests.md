# 108: AND and OR, combining two tests
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [101 SQL, you describe the result, the database figures out how](./101-sql-you-describe-the-result.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [107 comparisons, equal, not equal, bigger, smaller](./107-comparisons-equal-not-equal-bigger-smaller.md)
section: asking questions with SQL, part 8, ~2 min read

i asked the shop for snacks and sweets and got zero rows back, with no error. the english "and" fooled me.

AND and OR glue two [comparisons](./107-comparisons-equal-not-equal-bigger-smaller.md) (a column, a test and a value) into one condition (a test that is true or false per row, unless a value is null) for [WHERE](./106-where-keeping-only-the-rows-that-match.md) (the clause that keeps rows passing a check). AND keeps a row only when both tests are true, OR keeps it when at least one is. the shop, the imaginary gujarati snack store these notes run on, has 6 products in its [table](./079-a-table-rows-are-records-columns-are-fields.md), one row each (dhokla is a steamed savory cake, kaju katli a cashew sweet). here is each against category = 'snack' and price < 6:

| name | snack? | under 6? | AND | OR |
|---|---|---|---|---|
| dhokla | yes | no | no | yes |
| khandvi | yes | no | no | yes |
| jalebi | no | yes | no | yes |
| kaju katli | no | no | no | no |
| masala chai | no | yes | no | yes |
| fafda | yes | yes | yes | yes |

in python terms it is `if row["category"] == "snack" and row["price"] < 6`, one bigger if.

```sql
SELECT name FROM products WHERE category = 'snack' AND price < 6
```

```result
name
fafda
```

swap AND for OR and 5 rows come back, everything except kaju katli. now the trap:

```sql
SELECT name FROM products WHERE category = 'snack' AND category = 'sweet'
```

```result
name
```

in this table one row has one category, so it can never be both. in english "snacks and sweets" means either one, in SQL that is OR.

i kept reading AND as adding more rows, and it can only shrink the answer or leave it the same. OR is the one that grows it.

an empty result with no error is the same quiet failure as the capital D typo in 106, so when your filter returns nothing, an AND is one place to look.

mixing AND and OR in one WHERE has a trap, thats the next one.

---
prev: [107 comparisons, equal, not equal, bigger, smaller](./107-comparisons-equal-not-equal-bigger-smaller.md) | next: [109 parentheses, and AND runs before OR](./109-parentheses-and-runs-before-or.md)
