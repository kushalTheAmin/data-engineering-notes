# 122: computed columns and AS
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [104 SELECT and FROM, picking columns](./104-select-and-from-picking-columns.md), [105 SELECT star, every column, and why you rarely want it](./105-select-star-every-column.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [117 ORDER BY, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md)
section: asking questions with SQL, part 22, ~2 min read

can a query show a column that isnt in the table? say the shop, the imaginary gujarati snack store these notes run on, wants 1 off every product, and nobody wants to edit the products [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows) to do it (dhokla is a steamed savory cake, kaju katli a cashew sweet, khandvi a rolled gram flour snack, fafda a crunchy chickpea flour snack).

a computed column is an expression (a bit of arithmetic) in the [SELECT](./104-select-and-from-picking-columns.md) list, like `price - 1`, worked out fresh for every row, and AS gives it a name. in python it is building a new dictionary per row with one extra key, `{"name": r["name"], "sale_price": r["price"] - 1}`. first without a name:

```sql
SELECT name, price - 1 FROM products
```

```result
name | (price - 1)
dhokla | 5.00
khandvi | 6.50
jalebi | 4.00
kaju katli | 11.00
masala chai | 2.00
fafda | 3.50
```

the header is just the expression in brackets (DuckDB, the database these notes run in, does that). Postgres, a server database, uses a generated name like ?column? instead. nobody wants to read that, so name it:

```sql
SELECT name, price - 1 AS sale_price FROM products ORDER BY sale_price DESC
```

```result
name | sale_price
kaju katli | 11.00
khandvi | 6.50
dhokla | 5.00
jalebi | 4.00
fafda | 3.50
masala chai | 2.00
```

the name is yours, and [ORDER BY](./117-order-by-sorting-by-one-or-more-columns.md) (sorting the result) can use it. i assumed a new column like this got saved somewhere, and it only exists in that one result. [SELECT *](./105-select-star-every-column.md) (all columns) on products still shows four columns and the old prices.

one gotcha: DuckDB lets [WHERE](./106-where-keeping-only-the-rows-that-match.md) (the row filter) use sale_price too, but the Postgres docs say an output name works in ORDER BY, not in WHERE, there you write `price - 1` again. so if you move databases, that query breaks.

---
prev: [121 DISTINCT, removing duplicate rows](./121-distinct-removing-duplicate-rows.md) | next: not written yet
