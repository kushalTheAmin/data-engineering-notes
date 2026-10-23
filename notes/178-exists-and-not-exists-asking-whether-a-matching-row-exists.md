# 178: EXISTS and NOT EXISTS, asking whether a matching row exists
builds on: [164 fan out, when a join multiplies rows](./164-fan-out-when-a-join-multiplies-rows.md), [167 anti join, rows with no match](./167-anti-join-rows-with-no-match.md), [174 subquery in WHERE](./174-subquery-in-where.md), [177 correlated subqueries, a query that depends on the outer row](./177-correlated-subqueries-a-query-that-depends-on-the-outer-row.md)
section: bigger queries, part 5, ~2 min read

[174](./174-subquery-in-where.md) found customers with a delivered order by building a list of ids for IN (a match against a list). but you only needed a yes or no per customer: is there at least one delivered order for this person?

EXISTS is that yes or no: true when the inner query returns at least one row and false when it returns none, and NOT EXISTS flips it. the inner query is a [correlated subquery](./177-correlated-subqueries-a-query-that-depends-on-the-outer-row.md) (an inner query that uses the outer row), so every customer is asked separately. in python, on the shop (the imaginary gujarati snack store these notes run on), with orders cut down to order id, customer id and status:

```python
orders = [(101, 1, "delivered"), (102, 2, "delivered"), (103, 1, "delivered"), (104, 3, "cancelled"), (105, 4, "delivered"), (106, 1, "pending"), (107, 2, "delivered")]
customers = [(1, "Asha"), (2, "Bhavin"), (3, "Chirag"), (4, "Disha"), (5, "Esha")]
for cid, name in customers:
    found = [o for o in orders if o[1] == cid and o[2] == "delivered"]
    print(name, len(found), len(found) > 0)
```

```output
Asha 2 True
Bhavin 2 True
Chirag 0 False
Disha 1 True
Esha 0 False
```

the list comprehension is the inner query, `len(found) > 0` is EXISTS. in SQL:

```sql
SELECT name FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status = 'delivered') ORDER BY name
```

```result
name
Asha
Bhavin
Disha
```

Asha has 2 delivered orders and shows up once. EXISTS only asks whether there is one, so it can stop at the first match. a join (rows matched across tables) repeats her, the [fan out](./164-fan-out-when-a-join-multiplies-rows.md) (a left row copied per match), and gives 5 rows. keeping matched left rows once each is called a semi join.

flip it and you get the [anti join](./167-anti-join-rows-with-no-match.md) (keeps left rows with no match), written as the question you mean:

```sql
SELECT name FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status = 'delivered') ORDER BY name
```

```result
name
Chirag
Esha
```

Chirag ordered, but it was cancelled, so he lands next to Esha. what the inner SELECT lists normally doesnt matter: SELECT 1, SELECT * and SELECT NULL behave the same. i kept hunting for what the inner query hands back, and the answer is nothing, only whether anything came.

### check yourself

1. someone forgets the correlation and writes the inner filter as just `o.status = 'delivered'`. how many of the 5 customers does EXISTS keep?
```sql
SELECT name FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.status = 'delivered') ORDER BY name
```
<details><summary>answer</summary>

```result
name
Asha
Bhavin
Chirag
Disha
Esha
```
all 5. the inner query never mentions c, so it gives the same answer for every customer, and delivered orders exist. the tempting answer is 3, from picturing the earlier query, but without the link to the outer row nobody is being checked.

</details>

2. which customers does this keep, and is Asha one of them?
```sql
SELECT name FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status <> 'delivered') ORDER BY name
```
<details><summary>answer</summary>

```result
name
Asha
Chirag
```
yes, Asha stays. she has delivered orders too, but one match (her pending order 106) is enough. the tempting answer is Chirag only, from ruling Asha out because she has delivered orders.

</details>

---
prev: [177 correlated subqueries, a query that depends on the outer row](./177-correlated-subqueries-a-query-that-depends-on-the-outer-row.md) | next: [179 NOT IN and the NULL trap](./179-not-in-and-the-null-trap.md)
