# 158: table aliases, short nicknames for tables
builds on: [122 computed columns and AS](./122-computed-columns-and-as.md), [155 why joins, the answer lives in more than one table](./155-why-joins-the-answer-lives-in-more-than-one-table.md), [157 ON, how a join decides which rows match](./157-on-how-a-join-decides-which-rows-match.md)
section: combining tables with joins, part 4, ~2 min read

i gave orders a nickname, kept typing orders.order_id, and the query broke. why would a rename make the old name stop working?

the ON line from [157](./157-on-how-a-join-decides-which-rows-match.md) is 45 characters of orders.customer_id = customers.customer_id, and a real join repeats table names everywhere. a table alias is a short name you give a table for one query, written right after it in FROM. its the same idea as the [column alias](./122-computed-columns-and-as.md) (a name for a result column), just for a table. here is the shop (the imaginary gujarati snack store these notes run on), first 3 rows of the join from [155](./155-why-joins-the-answer-lives-in-more-than-one-table.md), with o for orders and c for customers:

```sql
SELECT o.order_id, c.name, c.city FROM orders o JOIN customers c ON o.customer_id = c.customer_id ORDER BY o.order_id LIMIT 3
```

```result
order_id | name | city
101 | Asha | Jersey City
102 | Bhavin | Edison
103 | Asha | Jersey City
```

the ON shrank to 32 characters, and AS is optional here, so `orders AS o` works too. now the part that bit me:

```sql
-- fails on purpose
SELECT orders.order_id FROM orders o JOIN customers c ON o.customer_id = c.customer_id
```

DuckDB, the database these notes run in, says the table "orders" was not found and suggests "o". the nickname replaces the real name for that query, it doesnt sit beside it. i assumed both would work, since nothing was deleted. the Postgres docs say the same, a table behind an alias cant be reached by its original name.

so pick the nickname once and use it in SELECT, ON and WHERE alike. you will also need aliases when a table joins to itself, because then the real name would be ambiguous (two copies, one name).

---
prev: [157 ON, how a join decides which rows match](./157-on-how-a-join-decides-which-rows-match.md) | next: not written yet
