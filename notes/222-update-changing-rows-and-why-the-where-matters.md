# 222: UPDATE, changing rows and why the WHERE matters
builds on: [220 INSERT, adding rows and matching values to columns](./220-insert-adding-rows-and-matching-values-to-columns.md), [221 INSERT from a SELECT, copying rows from a query](./221-insert-from-a-select-copying-rows-from-a-query.md), [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [138 count star vs count of a column](./138-count-star-vs-count-of-a-column.md)
section: changing data safely, part 15, ~2 min read

i meant to cancel one order, forgot a single line, and all 7 orders now say cancelled. which line? you could do it too, its one short line.

UPDATE changes values in rows that already exist, where [INSERT](./220-insert-adding-rows-and-matching-values-to-columns.md) adds new ones. SET names the column and its new value, and the [WHERE](./106-where-keeping-only-the-rows-that-match.md) (keeps only matching rows) picks which rows get it. the shop, the imaginary gujarati snack store, keeps 7 orders in a [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows). in DuckDB (a database that runs inside your script), where SELECT shows rows and ORDER BY sorts them, a slice:

```sql
UPDATE orders SET status = 'cancelled' WHERE order_id = 106;
SELECT order_id, status FROM orders WHERE order_id >= 105 ORDER BY order_id
```

```result
order_id | status
105 | delivered
106 | cancelled
107 | delivered
```

now the same UPDATE with the WHERE forgotten. count(*) [counts rows](./138-count-star-vs-count-of-a-column.md):

```sql
UPDATE orders SET status = 'cancelled';
SELECT count(*) AS cancelled FROM orders WHERE status = 'cancelled'
```

```result
cancelled
7
```

i assumed a missing WHERE would be an error, the database asking which rows, but it just means all of them. the old values are gone, no warning.

the other slip is quiet too: a WHERE that matches nothing changes 0 rows, and Postgres docs say thats not an error. SET can read the old value, so price = price + 1 adds 1 to whatever was there.

so what: this is a classic way to wreck a live table. MySQL, another database, has a safety option, --safe-updates (also --i-am-a-dummy), that refuses an UPDATE unless its WHERE uses a key column like the id, or it has a LIMIT. Postgres, a server database, takes the same statement.

### check yourself

1. jalebi costs 5.00 and kaju katli 12.00. a script that retries on failure runs this price rise twice. what do they cost afterwards?

```sql
UPDATE products SET price = price + 1 WHERE category = 'sweet';
UPDATE products SET price = price + 1 WHERE category = 'sweet';
SELECT name, price FROM products WHERE category = 'sweet' ORDER BY product_id
```

<details><summary>answer</summary>

```result
name | price
jalebi | 7.00
kaju katli | 14.00
```

each run reads the price as it is now, so two runs add 2. the tempting answer is 6.00 and 13.00, as if the database remembered the first run, but nothing does.

</details>

2. jalebi and kaju katli are sweets, masala chai is the only drink. the two lines below are the same, the second run by mistake. how many products are sweets afterwards, and does the second line error?

```sql
UPDATE products SET category = 'sweet' WHERE category = 'drink';
UPDATE products SET category = 'sweet' WHERE category = 'drink';
SELECT count(*) AS sweets FROM products WHERE category = 'sweet'
```

<details><summary>answer</summary>

```result
sweets
3
```

jalebi and kaju katli were sweets, and the first line turns masala chai into one. the second finds no drink, so it changes 0 rows and raises no error. a WHERE that tests the thing you change is safe to repeat, unlike price + 1.

</details>

---
prev: [221 INSERT from a SELECT, copying rows from a query](./221-insert-from-a-select-copying-rows-from-a-query.md) | next: not written yet
