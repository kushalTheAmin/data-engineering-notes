# 099: crows feet, reading one and many on the lines
builds on: [031 null, a marker for a missing value](./031-null.md), [092 relationships, one customer, many orders](./092-relationships-one-customer-many-orders.md), [093 foreign key](./093-foreign-key.md), [098 entity relationship diagrams, boxes and lines](./098-entity-relationship-diagrams.md)
section: tables, keys and relationships, part 21, ~2 min read

the forks and circles on the ends of the lines in an ERD (tables as boxes, joined by lines) look like decoration, but they answer a real question: how many rows can be on the other side?

crows feet is the notation for those end marks, named after the three-pronged fork that means many. in the shop, the imaginary gujarati snack store, customers and orders look like this:

```text
customers ||--------o{ orders
```

you read them by standing on a row and reading the mark at the far end. stand on Asha, look to the orders end: o{ says zero or more orders. stand on order 101, look to the customers end: || says exactly one customer. the four marks, as they look on the left end of a line:

```text
||   exactly one
|o   zero or one
}|   one or more
}o   zero or more
```

on the right end they mirror, so }o becomes o{. each end is a pair, the mark touching the box is the most (bar 1, fork many), the other the least (bar 1, circle 0).

i assumed the circle was decoration, but its the 0, and carries the most information, because Esha, customer 5, has no orders at all and the circle is why thats legal. thats the "many includes 0" of [092](./092-relationships-one-customer-many-orders.md).

the marks describe the design, not rows. orders.customer_id is NOT NULL, so every order must have a customer and the mark is ||. if it allowed [NULL](./031-null.md), the mark would be |o, zero or one customer.

Mermaid, a text-to-diagram tool, draws exactly these marks, and its docs use the same ||--o{ shape.

### check yourself

1. the line from products to order_items has o{ at the order_items end. fafda is product 6. predict this:

```sql
SELECT count(*) AS n FROM order_items WHERE product_id = 6
```
<details><summary>answer</summary>

```result
n
0
```

0, and the diagram still holds because o{ is zero or more. the tempting answer is that the diagram is wrong or fafda must have a row, but the fork allows many and the circle allows none.

</details>

2. the shop adds guest checkout, so orders.customer_id can be NULL. which mark goes at the customers end, || or |o?
<details><summary>answer</summary>

the |o mark, zero or one customer per order. a guest order has none, and no order has two. the tempting answer is o{, but one order still cant have many customers.

</details>

---
prev: [098 entity relationship diagrams, boxes and lines](./098-entity-relationship-diagrams.md) | next: [100 capstone, the whole shop as four connected tables](./100-capstone-the-whole-shop-as-four-connected-tables.md)
