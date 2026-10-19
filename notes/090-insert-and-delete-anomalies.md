# 090: insert and delete anomalies
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [087 primary key, one unique id per row](./087-primary-key.md), [089 update anomalies](./089-update-anomalies.md)
section: tables, keys and relationships, part 12, ~2 min read

Chirag is a customer, but delete his one order and the shop forgets he ever existed. nobody wrote a bad DELETE, the table was shaped wrong.

an insert anomaly is when you cant store one fact until some other fact exists. a delete anomaly is when removing one fact quietly removes another. same setup as [089](./089-update-anomalies.md): one wide [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows) where each row is an order with the customers name and city copied in. the shop, the imaginary gujarati snack store, has 7 orders and 5 customers. the code prints the customer names this table knows:

```python
wide = [
    {"order_id": 101, "name": "Asha",   "city": "Jersey City"},
    {"order_id": 102, "name": "Bhavin", "city": "Edison"},
    {"order_id": 103, "name": "Asha",   "city": "Jersey City"},
    {"order_id": 104, "name": "Chirag", "city": "Jersey City"},
    {"order_id": 105, "name": "Disha",  "city": "Hoboken"},
    {"order_id": 106, "name": "Asha",   "city": "Jersey City"},
    {"order_id": 107, "name": "Bhavin", "city": "Edison"},
]
print(sorted({r["name"] for r in wide}))
wide = [r for r in wide if r["order_id"] != 104]
print(sorted({r["name"] for r in wide}))
```

```output
['Asha', 'Bhavin', 'Chirag', 'Disha']
['Asha', 'Bhavin', 'Disha']
```

the first list has no Esha. she joined in March and sits in the shops separate customers table, but she has no order, so this wide table has no row for her. if it used order_id as its [primary key](./087-primary-key.md) (unique, never NULL), a row with no order id would be refused. to write her down you would have to invent an order. thats the insert anomaly.

the second list is the delete anomaly. 104 was Chirags only order (cancelled in the real shop, deleted here, say by a cleanup), and removing it took his name and city with it. i expected the insert side to be the harmless one, and it fails just as badly.

Wikipedias page on database normalization (storing each fact once) shows the same two failures, with a teacher who cant be recorded until assigned a course.

---
prev: [089 update anomalies](./089-update-anomalies.md) | next: not written yet
