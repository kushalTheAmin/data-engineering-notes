# 095: composite keys, a key made of two columns
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [087 primary key, one unique id per row](./087-primary-key.md), [093 foreign key](./093-foreign-key.md), [094 what a foreign key stops](./094-what-a-foreign-key-stops.md)
section: tables, keys and relationships, part 17, ~2 min read

which column is the primary key of order_items? i went looking and neither one works, order_id repeats and so does product_id.

in [094](./094-what-a-foreign-key-stops.md) i said the file that builds the shop uses a key of two columns here, and this is that. a composite key is a [primary key](./087-primary-key.md) (unique in every row, never NULL, meaning no value) made of two or more columns together, so only the combination has to be new. order_items is the table of the shop, the imaginary gujarati snack store, with one [row](./079-a-table-rows-are-records-columns-are-fields.md) per product on each order. a slice:

```sql
SELECT order_id, product_id, quantity FROM order_items WHERE order_id IN (101, 103) ORDER BY order_id, product_id
```

```result
order_id | product_id | quantity
101 | 1 | 2
101 | 5 | 2
103 | 2 | 1
103 | 5 | 1
```

101 appears twice and product 5 (masala chai) appears twice here, nobody minds. the pair is what the key watches, and no pair repeats. try adding chai to order 103 again, with a quantity of 9:

```sql
-- fails on purpose
INSERT INTO order_items VALUES (103, 5, 9)
```

DuckDB, the database these notes run, refuses it, saying duplicate key, violates the primary key constraint (the rule broken). quantity isnt in the key, so it doesnt help. the file that builds the shop declares it as PRIMARY KEY (order_id, product_id), and Postgres reads that the same.

i assumed every table needed one id column of its own, and you can see this one gets by with none. both columns are also [foreign keys](./093-foreign-key.md) (columns that point at another tables key), one at orders and one at products, so the key is built out of two pointers. without it an insert sent twice by accident could put chai on order 103 twice and every total would quietly be off.

### check yourself

1. order 106 holds only khandvi, product 2. you insert order 106 with product 1 (dhokla), both ids already exist in other rows. accepted or refused?

```sql
SELECT count(*) AS n FROM order_items WHERE order_id = 106 AND product_id = 1
```
<details><summary>answer</summary>

```result
n
0
```

accepted. the pair (106, 1) is new, and thats all the key checks. the tempting refused comes from seeing 106 and 1 each used elsewhere, but the key never looks at one column alone.

</details>

2. someone changes the key to (order_id, product_id, quantity). what can the table now hold that it couldnt before?
<details><summary>answer</summary>

order 103 with product 5 twice, once with quantity 1 and once with 9, because the triple is different. the key now accepts the very repeat it was meant to stop. the tempting answer is that a bigger key is stricter, but every column added makes a repeat easier to avoid.

</details>

---
prev: [094 what a foreign key stops](./094-what-a-foreign-key-stops.md) | next: not written yet
