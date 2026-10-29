# 254: modeling, deciding the tables before writing them
builds on: [253 capstone, placing an order as one transaction](./253-capstone-placing-an-order-as-one-transaction.md), [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [091 splitting into tables](./091-splitting-into-tables.md), [093 foreign key](./093-foreign-key.md), [097 junction tables, the table in the middle](./097-junction-tables.md)
section: designing tables, part 1, ~2 min read

[253](./253-capstone-placing-an-order-as-one-transaction.md) put Eshas order into tables that already existed. but somebody decided what those tables were before the first CREATE TABLE (the SQL command that makes a table). how do you even start?

modeling is deciding which tables you need and which table each fact belongs in, on paper, before any code. (a table plan, not machine learning.) in [091](./091-splitting-into-tables.md) i cut a wide [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows) apart after copies caused bugs, this goes forward.

say the shop, the imaginary gujarati snack store, wants a receipt for order 101. list its facts and ask of each: what is this a fact about?

| fact on the receipt | a fact about | so it lives in (table.column) |
| --- | --- | --- |
| Asha | a customer | customers.name |
| 2026-04-01 09:15 | an order | orders.ordered_at |
| dhokla | a product | products.name |
| 6.00 | a product | products.price |
| 2 | an order and a product together | order_items.quantity |

four facts have one subject, so that subjects table is the answer. the 2 is the odd one. its not about order 101 alone, since 101 also holds masala chai with its own 2, and not about dhokla alone, since dhokla sits in 3 orders. only the pair has one quantity, so the pair gets a table, the [junction table](./097-junction-tables.md) (a table with one row per pair of things). the [foreign keys](./093-foreign-key.md) (columns pointing at another tables id) then follow: orders keeps a customer id, order_items keeps two ids.

i figured design started with picking column types, but its that one question asked again and again.

one gotcha: with price only in products, old orders are read at todays price, but a receipt wants what it cost that day. a later note copies the price onto each order row on purpose.

---
prev: [253 capstone, placing an order as one transaction](./253-capstone-placing-an-order-as-one-transaction.md) | next: [255 entities and attributes](./255-entities-and-attributes.md)
