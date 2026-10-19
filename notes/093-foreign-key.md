# 093: foreign key, a column that points at another tables key
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [087 primary key, one unique id per row](./087-primary-key.md), [092 relationships, one customer, many orders](./092-relationships-one-customer-many-orders.md)
section: tables, keys and relationships, part 15, ~2 min read

order 104 has a 3 in its customer_id column. 3 what? on its own its just a number, and what makes it mean Chirag is a foreign key.

a foreign key is a column in one [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid where each row is one record) that usually holds values of another tables [primary key](./087-primary-key.md) (the column with a unique id per row). in the shop, the imaginary gujarati snack store, orders.customer_id is one. its the pointer column from [092](./092-relationships-one-customer-many-orders.md), the one on the orders side because one customer has many orders. a slice of the orders:

```sql
SELECT order_id, customer_id FROM orders WHERE order_id IN (101, 103, 104) ORDER BY order_id
```

```result
order_id | customer_id
101 | 1
103 | 1
104 | 3
```

now take those values to the customers table and look them up:

```sql
SELECT customer_id, name FROM customers WHERE customer_id IN (1, 3) ORDER BY customer_id
```

```result
customer_id | name
1 | Asha
3 | Chirag
```

so 104 is Chirags order. notice 1 shows up twice in the first result. thats fine, only orders primary key, order_id, has to be unique. a foreign key repeating is the whole point, one customer with many orders.

i assumed the numbers themselves said they were pointers, but they dont. the file that builds the shop declares it when the table is created, with REFERENCES customers (customer_id), a SQL phrase that tells the database where the column points. if you leave that phrase out its a plain integer column and the database has no idea it means anything. what that buys you is its own note.

in .NET (microsofts dev platform), Entity Framework Core guesses this from naming alone: a property called CustomerId next to a Customer property is treated as a foreign key to Customer.

### check yourself

1. customers has exactly one row with customer_id 1. so how many rows does this return, 1 or more?

```sql
SELECT order_id FROM orders WHERE customer_id = 1 ORDER BY order_id
```
<details><summary>answer</summary>

```result
order_id
101
103
106
```

3 rows. here customer_id is the foreign key, not the primary key, so it can repeat. the tempting 1 comes from [087](./087-primary-key.md), where a lookup by primary key matches at most one row.

</details>

2. a new table shipments has columns shipment_id, order_id and courier. which column is its primary key, which is a foreign key, and what does the foreign key point at?
<details><summary>answer</summary>

shipment_id is the primary key, it identifies a shipment. order_id is the foreign key, pointing at orders.order_id. the tempting answer is that order_id is the key because it has "id" in its name, but a name doesnt decide it, what the column does does.

</details>

---
prev: [092 relationships, one customer, many orders](./092-relationships-one-customer-many-orders.md) | next: [094 what a foreign key stops](./094-what-a-foreign-key-stops.md)
