# 136: capstone, one query traced clause by clause
builds on: [101 SQL, you describe the result, the database figures out how](./101-sql-you-describe-the-result.md), [102 a database in one file, setting up DuckDB](./102-a-database-in-one-file.md), [103 your first query against the shop](./103-your-first-query-against-the-shop.md), [104 SELECT and FROM, picking columns](./104-select-and-from-picking-columns.md), [105 SELECT star, every column, and why you rarely want it](./105-select-star-every-column.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [107 comparisons, equal, not equal, bigger, smaller](./107-comparisons-equal-not-equal-bigger-smaller.md), [108 AND and OR, combining two tests](./108-and-or-combining-two-tests.md), [109 parentheses, and AND runs before OR](./109-parentheses-and-runs-before-or.md), [110 NOT, flipping a condition](./110-not-flipping-a-condition.md), [111 IN, matching against a list](./111-in-matching-against-a-list.md), [112 BETWEEN, ranges that include both ends](./112-between-ranges-that-include-both-ends.md), [113 LIKE, matching text patterns](./113-like-matching-text-patterns.md), [114 three valued logic, true, false and unknown](./114-three-valued-logic-true-false-and-unknown.md), [115 IS NULL and IS NOT NULL](./115-is-null-and-is-not-null.md), [116 COALESCE, a fallback when a value is NULL](./116-coalesce-a-fallback-when-a-value-is-null.md), [117 ORDER BY, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md), [118 no ORDER BY, no promised order](./118-no-order-by-no-promised-order.md), [119 where NULLs land when you sort](./119-where-nulls-land-when-you-sort.md), [120 LIMIT and OFFSET, paging through rows](./120-limit-and-offset-paging-through-rows.md), [121 DISTINCT, removing duplicate rows](./121-distinct-removing-duplicate-rows.md), [122 computed columns and AS](./122-computed-columns-and-as.md), [123 CASE WHEN, if and else inside a query](./123-case-when-if-and-else-inside-a-query.md), [124 text functions, lower, upper, length and trim](./124-text-functions-lower-upper-length-and-trim.md), [125 concatenating text, and taking pieces of it](./125-concatenating-text-and-taking-pieces-of-it.md), [126 date parts, pulling out the year, month and day](./126-date-parts-pulling-out-the-year-month-and-day.md), [127 truncating timestamps to a day or a month](./127-truncating-timestamps-to-a-day-or-a-month.md), [128 adding and subtracting intervals](./128-adding-and-subtracting-intervals.md), [129 the difference between two dates](./129-the-difference-between-two-dates.md), [130 NULLIF and dividing by zero](./130-nullif-and-dividing-by-zero.md), [131 integer division, when 7 / 2 gives 3](./131-integer-division-when-7-divided-by-2-gives-3.md), [132 CAST, changing a values type](./132-cast-changing-a-values-type.md), [133 casts that fail, and TRY_CAST](./133-casts-that-fail-and-try-cast.md), [134 the order SQL really runs in](./134-the-order-sql-really-runs-in.md), [135 one language, many dialects](./135-one-language-many-dialects.md)
section: asking questions with SQL, wrap up, ~3 min read

this one query on the shop uses most of this section. can you say which 3 rows come back before running it?

the shop is the imaginary gujarati snack store these notes run on. a clause is one keyword plus its piece of a query, and [134](./134-the-order-sql-really-runs-in.md) showed they run in a fixed order whatever order you type them: FROM, WHERE, SELECT, ORDER BY, LIMIT. the middle numbers are the notes that built each clause, the right column is how many rows are left after it:

```sql
SELECT name, category, price FROM products
```

```result
name | category | price
dhokla | snack | 6.00
khandvi | snack | 7.50
jalebi | sweet | 5.00
kaju katli | sweet | 12.00
masala chai | drink | 3.00
fafda | snack | 4.50
```

those are the 6 rows it starts from, and these are the steps:

```text
FROM products      104            6 rows
WHERE              106 to 113     4 rows
SELECT             104 122 123    4 rows
ORDER BY           117            4 rows
LIMIT              120            3 rows
```

```sql
SELECT name, price - 1 AS sale_price, CASE WHEN price < 5 THEN 'cheap' WHEN price < 8 THEN 'regular' ELSE 'treat' END AS tier FROM products WHERE category IN ('snack', 'sweet') AND price >= 5 ORDER BY sale_price DESC LIMIT 3
```

```result
name | sale_price | tier
kaju katli | 11.00 | treat
khandvi | 6.50 | regular
dhokla | 5.00 | regular
```

WHERE comes right after FROM and drops masala chai, a drink, with [IN](./111-in-matching-against-a-list.md) (matching a list), and fafda, a crunchy chickpea flour snack, at 4.50 with a [comparison](./107-comparisons-equal-not-equal-bigger-smaller.md) (a column, a test, a value). SELECT then builds [sale_price](./122-computed-columns-and-as.md) (a named computed column) and a [CASE WHEN](./123-case-when-if-and-else-inside-a-query.md) tier (an if inside a query) for the 4 survivors. ORDER BY sorts on the new name, DESC meaning biggest first, and LIMIT cuts to 3, so jalebi, a syrupy sweet, falls off the end. (dhokla is a steamed savory cake, khandvi a rolled chickpea snack, kaju katli a cashew sweet.)

i expected a query this long to be hard to follow, and traced it is 5 small steps. each clause works on the rows the one before left. when a query returns something odd, delete clauses from the bottom up and count rows after each one.

here is the whole section on one map:

| job | notes |
|---|---|
| ask and set up | [101](./101-sql-you-describe-the-result.md) [102](./102-a-database-in-one-file.md) [103](./103-your-first-query-against-the-shop.md) |
| pick columns | [104](./104-select-and-from-picking-columns.md) [105](./105-select-star-every-column.md) |
| keep rows | [106](./106-where-keeping-only-the-rows-that-match.md) [107](./107-comparisons-equal-not-equal-bigger-smaller.md) [108](./108-and-or-combining-two-tests.md) [109](./109-parentheses-and-runs-before-or.md) [110](./110-not-flipping-a-condition.md) [111](./111-in-matching-against-a-list.md) [112](./112-between-ranges-that-include-both-ends.md) [113](./113-like-matching-text-patterns.md) |
| unknown values | [114](./114-three-valued-logic-true-false-and-unknown.md) [115](./115-is-null-and-is-not-null.md) [116](./116-coalesce-a-fallback-when-a-value-is-null.md) |
| sort and cut | [117](./117-order-by-sorting-by-one-or-more-columns.md) [118](./118-no-order-by-no-promised-order.md) [119](./119-where-nulls-land-when-you-sort.md) [120](./120-limit-and-offset-paging-through-rows.md) |
| drop repeats | [121](./121-distinct-removing-duplicate-rows.md) |
| build columns | [122](./122-computed-columns-and-as.md) [123](./123-case-when-if-and-else-inside-a-query.md) [124](./124-text-functions-lower-upper-length-and-trim.md) [125](./125-concatenating-text-and-taking-pieces-of-it.md) [126](./126-date-parts-pulling-out-the-year-month-and-day.md) [127](./127-truncating-timestamps-to-a-day-or-a-month.md) [128](./128-adding-and-subtracting-intervals.md) [129](./129-the-difference-between-two-dates.md) [130](./130-nullif-and-dividing-by-zero.md) [131](./131-integer-division-when-7-divided-by-2-gives-3.md) [132](./132-cast-changing-a-values-type.md) [133](./133-casts-that-fail-and-try-cast.md) |
| order and dialects | [134](./134-the-order-sql-really-runs-in.md) [135](./135-one-language-many-dialects.md) |

the next section turns many rows into a few numbers, and adds a step between WHERE and SELECT.

### check yourself

1. without running it, which 2 names come back, and why not only kaju katli?

```sql
SELECT name FROM products WHERE category = 'snack' OR category = 'sweet' AND price >= 10 ORDER BY price LIMIT 2
```
<details><summary>answer</summary>

```result
name
fafda
dhokla
```

AND goes first, so WHERE keeps every snack plus sweets at 10 or more: fafda, dhokla, khandvi and kaju katli. ORDER BY price then LIMIT 2 takes the 2 cheapest, fafda 4.50 and dhokla 6.00. kaju katli alone is the tempting answer, from grouping it as (snack or sweet) and 10 or more.

</details>

2. the traced query ran in DuckDB. a teammate adds `AND sale_price > 5` to the WHERE and moves it to Postgres, a server database. what happens, and what do they write instead?
<details><summary>answer</summary>

an error. WHERE runs before SELECT, so sale_price does not exist yet there in Postgres (DuckDB is friendlier). they write the expression out again. on a simpler query that is:

```sql
SELECT name FROM products WHERE price - 1 > 5 ORDER BY product_id
```

```result
name
khandvi
kaju katli
```

the tempting answer is that it works, because ORDER BY accepts the same name.

</details>

---
prev: [135 one language, many dialects](./135-one-language-many-dialects.md) | next: [137 aggregate functions, many rows in, one value out](./137-aggregate-functions-many-rows-in-one-value-out.md)
