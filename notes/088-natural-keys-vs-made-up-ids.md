# 088: natural keys vs made up ids
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [087 primary key, one unique id per row](./087-primary-key.md)
section: tables, keys and relationships, part 10, ~2 min read

the customer already has an email, so say nobody else shares it, so why would i invent a number to identify them? i assumed the real thing had to be the better key.

a natural key is a value from the real world that already tells rows apart, like an email. a made up id (a surrogate key) is a value, usually a number handed out by the database, that means nothing outside it. either can be the [primary key](./087-primary-key.md) (a column unique in every row, never NULL, no value). pretend the shop, the imaginary gujarati snack store, tracked orders by email, copied into each order. Asha has orders 101, 103 and 106, then she changes her email:

```python
asha = {"customer_id": 1, "email": "asha@example.com"}
by_email = [{"order_id": 101, "who": "asha@example.com"},
            {"order_id": 103, "who": "asha@example.com"},
            {"order_id": 106, "who": "asha@example.com"}]
by_id = [{"order_id": 101, "who": 1},
         {"order_id": 103, "who": 1},
         {"order_id": 106, "who": 1}]

asha["email"] = "asha.k@example.com"  # she changes it

print("by email:", [o["order_id"] for o in by_email if o["who"] == asha["email"]])
print("by id:", [o["order_id"] for o in by_id if o["who"] == asha["customer_id"]])
```

```output
by email: []
by id: [101, 103, 106]
```

the orders never moved, but what they pointed at changed, so now they point at nobody (a database can also refuse such a change, a later note). a key made of a real world fact breaks when that fact changes. the id says nothing about Asha, so nothing in her life changes it. that meaninglessness felt like cheating to me at first, and its the whole point.

the catch: an id doesnt stop the same person signing up twice, you just get ids 6 and 7 for one email. so keep the email as a UNIQUE NOT NULL column too (unique but not the key), or missing (NULL) emails slip past as in 087. Postgres, a database, has identity columns that hand out the next id for you, per its docs.


### check yourself

1. the shop keys products by product_id. a spelling fix renames product 4, kaju katli. what does this return before and after the rename? it counts the rows of order_items, the shop table of items per order, where product_id is 4.
```sql
SELECT count(*) AS n FROM order_items WHERE product_id = 4
```
<details><summary>answer</summary>

```result
n
2
```

2 both times, only the name column changed. 0 after the rename is the trap, that would happen if items pointed at the name.

</details>

2. a shop keyed customers by phone number. Bhavin leaves but his row stays, and new customer Gita gets his old number. her signup is refused as a duplicate. why, and why is that bad?
<details><summary>answer</summary>

the key matched Bhavins old row, so the database refuses a different person. a real person cant sign up because the real world reused the fact.

</details>

3. the shop makes customer_id the key and email UNIQUE. signups arrive: id 6 with g@example.com, id 7 with g@example.com, id 8 with h@example.com. which get refused?
<details><summary>answer</summary>

only id 7. the key is fine, the email clashes with id 6. id 8 is accepted. the tempting answer is none, since every id is new.

</details>

---
prev: [087 primary key, one unique id per row](./087-primary-key.md) | next: [089 update anomalies](./089-update-anomalies.md)
