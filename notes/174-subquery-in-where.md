# 174: subquery in WHERE
builds on: [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [111 IN, matching against a list](./111-in-matching-against-a-list.md), [164 fan out, when a join multiplies rows](./164-fan-out-when-a-join-multiplies-rows.md), [173 capstone, the shop revenue report from four tables](./173-capstone-the-shop-revenue-report-from-four-tables.md)
section: bigger queries, part 1, ~2 min read

which customers have a delivered order? [173](./173-capstone-the-shop-revenue-report-from-four-tables.md) answered everything with joins, but this one doesnt need a join at all, it needs a query inside a query.

a subquery is a SELECT written in parentheses inside another query. in WHERE, after [IN](./111-in-matching-against-a-list.md) (matches a value against a list), the inner query makes the list. the shop is the imaginary gujarati snack store these notes run on, and the easiest way to picture it is the inner query running first:

```text
inner: SELECT customer_id FROM orders WHERE status = 'delivered'
       -> 1, 2, 1, 4, 2        (one id per delivered order)

outer: for each customer, is customer_id in that list?
       Asha    1  yes
       Bhavin  2  yes
       Chirag  3  no
       Disha   4  yes
       Esha    5  no
```

```sql
SELECT name FROM customers WHERE customer_id IN (SELECT customer_id FROM orders WHERE status = 'delivered') ORDER BY name
```

```result
name
Asha
Bhavin
Disha
```

in python its `ids = [o["customer_id"] for o in orders if o["status"] == "delivered"]` and then a loop over customers with `if c["customer_id"] in ids`. the list has repeats, 1 and 2 show up twice, and nobody cares, IN only asks whether the id is in there.

thats the part i liked. the join version of this question gives Asha twice and Bhavin twice, 5 rows, because of the [fan out](./164-fan-out-when-a-join-multiplies-rows.md) (a left row repeated per match). the subquery never repeats a customer, since you only ever ask about customers.

the catch is that it only gives you customer columns. you cant also show the order date from the inner query, thats what a join is for.

### check yourself

1. this runs without error. how many rows does it return, and why?
```sql
SELECT name FROM customers WHERE customer_id IN (SELECT order_id FROM orders WHERE status = 'delivered')
```
<details><summary>answer</summary>

```result
name
```
zero rows. the inner list is order ids, 101 to 107, and no customer id (1 to 5) is in it. the tempting answer is 3, from reading order_id as the customer. the database never checks that the two columns mean the same thing.

</details>

2. orders has 7 rows. predict the count here.
```sql
SELECT count(*) FROM customers WHERE customer_id IN (SELECT customer_id FROM orders)
```
<details><summary>answer</summary>

```result
count_star()
4
```
4, not 7 and not 5. the inner list has 7 ids with repeats, but each customer is checked once, and Esha has no order. 7 is the tempting answer, from counting the list instead of the customers.

</details>

3. you change the inner filter to status <> 'delivered' (any status but delivered). which customers come back, and is Asha a surprise?
<details><summary>answer</summary>

```sql
SELECT name FROM customers WHERE customer_id IN (SELECT customer_id FROM orders WHERE status <> 'delivered') ORDER BY name
```

```result
name
Asha
Chirag
```
Asha has pending order 106, so she counts. this is "has at least one undelivered order", not "never got a delivery". the tempting answer is only Chirag.

</details>

---
prev: [173 capstone, the shop revenue report from four tables](./173-capstone-the-shop-revenue-report-from-four-tables.md) | next: not written yet
