# 173: capstone, the shop revenue report from four tables
builds on: [138 COUNT star vs COUNT of a column](./138-count-star-vs-count-of-a-column.md), [139 COUNT DISTINCT, counting different values](./139-count-distinct-counting-different-values.md), [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md), [154 capstone, orders per customer traced from rows to groups](./154-capstone-orders-per-customer-traced-from-rows-to-groups.md), [155 why joins, the answer lives in more than one table](./155-why-joins-the-answer-lives-in-more-than-one-table.md), [156 inner join traced by hand](./156-inner-join-traced-by-hand.md), [157 ON, how a join decides which rows match](./157-on-how-a-join-decides-which-rows-match.md), [158 table aliases, short nicknames for tables](./158-table-aliases-short-nicknames-for-tables.md), [159 left join, keep every row from the left table](./159-left-join-keep-every-row-from-the-left-table.md), [160 the nulls a left join creates](./160-the-nulls-a-left-join-creates.md), [161 a WHERE that quietly turns a left join into an inner join](./161-a-where-that-quietly-turns-a-left-join-into-an-inner-join.md), [162 right and full outer joins](./162-right-and-full-outer-joins.md), [163 joining three tables](./163-joining-three-tables.md), [164 fan out, when a join multiplies rows](./164-fan-out-when-a-join-multiplies-rows.md), [165 double counting, why sums after a fan out lie](./165-double-counting-why-sums-after-a-fan-out-lie.md), [166 joining on columns that can be NULL](./166-joining-on-columns-that-can-be-null.md), [167 anti join, rows with no match](./167-anti-join-rows-with-no-match.md), [168 self join, a table joined to itself](./168-self-join-a-table-joined-to-itself.md), [169 cross join, every row with every row](./169-cross-join-every-row-with-every-row.md), [170 joining on a range, matching a date to a period](./170-joining-on-a-range-matching-a-date-to-a-period.md), [171 joins plus GROUP BY, revenue per customer](./171-joins-plus-group-by-revenue-per-customer.md), [172 practice, five join questions on the shop, checking row counts](./172-practice-five-join-questions-on-the-shop-checking-row-counts.md)
section: combining tables with joins, wrap up, ~3 min read

Esha never ordered, Chirag only has a cancelled order, and the owner still wants all 5 customers on one report with delivered revenue. can you get that out of joins in one query? the last section ended on [154](./154-capstone-orders-per-customer-traced-from-rows-to-groups.md), where Esha had no group at all, and this section is how she gets back in.

the answer is a chain of left joins (each keeps every row from the table written first, [159](./159-left-join-keep-every-row-from-the-left-table.md)) into one GROUP BY. the shop, the imaginary gujarati snack store these notes run on, keeps names, orders, items and prices in four tables. here is how the row count moves:

```text
customers                                        5 rows
LEFT JOIN orders, status test inside ON  [157, 161]   7 rows  (Chirag and Esha get NULL)
LEFT JOIN order_items                    [163, 164]  13 rows  (orders fan out into items)
LEFT JOIN products                       [163]       13 rows  (one price per item)
GROUP BY name, sum quantity * price      [171]        5 rows
```

```sql
SELECT c.name, count(DISTINCT o.order_id) AS orders, coalesce(sum(oi.quantity), 0) AS items, coalesce(sum(oi.quantity * p.price), 0) AS revenue FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.status = 'delivered' LEFT JOIN order_items oi ON o.order_id = oi.order_id LEFT JOIN products p ON oi.product_id = p.product_id GROUP BY c.name ORDER BY c.name
```

```result
name | orders | items | revenue
Asha | 2 | 6 | 28.50
Bhavin | 2 | 4 | 28.00
Chirag | 0 | 0 | 0.00
Disha | 1 | 5 | 37.00
Esha | 0 | 0 | 0.00
```

the status test sits in the ON, so cancelled and pending orders never join, but the customer stays. every join after it is a left join too, or Esha dies at the next one. count(DISTINCT) counts orders, not the 13 fanned out rows, and coalesce turns the NULL sums into 0. i expected the last join to be the tricky one, and its the ON on the first one that decides who survives.

the pieces, each with its note:
- why and how: [why joins](./155-why-joins-the-answer-lives-in-more-than-one-table.md), [inner join](./156-inner-join-traced-by-hand.md), [ON](./157-on-how-a-join-decides-which-rows-match.md), [aliases](./158-table-aliases-short-nicknames-for-tables.md)
- keeping rows: [left join](./159-left-join-keep-every-row-from-the-left-table.md), [its nulls](./160-the-nulls-a-left-join-creates.md), [the WHERE trap](./161-a-where-that-quietly-turns-a-left-join-into-an-inner-join.md), [right and full](./162-right-and-full-outer-joins.md)
- growing: [three tables](./163-joining-three-tables.md), [fan out](./164-fan-out-when-a-join-multiplies-rows.md), [double counting](./165-double-counting-why-sums-after-a-fan-out-lie.md)
- odd matches: [NULL keys](./166-joining-on-columns-that-can-be-null.md), [anti join](./167-anti-join-rows-with-no-match.md), [self join](./168-self-join-a-table-joined-to-itself.md), [cross join](./169-cross-join-every-row-with-every-row.md), [range join](./170-joining-on-a-range-matching-a-date-to-a-period.md)
- using them: [revenue per customer](./171-joins-plus-group-by-revenue-per-customer.md), [row count practice](./172-practice-five-join-questions-on-the-shop-checking-row-counts.md)

the next section is about queries that hold other queries.

### check yourself

1. a teammate swaps count(DISTINCT o.order_id) for count(o.order_id) in the report. predict the orders column. which customer is wrong in a way you can see?
```sql
SELECT c.name, count(o.order_id) AS orders FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.status = 'delivered' LEFT JOIN order_items oi ON o.order_id = oi.order_id LEFT JOIN products p ON oi.product_id = p.product_id GROUP BY c.name ORDER BY c.name
```
<details><summary>answer</summary>

```result
name | orders
Asha | 4
Bhavin | 4
Chirag | 0
Disha | 3
Esha | 0
```
it counts joined rows, one per item, so Asha shows 4 for 2 orders and Disha 3 for 1. the tempting answer is the same as before, since the column is still named orders.

</details>

2. the report adds up to 93.50, but the revenue per customer in [171](./171-joins-plus-group-by-revenue-per-customer.md) with no status test added up to 126.50. which statuses explain the 33.00 gap?
```sql
SELECT o.status, sum(oi.quantity * p.price) AS revenue FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id GROUP BY o.status ORDER BY o.status
```
<details><summary>answer</summary>

```result
status | revenue
cancelled | 18.00
delivered | 93.50
pending | 15.00
```
cancelled 18.00 plus pending 15.00 is 33.00, so no row went missing, the ON just kept those two out on purpose. the tempting answer is a join dropping rows, but the left joins kept every customer.

</details>

---
prev: [172 practice, five join questions on the shop, checking row counts](./172-practice-five-join-questions-on-the-shop-checking-row-counts.md) | next: not written yet
