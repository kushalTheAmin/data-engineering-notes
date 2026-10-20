# 104: SELECT and FROM, picking columns
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [101 SQL, you describe the result, the database figures out how](./101-sql-you-describe-the-result.md), [103 your first query against the shop](./103-your-first-query-against-the-shop.md)
section: asking questions with SQL, part 4, ~2 min read

swap two words after SELECT and the whole answer comes back flipped. so what do the two keywords in a [query](./101-sql-you-describe-the-result.md) (one request to a database) really control?

FROM names the table to read, SELECT names the columns to keep, in the order you write them. the shop, the imaginary gujarati snack store these notes run on, has a products [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows) with four columns. here is a slice of it:

| product_id | name | category | price |
|---|---|---|---|
| 1 | dhokla | snack | 6.00 |
| 2 | khandvi | snack | 7.50 |
| 3 | jalebi | sweet | 5.00 |

and this query, the [first one](./103-your-first-query-against-the-shop.md) with the columns flipped:

```sql
SELECT price, name FROM products
```

```result
price | name
6.00 | dhokla
7.50 | khandvi
5.00 | jalebi
12.00 | kaju katli
3.00 | masala chai
4.50 | fafda
```

in python terms, for every row dictionary you build a new one with only the keys you listed, in that order. product_id and category never make it out. the table itself is untouched, the query only decides what you see. (dhokla is a steamed savory cake, khandvi a rolled gram flour snack, jalebi a syrupy sweet, kaju katli a cashew sweet, masala chai spiced tea, fafda a crunchy chickpea flour snack.)

now the part i got wrong. i assumed picking one column would give me the distinct values:

```sql
SELECT category FROM products
```

```result
category
snack
snack
sweet
sweet
drink
snack
```

nope. you get one result row per table row, six, with snack three times. a plain SELECT list keeps or drops columns, it never drops rows (WHERE does that), so if you only want each category once you need something else, and a later note covers it.

this is the usual first surprise when someone asks "what categories do we sell" and gets a wall of repeats.

---
prev: [103 your first query against the shop](./103-your-first-query-against-the-shop.md) | next: not written yet
