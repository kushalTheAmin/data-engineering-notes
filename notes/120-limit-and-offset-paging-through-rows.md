# 120: LIMIT and OFFSET, paging through rows
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [101 SQL, you describe the result, the database figures out how](./101-sql-you-describe-the-result.md), [117 ORDER BY, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md), [118 no ORDER BY, no promised order](./118-no-order-by-no-promised-order.md)
section: asking questions with SQL, part 20, ~2 min read

how does an app show you "page 2" of a long list without loading the whole thing? i guessed it was something clever, and its two small words.

LIMIT says how many rows to return, OFFSET says how many rows to skip first. here is the menu of the shop, the imaginary gujarati snack store these notes run on, priciest first, two rows per page (dhokla is a steamed savory cake, kaju katli and jalebi are sweets, a slice of the products [table](./079-a-table-rows-are-records-columns-are-fields.md)):

```sql
SELECT name, price FROM products ORDER BY price DESC LIMIT 2
```

```result
name | price
kaju katli | 12.00
khandvi | 7.50
```

```sql
SELECT name, price FROM products ORDER BY price DESC LIMIT 2 OFFSET 2
```

```result
name | price
dhokla | 6.00
jalebi | 5.00
```

its the same idea as cutting a python list with a slice, skip two rows and take two. so for pages of two, you skip (page number minus one) times two rows, and OFFSET 4 gives the last page, fafda and masala chai. this OFFSET counts rows to skip, not a clock offset like in [028](./028-time-zone-offsets.md).

the part that surprised me in the Postgres docs (Postgres is a server database): LIMIT without [ORDER BY](./117-order-by-sorting-by-one-or-more-columns.md) gives an unpredictable subset, because rows have [no promised order](./118-no-order-by-no-promised-order.md). page 1 and page 2 could even overlap or miss rows. also the skipped rows still get computed, so per the same docs a huge OFFSET gets slow.

---
prev: [119 where NULLs land when you sort](./119-where-nulls-land-when-you-sort.md) | next: not written yet
