# 092: relationships, one customer, many orders
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [087 primary key, one unique id per row](./087-primary-key.md), [091 splitting into tables](./091-splitting-into-tables.md)
section: tables, keys and relationships, part 14, ~2 min read

if Asha has 3 orders, does that make her 3 customers? no, and the way the shop tells them apart is called a relationship.

a relationship is how rows in one [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows) connect to rows in another. a common one is one to many: one row on one side matches many rows on the other. in the shop, the imaginary gujarati snack store, one customer has many orders, and after the [split](./091-splitting-into-tables.md) (a table per kind of thing) each order holds its customers id. all 5 customers and all 7 orders:

```text
customers (one)        orders (many)
1 Asha     ------->    101, 103, 106     3 orders
2 Bhavin   ------->    102, 107          2 orders
3 Chirag   ------->    104               1 order
4 Disha    ------->    105               1 order
5 Esha     ------->    (none)            0 orders
```

read it left to right and each customer has a pile. read it right to left and every order has exactly one customer. 3 + 2 + 1 + 1 + 0 is 7, so each order sits in exactly one pile.

this tells you where the pointer goes. an order has one customer, so one customer_id per row fits in a single cell. the customers table would need a whole list of order ids in one cell, growing every time Asha buys something. so the pointer lives on the many side.

the part i kept missing is that "many" includes 0 and 1. Esha is still one to many, her pile is just empty. the shape is a rule about what is allowed, not a count of what exists right now.

the column holding the pointer needs its own name, which the next note gives it.

---
prev: [091 splitting into tables](./091-splitting-into-tables.md) | next: [093 foreign key](./093-foreign-key.md)
