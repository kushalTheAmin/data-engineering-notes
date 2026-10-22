# 165: double counting, why sums after a fan out lie
builds on: [121 DISTINCT, removing duplicate rows](./121-distinct-removing-duplicate-rows.md), [140 SUM and AVG, adding up and averaging](./140-sum-and-avg-adding-up-and-averaging.md), [156 inner join traced by hand](./156-inner-join-traced-by-hand.md), [164 fan out, when a join multiplies rows](./164-fan-out-when-a-join-multiplies-rows.md)
section: combining tables with joins, part 11, ~2 min read

the 7 delivery fees in the shop add up to 15.00. pair each one with its order items (a join), sum again, and the database says 31.00. nobody touched a fee, so where did 16 come from?

double counting is a [sum](./140-sum-and-avg-adding-up-and-averaging.md) (adds a column up) running over rows a [fan out](./164-fan-out-when-a-join-multiplies-rows.md) (a left row kept once per match) already copied. in the shop, the imaginary snack store these notes run on, a new table order_fees holds one flat fee per order (104 was cancelled, so 0.00). an [inner join](./156-inner-join-traced-by-hand.md) (keeps only matching pairs) to order_items, one row per product in an order, gives this slice for orders 104 and 105:

| order_id | fee | product_id |
|---|---|---|
| 104 | 0.00 | 1 |
| 105 | 3.00 | 3 |
| 105 | 3.00 | 4 |
| 105 | 3.00 | 5 |

order 105 paid its 3.00 once, but the fee now sits on 3 rows, so sum adds it 3 times. all 13 rows get counted.

```sql
SELECT sum(f.fee) AS joined_sum, count(*) AS rows_out, sum(DISTINCT f.fee) AS distinct_sum FROM order_fees f JOIN order_items oi ON f.order_id = oi.order_id
```

```result
joined_sum | rows_out | distinct_sum
31.00 | 13 | 5.00
```

i figured [DISTINCT](./121-distinct-removing-duplicate-rows.md) would undo the copies, but inside sum it keeps one of each amount, not one of each order. fees are only 0.00, 2.00 and 3.00, so it gives 5.00, wrong in a new way.

for a plain total, the fix is to sum before the join, from order_fees alone, which gives the real 15.00. a column from the many side (order_items), like quantity, is safe to sum in this join, since every item row is real.

this is how a revenue number quietly inflates when someone adds a join to a working query. a cheap habit you can steal: compare the total with the same sum before the join.

### check yourself

1. Asha has orders 101, 103 and 106, all with a 2.00 fee, and they have 2, 2 and 1 rows in order_items. what does this return?

```sql
SELECT sum(f.fee) AS fees FROM orders o JOIN order_fees f ON o.order_id = f.order_id JOIN order_items oi ON o.order_id = oi.order_id WHERE o.customer_id = 1
```

<details><summary>answer</summary>

```result
fees
10.00
```

5 rows of 2.00. the true total is 6.00, and the tempting answer is 6.00 because the fees look like they belong to orders, not rows.

</details>

2. a teammate fixes Ashas number by switching to sum(DISTINCT f.fee). what does that give her, and why is it wrong?

<details><summary>answer</summary>

```sql
SELECT sum(DISTINCT f.fee) AS fees FROM orders o JOIN order_fees f ON o.order_id = f.order_id JOIN order_items oi ON o.order_id = oi.order_id WHERE o.customer_id = 1
```

```result
fees
2.00
```

all three of her fees are 2.00, so DISTINCT keeps one. it collapsed three real orders into one, wrong in the other direction. the tempting answer is 6.00, because it looks like it removes only the copies.

</details>

---
prev: [164 fan out, when a join multiplies rows](./164-fan-out-when-a-join-multiplies-rows.md) | next: [166 joining on columns that can be NULL](./166-joining-on-columns-that-can-be-null.md)
