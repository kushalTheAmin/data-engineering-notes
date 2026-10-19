# 097: junction tables, the table in the middle
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [093 foreign key](./093-foreign-key.md), [095 composite keys](./095-composite-keys.md), [096 why many to many cant live in either table](./096-why-many-to-many-cant-live-in-either-table.md)
section: tables, keys and relationships, part 19, ~2 min read

where does "order 101 has 2 chai" live, if its not a fact about the order and not a fact about chai? in a third table that exists only to hold pairs.

a junction table is a table with one row per pair, and a [foreign key](./093-foreign-key.md) (a column pointing at another tables key) to each side. the shop, the imaginary gujarati snack store, already has one. order_items is it, and its two foreign keys together make its [composite key](./095-composite-keys.md) (a key made of two columns).

```text
orders (order_id)  <--- order_items --->  products (product_id)
                     order_id | product_id | quantity
```

the two arrows are pointer columns, so orders and products never point at each other. the pairs for dhokla (product 1) and for order 101, both in a slice of rows:

```sql
SELECT order_id, product_id, quantity FROM order_items WHERE product_id = 1 OR order_id = 101 ORDER BY order_id, product_id
```

```result
order_id | product_id | quantity
101 | 1 | 2
101 | 5 | 2
104 | 1 | 3
107 | 1 | 1
```

read down product_id 1 and you get dhokla on 101, 104 and 107, 3 orders from 3 rows. read order 101 and you get 2 products from 2 rows. nothing is crammed into a cell, nothing repeats on the big tables.

what surprised me is quantity. i would have guessed it belongs on the product or the order, but 2 dhokla only makes sense for this order, so it sits on the pair. anything that describes the pair goes in the middle table.

this isnt a shop quirk. Django, a python web framework, generates this table for you when you declare a many to many field, and its docs say the generated table carries a uniqueness rule on the two columns.

### check yourself

1. order 106 holds only khandvi. the customer adds 2 kaju katli (product 4). which table gets a new row, and what does this return afterwards?

```sql
SELECT count(*) AS n FROM order_items WHERE order_id = 106
```
<details><summary>answer</summary>

```result
n
1
```

that is the count now. afterwards 2, because order_items gets one new row (106, 4, 2). orders and products dont change. the tempting answer is editing the orders row, but an order cant hold two products in one cell.

</details>

2. a discount applies to dhokla only on order 104. which table holds the discount column, and why not products?
<details><summary>answer</summary>

order_items, on the (104, 1) row. a column on products would discount dhokla on all 3 of its orders. the tempting answer is products because the discount is "about dhokla", but it describes this pair.

</details>

---
prev: [096 why many to many cant live in either table](./096-why-many-to-many-cant-live-in-either-table.md) | next: [098 entity relationship diagrams, boxes and lines](./098-entity-relationship-diagrams.md)
