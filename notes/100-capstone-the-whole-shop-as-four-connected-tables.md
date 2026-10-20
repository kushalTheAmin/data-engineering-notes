# 100: capstone, the whole shop as four connected tables
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [080 every column holds one type](./080-every-column-holds-one-type.md), [081 why a shared spreadsheet breaks when many people use it](./081-why-a-shared-spreadsheet-breaks.md), [082 a database, a program that guards your data](./082-a-database-guards-the-data.md), [083 schema on write vs schema on read](./083-schema-on-write-vs-schema-on-read.md), [084 a network, computers sending bytes to each other](./084-a-network.md), [085 addresses and ports, the right program on the right machine](./085-addresses-and-ports.md), [086 client and server, you ask, the database answers](./086-client-and-server.md), [087 primary key, one unique id per row](./087-primary-key.md), [088 natural keys vs made up ids](./088-natural-keys-vs-made-up-ids.md), [089 update anomalies](./089-update-anomalies.md), [090 insert and delete anomalies](./090-insert-and-delete-anomalies.md), [091 splitting into tables, each fact lives in one place](./091-splitting-into-tables.md), [092 relationships, one customer, many orders](./092-relationships-one-customer-many-orders.md), [093 foreign key](./093-foreign-key.md), [094 what a foreign key stops, rows pointing at nothing](./094-what-a-foreign-key-stops.md), [095 composite keys, a key made of two columns](./095-composite-keys.md), [096 why many to many cant live in either table](./096-why-many-to-many-cant-live-in-either-table.md), [097 junction tables, the table in the middle](./097-junction-tables.md), [098 entity relationship diagrams, boxes and lines](./098-entity-relationship-diagrams.md), [099 crows feet, reading one and many on the lines](./099-crows-feet-reading-one-and-many.md)
section: tables, keys and relationships, wrap up, ~3 min read

can you draw the whole shop from memory, which tables exist and what points at what? by now you can, and it fits in four lines of text.

the shop is the imaginary gujarati snack store these notes run on. it ends this section as four [tables](./079-a-table-rows-are-records-columns-are-fields.md) (grids of rows), drawn the way [098](./098-entity-relationship-diagrams.md) and [099](./099-crows-feet-reading-one-and-many.md) showed, with PK for primary key and FK for [foreign key](./093-foreign-key.md) (a column pointing at another tables key):

```text
customers ||--o{ orders ||--o{ order_items }o--|| products

customers          orders             order_items          products
customer_id PK     order_id PK        order_id PK FK       product_id PK
name               customer_id FK     product_id PK FK     name
city               ordered_at         quantity             category
joined_on          status                                  price
```

and the real rows behind it:

```sql
SELECT (SELECT count(*) FROM customers) AS customers, (SELECT count(*) FROM orders) AS orders, (SELECT count(*) FROM order_items) AS order_items, (SELECT count(*) FROM products) AS products
```

```result
customers | orders | order_items | products
5 | 7 | 13 | 6
```

every note here fixed one way the last shape broke:

| what broke | the fix | notes |
|---|---|---|
| a spot for a missing value, mixed types | table, one type per column | [079](./079-a-table-rows-are-records-columns-are-fields.md) [080](./080-every-column-holds-one-type.md) |
| two saves, one lost | a database guarding the data | [081](./081-why-a-shared-spreadsheet-breaks.md) [082](./082-a-database-guards-the-data.md) [083](./083-schema-on-write-vs-schema-on-read.md) |
| the data is on another machine | network, address, client and server | [084](./084-a-network.md) [085](./085-addresses-and-ports.md) [086](./086-client-and-server.md) |
| which row is which | primary key, made up ids | [087](./087-primary-key.md) [088](./088-natural-keys-vs-made-up-ids.md) |
| a fact copied, drifting, lost | anomalies, then splitting | [089](./089-update-anomalies.md) [090](./090-insert-and-delete-anomalies.md) [091](./091-splitting-into-tables.md) |
| pieces must find each other | relationship, foreign key | [092](./092-relationships-one-customer-many-orders.md) [093](./093-foreign-key.md) [094](./094-what-a-foreign-key-stops.md) |
| many to many | composite key, junction table | [095](./095-composite-keys.md) [096](./096-why-many-to-many-cant-live-in-either-table.md) [097](./097-junction-tables.md) |
| show it fast | diagram, marks | [098](./098-entity-relationship-diagrams.md) [099](./099-crows-feet-reading-one-and-many.md) |

i expected a pile of machinery, and what surprised me is how little there is. one kind of pointer column plus one extra table did all the connecting, and the rest are rules that keep it honest.

one gotcha: the diagram says an order has zero or more items, and nothing in the shop forces an order to have any. a bare order row is legal. Esha with no orders and fafda on no item are the same circle at work.

the next section stops drawing these tables and starts asking them questions.

### check yourself

1. the shop wants to store which products a customer marked as a favorite. what new table, and what is its key?
<details><summary>answer</summary>

favorites, with customer_id and product_id, each a foreign key, together the primary key. its many to many, so it needs a junction table. the tempting answer is a favorite column on customers, which holds only one product.

</details>

2. Chirag cancelled order 104. predict this:

```sql
SELECT count(*) AS n FROM order_items WHERE order_id = 104
```
<details><summary>answer</summary>

```result
n
1
```

one row. cancelled is just a status value on the orders row, and its item row stays. the tempting answer is 0, from assuming a cancelled order loses its items.

</details>

---
prev: [099 crows feet, reading one and many on the lines](./099-crows-feet-reading-one-and-many.md) | next: not written yet
