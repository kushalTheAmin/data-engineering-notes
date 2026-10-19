# 098: entity relationship diagrams, boxes and lines
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [087 primary key, one unique id per row](./087-primary-key.md), [093 foreign key](./093-foreign-key.md), [097 junction tables, the table in the middle](./097-junction-tables.md)
section: tables, keys and relationships, part 20, ~2 min read

how would you show a teammate how your tables connect in 5 seconds, without a single row of data? you draw an entity relationship diagram, ERD for short.

an ERD is a picture with one box per [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows) and one line per relationship. an entity is just a kind of thing you keep facts about, so each one becomes a table. here are two tables of the shop, the imaginary gujarati snack store:

```text
 customers                     orders
+----------------------+      +--------------------------+
| customer_id   PK     |      | order_id      PK         |
| name                 |------| customer_id   FK         |
|                      |places| ordered_at               |
+----------------------+      +--------------------------+
```

each box lists its columns. PK marks the [primary key](./087-primary-key.md) (the unique id column) and FK marks a [foreign key](./093-foreign-key.md) (a column pointing at another tables key). the line joins the two tables, and it goes exactly where the FK is, from orders.customer_id to customers.customer_id. the word on it, places, says what the link means: a customer places orders.

what clicked for me is that nothing in this picture is data. no Asha, no 101. its the shape of the database. i expected a diagram to show the data, and it lets you read the design before you ever see a row. the little marks on the line ends say how many, and that gets its own note.

for the junction table from [097](./097-junction-tables.md), you just draw another box with two lines coming out of it. pgAdmin, the admin tool for Postgres, can generate one for an existing database, so you rarely draw it from scratch.

### check yourself

1. in the shop, order_items has foreign keys to orders and to products. how many lines touch the order_items box, and which columns do they come from?
<details><summary>answer</summary>

2 lines, one from order_items.order_id to orders and one from order_items.product_id to products. one line per foreign key. the tempting answer is 1 line to "the order", because a line is easy to read as "belongs to", but each foreign key gets its own line.

</details>

2. a teammate says the ERD shows Asha has 3 orders. do they have it right?
<details><summary>answer</summary>

no. the ERD only shows that a customer can place orders, the shape. the 3 for Asha is a row count you get by querying orders. the tempting yes comes from thinking a diagram holds the data, but boxes list columns, never rows.

</details>

---
prev: [097 junction tables, the table in the middle](./097-junction-tables.md) | next: not written yet
