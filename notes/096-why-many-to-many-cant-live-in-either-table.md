# 096: why many to many cant live in either table
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [087 primary key, one unique id per row](./087-primary-key.md), [089 update anomalies](./089-update-anomalies.md), [092 relationships, one customer, many orders](./092-relationships-one-customer-many-orders.md), [095 composite keys](./095-composite-keys.md)
section: tables, keys and relationships, part 18, ~2 min read

order 101 has dhokla and masala chai on it. so which product_id goes in its row in the orders table? i tried both answers and neither fits.

a many to many relationship is when rows on each side can match many rows on the other. in the shop, the imaginary gujarati snack store, an order holds many products, and a product lands on many orders. (dhokla is a steamed savory cake, kaju katli a cashew fudge, jalebi a fried sweet.) in [092](./092-relationships-one-customer-many-orders.md) the pointer went on the many side, so one [table](./079-a-table-rows-are-records-columns-are-fields.md) cell holds one value. here both sides are many. tried both ways:

```text
pointer in orders             pointer in products
order 101 -> dhokla           dhokla      -> 101, 104, 107
             masala chai      masala chai -> 101, 103, 105
order 105 -> kaju katli
             jalebi           3 order ids in one cell
             masala chai      for each of them
3 products in one cell
```

you could repeat the row instead, once per product, but then order_id repeats, and the [primary key](./087-primary-key.md) (a unique id per row) refuses it. and even if it let it through, the customer and time would be copied onto every repeat, the same [update anomaly](./089-update-anomalies.md) as the wide table.

i kept hunting for which side the pointer belongs on, and the honest answer is neither. the relationship isnt a fact about an order or about a product, its a fact about the pair, like "order 101 has chai". and a pair is something [095](./095-composite-keys.md) already showed a key made of.

the shop already holds those pairs, 13 rows of them in order_items. Entity Framework Core, a .NET database library, says it in its docs too, a foreign key alone cant show many to many, it needs an extra table. the next note builds that table.

---
prev: [095 composite keys](./095-composite-keys.md) | next: [097 junction tables](./097-junction-tables.md)
