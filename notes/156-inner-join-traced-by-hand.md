# 156: inner join traced by hand
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [093 foreign key, a column that points at another tables key](./093-foreign-key.md), [155 why joins, the answer lives in more than one table](./155-why-joins-the-answer-lives-in-more-than-one-table.md)
section: combining tables with joins, part 2, ~2 min read

7 orders and 5 customers make 35 possible pairs, and a join hands back only 7. so what happens to the other 28?

[155](./155-why-joins-the-answer-lives-in-more-than-one-table.md) showed a join as a loop inside a loop. an inner join keeps a pair only when the match holds, and drops every pair where it doesnt. the shop (the imaginary gujarati snack store these notes run on) has order 105, whose customer_id, the foreign key (a column holding another tables id), is 4. the loop takes that order and walks down all 5 customer rows:

| customer row | customer_id | equals 4? | pair kept |
|---|---|---|---|
| Asha | 1 | no | dropped |
| Bhavin | 2 | no | dropped |
| Chirag | 3 | no | dropped |
| Disha | 4 | yes | 105 Disha Hoboken |
| Esha | 5 | no | dropped |

1 kept, 4 thrown away. repeat for all 7 orders: 7 times 5 is 35 checks, 7 survivors. i kept picturing a direct jump to the row with id 4, but the plain version just tries every row and keeps the ones that match.

the part that bites is the other direction. flip it around and ask which customers appear ([DISTINCT](./121-distinct-removing-duplicate-rows.md) keeps one copy of each name):

```sql
SELECT DISTINCT customers.name FROM customers JOIN orders ON customers.customer_id = orders.customer_id ORDER BY customers.name
```

```result
name
Asha
Bhavin
Chirag
Disha
```

Esha matched nothing, so she isnt in the output, and nothing warns you. a plain JOIN is an inner join in Postgres and DuckDB (two databases), so a report built on one quietly loses customers with no orders. a later note shows how to keep them.

### check yourself

1. Asha and Chirag live in Jersey City, and between them they placed 4 orders, Asha 3 and Chirag 1. how many rows does this return? dont run it first.
```sql
SELECT count(*) FROM orders JOIN customers ON orders.customer_id = customers.customer_id WHERE customers.city = 'Jersey City'
```
<details><summary>answer</summary>

```result
count_star()
4
```
four rows. the join first pairs each order with its customer, then WHERE keeps the ones whose city is Jersey City. the tempting answer is 2, from counting the 2 customers who live there, but the rows being counted are orders.

</details>

2. the shop adds a sixth customer who has ordered nothing. for the literal loop, how many checks now, and how many rows come out?
<details><summary>answer</summary>

42 checks, still 7 rows. every order is compared with every customer, 7 times 6, and the new customer matches no order so adds no row. the tempting answer is 8 rows, from thinking a new customer always shows up. the database often skips most of the checks, but the result is the same.

</details>

---
prev: [155 why joins, the answer lives in more than one table](./155-why-joins-the-answer-lives-in-more-than-one-table.md) | next: not written yet
