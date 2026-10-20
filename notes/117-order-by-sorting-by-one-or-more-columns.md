# 117: ORDER BY, sorting by one or more columns
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [104 SELECT and FROM, picking columns](./104-select-and-from-picking-columns.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md)
section: asking questions with SQL, part 17, ~2 min read

i want the shop menu grouped by category, and inside each category the priciest item first. one sort, two rules. how do you say that in SQL, the language for asking a database questions?

ORDER BY sorts the rows a query (a question you ask the database) returns, by the column you name, smallest first unless you add DESC (biggest first). name a second column and it only matters when the first one ties. here is the products table of the shop, the imaginary gujarati snack store these notes run on, with 6 rows:

```sql
SELECT name, category, price FROM products ORDER BY category, price DESC
```

```result
name | category | price
masala chai | drink | 3.00
khandvi | snack | 7.50
dhokla | snack | 6.00
fafda | snack | 4.50
kaju katli | sweet | 12.00
jalebi | sweet | 5.00
```

read it as category first, always. drink, snack, sweet, in alphabetical order, and every row of a category sits together. only inside the 3 snacks (khandvi, a rolled chickpea flour snack, dhokla, a steamed savory cake, and fafda, a crunchy chickpea flour snack) does price get a vote, 7.50, 6.00, 4.50, because DESC flips just that column. kaju katli, a cashew sweet, at 12.00 is the priciest product overall but sits fifth, since sweet comes last alphabetically, and category is sorted first. jalebi, a syrupy sweet, follows it.

in python this is a [list of rows](./079-a-table-rows-are-records-columns-are-fields.md) with a sort key that is a pair (the minus sign is the DESC trick, flipping prices so biggest sorts first):

```python
rows = [("khandvi", "snack", 7.5), ("jalebi", "sweet", 5.0), ("dhokla", "snack", 6.0)]
print(sorted(rows, key=lambda r: (r[1], -r[2])))
```

```output
[('khandvi', 'snack', 7.5), ('dhokla', 'snack', 6.0), ('jalebi', 'sweet', 5.0)]
```

i kept assuming a second sort column gets applied to the whole result, and it never does, it only breaks ties left by the first one. ORDER BY runs last, after [WHERE](./106-where-keeping-only-the-rows-that-match.md) has dropped rows and [SELECT](./104-select-and-from-picking-columns.md) has picked columns, so it sorts only what is left.

---
prev: [116 COALESCE, a fallback when a value is NULL](./116-coalesce-a-fallback-when-a-value-is-null.md) | next: not written yet
