# 091: splitting into tables, each fact lives in one place
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [088 natural keys vs made up ids](./088-natural-keys-vs-made-up-ids.md), [089 update anomalies](./089-update-anomalies.md), [090 insert and delete anomalies](./090-insert-and-delete-anomalies.md)
section: tables, keys and relationships, part 13, ~2 min read

so where should Ashas city live? the last two notes ([089](./089-update-anomalies.md) and [090](./090-insert-and-delete-anomalies.md)) all came from copying it onto every order row, and the fix is one cut.

splitting into tables means each kind of thing gets its own [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows), and other tables keep only its id. the shop, the imaginary gujarati snack store, is already built this way. before, a slice of the wide table:

| order_id | name | city |
|---|---|---|
| 101 | Asha | Jersey City |
| 103 | Asha | Jersey City |
| 106 | Asha | Jersey City |

after, all 5 customers, and a slice of the 7 orders:

| customer_id | name | city |
|---|---|---|
| 1 | Asha | Jersey City |
| 2 | Bhavin | Edison |
| 3 | Chirag | Jersey City |
| 4 | Disha | Hoboken |
| 5 | Esha | NULL |

| order_id | customer_id |
|---|---|
| 101 | 1 |
| 103 | 1 |
| 104 | 3 |
| 106 | 1 |

Ashas name and city are written once now. her orders carry only 1, the [made up id](./088-natural-keys-vs-made-up-ids.md) that means nothing and never changes. so all three anomalies shrink:

- update: change the city on customer 1 and all 3 orders follow, they only hold the 1
- insert: Esha has her row with no order
- delete: remove order 104 and Chirags row in customers stays

across the shop, the wide table wrote a city 7 times, one per order. the split writes it 4 times, once per customer who has one. i expected splitting to need something clever, and it was just stop copying and leave a pointer.

the cost is that an order no longer shows a name by itself, you look up id 1 in the other table. that lookup is called a join, a later note covers it, and first the pointer column needs a proper name.

---
prev: [090 insert and delete anomalies](./090-insert-and-delete-anomalies.md) | next: [092 relationships, one customer, many orders](./092-relationships-one-customer-many-orders.md)
