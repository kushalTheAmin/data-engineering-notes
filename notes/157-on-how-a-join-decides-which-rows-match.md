# 157: ON, how a join decides which rows match
builds on: [093 foreign key, a column that points at another tables key](./093-foreign-key.md), [155 why joins, the answer lives in more than one table](./155-why-joins-the-answer-lives-in-more-than-one-table.md), [156 inner join traced by hand](./156-inner-join-traced-by-hand.md)
section: combining tables with joins, part 3, ~2 min read

a join checks 35 pairs and keeps 7. what if the check said yes to every pair?

in [156](./156-inner-join-traced-by-hand.md) an inner join (keeps only pairs that pass a test) dropped 28 of 35 pairs. the test is the ON. its the if inside the loop from [155](./155-why-joins-the-answer-lives-in-more-than-one-table.md): for each pair of rows, ON is true or false, and the pair survives on true. usually it compares a foreign key (a column holding another tables id) to the id it points at, but thats a habit, not a rule. any true or false test works. here is the shop (the imaginary gujarati snack store these notes run on) with three different ONs, counting the rows each one keeps:

```sql
SELECT
  (SELECT count(*) FROM orders JOIN customers ON orders.customer_id = customers.customer_id) AS ids_match,
  (SELECT count(*) FROM orders JOIN customers ON orders.customer_id = customers.customer_id AND customers.city = 'Jersey City') AS and_jersey_city,
  (SELECT count(*) FROM orders JOIN customers ON true) AS always_true
```

```result
ids_match | and_jersey_city | always_true
7 | 4 | 35
```

the middle one adds a second test with AND, so a pair needs both, and only the 4 orders from Asha and Chirag (both in Jersey City) remain. the last one never says no, so all 35 pairs come out, every order next to every customer. i assumed ON had to be an equals between ids, and it takes whatever test you hand it.

the bite is that nothing errors. compare the wrong columns, or lose the id test in an edit, and you get a plausible looking table that is too big or too small. the Postgres docs describe the always true case as a cross join, a Cartesian product: N rows times M rows. so when a joined count looks off, check the ON first.

---
prev: [156 inner join traced by hand](./156-inner-join-traced-by-hand.md) | next: not written yet
