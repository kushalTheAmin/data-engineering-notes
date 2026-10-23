# 183: INTERSECT and EXCEPT
builds on: [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [121 DISTINCT, removing duplicate rows](./121-distinct-removing-duplicate-rows.md), [179 NOT IN and the NULL trap](./179-not-in-and-the-null-trap.md), [182 UNION and UNION ALL](./182-union-and-union-all.md)
section: bigger queries, part 10, ~2 min read

which customers have both a delivered order and an order that is not delivered? and which have only delivered ones? in [182](./182-union-and-union-all.md) i stacked these two lists of customer ids, here i compare them instead.

INTERSECT keeps the rows that appear in both queries. EXCEPT keeps the rows from the first query that are missing from the second. the shop, the imaginary gujarati snack store these notes run on, has customer ids (1 Asha, 2 Bhavin, 3 Chirag, 4 Disha) 1, 2, 1, 4, 2 on [delivered](./106-where-keeping-only-the-rows-that-match.md) (WHERE, keeps rows passing a test) orders and 3, 1 on the rest:

```sql
SELECT customer_id FROM orders WHERE status = 'delivered' INTERSECT SELECT customer_id FROM orders WHERE status <> 'delivered'
```

```result
customer_id
1
```

```sql
SELECT customer_id FROM orders WHERE status = 'delivered' EXCEPT SELECT customer_id FROM orders WHERE status <> 'delivered' ORDER BY customer_id
```

```result
customer_id
2
4
```

in python these are two sets, `a & b` and `a - b`. like plain [UNION](./182-union-and-union-all.md) (stacks two queries, drops repeats), both also drop repeated rows, so Bhavin shows once even with 2 delivered orders.

i expected swapping the two queries to give the same rows. it doesnt. flip EXCEPT and you get customer 3, Chirag, whose only order was cancelled. INTERSECT is the one that doesnt care about order.

this is the quick way to ask "who is in A but not B" without a join. same columns-by-position rule as UNION.

### check yourself

1. snack names are dhokla, khandvi, fafda. names under 6 are jalebi, masala chai, fafda. subtracting in the other direction, snacks EXCEPT cheap, keeps dhokla and khandvi. predict the rows when the sides swap, as written below.
```sql
SELECT name FROM products WHERE price < 6 EXCEPT SELECT name FROM products WHERE category = 'snack' ORDER BY name
```
<details><summary>answer</summary>

```result
name
jalebi
masala chai
```
EXCEPT only subtracts the second list from the first, so fafda goes and the cheap non-snacks stay. the tempting answer is dhokla and khandvi again, from thinking the difference is the same both ways.

</details>

2. the cities are Jersey City, Edison, Jersey City, Hoboken, and Esha has none (a NULL). as [179](./179-not-in-and-the-null-trap.md) showed, NOT IN dies on a NULL. predict the rows here.
```sql
SELECT city FROM customers EXCEPT SELECT city FROM customers WHERE customer_id = 5 ORDER BY city
```
<details><summary>answer</summary>

```result
city
Edison
Hoboken
Jersey City
```
EXCEPT treats two NULLs as the same, like DISTINCT does, so the NULL city is removed and 3 rows stay. the tempting answer is 4, with a NULL row left in because NULL never equals anything.

</details>

---
prev: [182 UNION and UNION ALL](./182-union-and-union-all.md) | next: [184 window functions, a total next to every row](./184-window-functions-a-total-next-to-every-row.md)
