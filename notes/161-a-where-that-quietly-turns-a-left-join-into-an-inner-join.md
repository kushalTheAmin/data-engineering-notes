# 161: a WHERE that quietly turns a left join into an inner join
builds on: [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [114 three valued logic, true, false and unknown](./114-three-valued-logic-true-false-and-unknown.md), [157 ON, how a join decides which rows match](./157-on-how-a-join-decides-which-rows-match.md), [159 left join, keep every row from the left table](./159-left-join-keep-every-row-from-the-left-table.md), [160 the nulls a left join creates](./160-the-nulls-a-left-join-creates.md)
section: combining tables with joins, part 7, ~2 min read

i wrote a left join to keep every customer, added one WHERE on the orders side, and Esha vanished again. the join was fine, so what ate her row?

a WHERE comparison on a right table column runs after the join, so it also tests the NULLs (missing values) the join filled in, and drops those rows. in [160](./160-the-nulls-a-left-join-creates.md) Eshas order side was NULL. now `o.status = 'delivered'` meets that NULL, comes out [unknown](./114-three-valued-logic-true-false-and-unknown.md) (neither true nor false), and [WHERE](./106-where-keeping-only-the-rows-that-match.md) keeps only true. the shop (the imaginary gujarati snack store these notes run on), a [left join](./159-left-join-keep-every-row-from-the-left-table.md) (keeps every left row), same test in two places:

```sql
SELECT c.name, o.order_id FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id WHERE o.status = 'delivered' ORDER BY c.name, o.order_id
```

```result
name | order_id
Asha | 101
Asha | 103
Bhavin | 102
Bhavin | 107
Disha | 105
```

5 rows, and Esha and Chirag are both gone, which is exactly what an inner join (keeps only matching pairs) would give. Chirags only order was cancelled, so he has a real order that fails the test. now the test moves into the [ON](./157-on-how-a-join-decides-which-rows-match.md) (the test that decides which pairs match):

```sql
SELECT c.name, o.order_id FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.status = 'delivered' ORDER BY c.name, o.order_id
```

```result
name | order_id
Asha | 101
Asha | 103
Bhavin | 102
Bhavin | 107
Chirag | NULL
Disha | 105
Esha | NULL
```

7 rows. a customer with no delivered order simply has no match, so the left join keeps them with NULL. i assumed a filter was a filter wherever i put it, and with a left join the spot decides what survives. the Postgres docs (a server database) say it plainly: ON is processed before the join, WHERE after, and it only matters for outer joins.

so a right side comparison in WHERE quietly makes your left join an inner join. only IS NULL asks for the filled in rows instead.

### check yourself

1. predict the number of rows, and which customer is the only one with a real order_id.

```sql
SELECT count(*) AS n FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.status = 'cancelled'
```
<details><summary>answer</summary>

```result
n
5
```

5 rows, one per customer, since only order 104 matches and the other 4 customers get a single NULL row. Chirag is the only one with an order_id (104). the tempting answer is 1 row, from reading the test as a filter.

</details>

2. a teammate moves `c.city = 'Jersey City'` from WHERE into the ON of the same left join. does it change the row count?

```sql
SELECT count(*) AS n FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id WHERE c.city = 'Jersey City'
```
<details><summary>answer</summary>

```result
n
4
```

4 rows (Asha 3, Chirag 1), since WHERE on the left table just drops left rows. inside the ON:

```sql
SELECT count(*) AS n FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id AND c.city = 'Jersey City'
```

```result
n
7
```

7, because Bhavin, Disha and Esha are kept with NULL instead of dropped. the tempting answer is no change, from thinking the rule only bites on the right table.

</details>

---
prev: [160 the nulls a left join creates](./160-the-nulls-a-left-join-creates.md) | next: [162 right and full outer joins](./162-right-and-full-outer-joins.md)
