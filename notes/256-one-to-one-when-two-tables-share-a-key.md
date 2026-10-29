# 256: one to one, when two tables share a key
builds on: [255 entities and attributes](./255-entities-and-attributes.md), [092 relationships, one customer, many orders](./092-relationships-one-customer-many-orders.md), [093 foreign key](./093-foreign-key.md), [087 primary key, one unique id per row](./087-primary-key.md), [159 left join, keep every row from the left table](./159-left-join-keep-every-row-from-the-left-table.md), [031 null, a marker meaning there is no value](./031-null.md)
section: designing tables, part 3, ~2 min read

why would you build a second table with at most one row per customer, when a column would do? and what stops it sneaking up to two?

in [255](./255-entities-and-attributes.md) city would get its own table because customers share one. this is the opposite: one to one, a row matching at most one row there, where [092](./092-relationships-one-customer-many-orders.md) had one row matching a pile.

in the shop, the imaginary gujarati snack store, phone numbers are optional, so they live in customer_contacts. its [primary key](./087-primary-key.md) (a column unique in every row) is the customer id, which is also a [foreign key](./093-foreign-key.md) (a column pointing at another tables id) back to customers.

```sql
SELECT c.name, k.phone
FROM customers c
LEFT JOIN customer_contacts k ON k.customer_id = c.customer_id
ORDER BY c.customer_id
```

```result
name | phone
Asha | 555-0101
Bhavin | 555-0102
Chirag | NULL
Disha | 555-0104
Esha | NULL
```

a [left join](./159-left-join-keep-every-row-from-the-left-table.md) (keep every left row, fill gaps) gives 5 rows for 5 customers. Chirag and Esha shared no number, so the join fills in [NULL](./031-null.md) (no value). left joining customers to orders instead gives 8 rows, Asha repeats 3 times. a one to one join cant multiply rows.

what stops it is the key being unique. orders.customer_id isnt, so Asha gets a pile there.

```sql
-- fails on purpose
INSERT INTO customer_contacts VALUES (1, '555-0199')
```

DuckDB, the database these notes run, answers duplicate key, violates primary key constraint. i read one to one as a perfect pairing, but 2 of 5 customers have no partner. its at most one, the same way one to many in 092 could mean zero.

Django, a python web framework, has OneToOneField, which its docs call similar to a unique foreign key. a sometimes-NULL column is often fine, so split when most rows would be empty.

---
prev: [255 entities and attributes](./255-entities-and-attributes.md) | next: not written yet
