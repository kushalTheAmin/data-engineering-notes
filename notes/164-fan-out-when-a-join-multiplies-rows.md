# 164: fan out, when a join multiplies rows
builds on: [092 relationships, one customer many orders](./092-relationships-one-customer-many-orders.md), [143 group by, one group per value](./143-group-by-one-group-per-value.md), [156 inner join traced by hand](./156-inner-join-traced-by-hand.md), [163 joining three tables](./163-joining-three-tables.md)
section: combining tables with joins, part 10, ~2 min read

i joined 7 orders to their items and got 13 rows back. where did 6 extra orders come from? they didnt, some orders got repeated.

thats fan out: a left row matching several right rows is kept once per match. in the shop (the imaginary gujarati snack store these notes run on), order_items has one row per product in an order, the "many" side of a [one to many](./092-relationships-one-customer-many-orders.md) link. an [inner join](./156-inner-join-traced-by-hand.md) (keeps only matching pairs) on orders 104 and 105:

```sql
SELECT o.order_id, o.status, oi.product_id FROM orders o JOIN order_items oi ON o.order_id = oi.order_id WHERE o.order_id IN (104, 105) ORDER BY o.order_id, oi.product_id
```

```result
order_id | status | product_id
104 | cancelled | 1
105 | delivered | 3
105 | delivered | 4
105 | delivered | 5
```

order 105 has three items, so it shows up three times. i read a join as adding columns, and it can photocopy the row instead. rows per order, per [group](./143-group-by-one-group-per-value.md):

```sql
SELECT o.order_id, count(*) AS rows_out FROM orders o JOIN order_items oi ON o.order_id = oi.order_id GROUP BY o.order_id ORDER BY o.order_id
```

```result
order_id | rows_out
101 | 2
102 | 2
103 | 2
104 | 1
105 | 3
106 | 1
107 | 2
```

2 + 2 + 2 + 1 + 3 + 1 + 2 is 13, the answer to the extra rows in [163](./163-joining-three-tables.md). an order with no items would get zero copies and vanish.

this is how "how many orders" becomes 13 on a dashboard, when you count rows after a join.

### check yourself

1. after joining customers to orders, what does this return?

```sql
SELECT c.name, count(*) AS rows_out FROM customers c JOIN orders o ON c.customer_id = o.customer_id WHERE c.name IN ('Asha', 'Esha') GROUP BY c.name
```

<details><summary>answer</summary>

```result
name | rows_out
Asha | 3
```

Asha has 3 orders, so she fans out to 3 rows. Esha has none, so she gets zero copies and no row at all. the tempting answer is Esha with 0, but a count of nothing needs a row to sit on.

</details>

2. you join orders to order_items and count(*) gives 13, but your boss wants the number of orders. what do you change, and what comes out?

<details><summary>answer</summary>

count each order once with count(DISTINCT o.order_id).

```sql
SELECT count(*) AS n, count(DISTINCT o.order_id) AS orders FROM orders o JOIN order_items oi ON o.order_id = oi.order_id
```

```result
n | orders
13 | 7
```

the join made 13 rows, but only 7 different order ids. adding a WHERE wouldnt fix it, no row is wrong, there are just too many.

</details>

---
prev: [163 joining three tables](./163-joining-three-tables.md) | next: [165 double counting, why sums after a fan out lie](./165-double-counting-why-sums-after-a-fan-out-lie.md)
