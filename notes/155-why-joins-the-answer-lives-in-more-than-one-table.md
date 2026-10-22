# 155: why joins, the answer lives in more than one table
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [091 splitting into tables, each fact lives in one place](./091-splitting-into-tables.md), [093 foreign key, a column that points at another tables key](./093-foreign-key.md), [154 capstone, orders per customer traced from rows to groups](./154-capstone-orders-per-customer-traced-from-rows-to-groups.md)
section: combining tables with joins, part 1, ~2 min read

order 104 was cancelled. which city was it going to? the orders table has no city, and the customers table has no orders.

[154](./154-capstone-orders-per-customer-traced-from-rows-to-groups.md) ended on Esha, who the orders table cant show. this is the mirror problem: the orders table cant show a city. the shop (the imaginary gujarati snack store these notes run on) is split into tables, as in [091](./091-splitting-into-tables.md), so each fact is written once, and the price is that a question touching two tables needs them put back together. thats a join: pair up rows from two tables, usually wherever a [foreign key](./093-foreign-key.md) (a column holding another tables id) equals the id it points at.

in python its a loop inside a loop. a slice (just a few rows) of the orders and customers tables, each a list of dictionaries:

```python
orders = [{"order_id": 101, "customer_id": 1}, {"order_id": 104, "customer_id": 3}, {"order_id": 105, "customer_id": 4}]
customers = [{"customer_id": 1, "name": "Asha", "city": "Jersey City"}, {"customer_id": 3, "name": "Chirag", "city": "Jersey City"}, {"customer_id": 4, "name": "Disha", "city": "Hoboken"}]
for o in orders:
    for c in customers:
        if o["customer_id"] == c["customer_id"]:
            print(o["order_id"], c["name"], c["city"])
```

```output
101 Asha Jersey City
104 Chirag Jersey City
105 Disha Hoboken
```

the same on all 7 orders and 5 customers, in SQL. ON says which two columns must be equal here:

```sql
SELECT orders.order_id, customers.name, customers.city FROM orders JOIN customers ON orders.customer_id = customers.customer_id ORDER BY orders.order_id
```

```result
order_id | name | city
101 | Asha | Jersey City
102 | Bhavin | Edison
103 | Asha | Jersey City
104 | Chirag | Jersey City
105 | Disha | Hoboken
106 | Asha | Jersey City
107 | Bhavin | Edison
```

so 104 was Chirag, in Jersey City. i figured pulling in a second table would make the result bigger, but its 7 rows, the same as orders, because each order finds exactly one customer. Esha is missing again, nobody points at her.

you never write that loop. the database often finds a faster way, and the rows come out the same. the docs of Postgres, a popular database, call the literal loop a nested loop join.

---
prev: [154 capstone, orders per customer traced from rows to groups](./154-capstone-orders-per-customer-traced-from-rows-to-groups.md) | next: [156 inner join traced by hand](./156-inner-join-traced-by-hand.md)
