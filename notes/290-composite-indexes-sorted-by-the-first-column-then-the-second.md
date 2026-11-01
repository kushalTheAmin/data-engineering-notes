# 290: composite indexes, sorted by the first column, then the second
builds on: [289 how a B tree stays balanced as rows arrive](./289-how-a-b-tree-stays-balanced-as-rows-arrive.md), [286 index, a sorted shortcut to rows](./286-index-a-sorted-shortcut-to-rows.md)
section: inside a database server, part 7, ~2 min read

[289](./289-how-a-b-tree-stays-balanced-as-rows-arrive.md) kept the sorted entries in order as rows arrive. but an index on customer_id alone puts Ashas 3 entries side by side with no say in their order, so what if the index sorted on two columns?

a composite index (Postgres, a database server, calls it multicolumn) is an [index](./286-index-a-sorted-shortcut-to-rows.md), a sorted list of values plus where each row lives, on two or more columns. entries sort by the first column, and only inside a tie (two entries with the same first value) does the second decide.

the shop, the imaginary gujarati snack store these notes run on, with its 7 orders. an index on (customer_id, ordered_at) holds these entries, order_id standing in for where each row lives:

```sql
SELECT customer_id, ordered_at, order_id FROM orders ORDER BY customer_id, ordered_at;
```

```result
customer_id | ordered_at | order_id
1 | 2026-04-01 09:15:00 | 101
1 | 2026-04-03 12:05:00 | 103
1 | 2026-04-08 10:00:00 | 106
2 | 2026-04-01 18:40:00 | 102
2 | 2026-04-09 13:45:00 | 107
3 | 2026-04-04 08:30:00 | 104
4 | 2026-04-06 19:10:00 | 105
```

Ashas 3 orders sit together, oldest first, and Bhavins start only after hers end. now flip the columns to (ordered_at, customer_id):

```sql
SELECT ordered_at, customer_id, order_id FROM orders ORDER BY ordered_at, customer_id;
```

```result
ordered_at | customer_id | order_id
2026-04-01 09:15:00 | 1 | 101
2026-04-01 18:40:00 | 2 | 102
2026-04-03 12:05:00 | 1 | 103
2026-04-04 08:30:00 | 3 | 104
2026-04-06 19:10:00 | 4 | 105
2026-04-08 10:00:00 | 1 | 106
2026-04-09 13:45:00 | 2 | 107
```

now Asha is at 101, 103 and 106 with other people between. every timestamp here is different, so customer_id never gets to break a tie.

i figured two columns meant two sorted lists, but its one list, and the second column only matters inside the first.

in Postgres you write CREATE INDEX ON orders (customer_id, ordered_at), and Ashas orders by time become one unbroken run of entries, because her entries sit together in time order. the Postgres docs describe reading an index from the first matching entry to the last, which only works because of this order. so the column order you pick is the whole design.

### check yourself

1. an index on orders (status, customer_id). what are its first 3 entries?

```sql
SELECT status, customer_id FROM orders ORDER BY status, customer_id LIMIT 3;
```

<details><summary>answer</summary>

```result
status | customer_id
cancelled | 3
delivered | 1
delivered | 1
```

status sorts first, and cancelled comes before delivered, so customer 3 leads even though 1 is smaller. the tempting answer starts with customer 1 and leaves cancelled for later, from sorting on the smaller number.

</details>

2. an index on customers (city, name). does Chirags entry come before or after Dishas?

```sql
SELECT city, name FROM customers WHERE city IS NOT NULL ORDER BY city, name;
```

<details><summary>answer</summary>

```result
city | name
Edison | Bhavin
Hoboken | Disha
Jersey City | Asha
Jersey City | Chirag
```

after. Hoboken sorts before Jersey City, and the name only breaks the tie between Asha and Chirag. the tempting answer is before, from C coming before D in the names.

</details>

---
prev: [289 how a B tree stays balanced as rows arrive](./289-how-a-b-tree-stays-balanced-as-rows-arrive.md) | next: not written yet
