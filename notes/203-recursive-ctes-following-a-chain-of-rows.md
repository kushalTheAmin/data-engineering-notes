# 203: recursive CTEs, following a chain of rows
builds on: [156 inner join traced by hand](./156-inner-join-traced-by-hand.md), [158 table aliases](./158-table-aliases-short-nicknames-for-tables.md), [180 CTEs](./180-ctes-naming-each-step-with-with.md), [182 UNION ALL](./182-union-and-union-all.md)
section: bigger queries, part 30, ~2 min read

Asha told Bhavin about the shop, Bhavin told Disha, Disha told Esha. how do you ask for everyone Asha brought in, through friends of friends, when you dont know how many hops there are?

a recursive CTE is a [CTE](./180-ctes-naming-each-step-with-with.md) (an inner query named up front with WITH) that reads its own rows. a start query runs once, then a repeat query runs on the rows the last round found, until a round finds nothing. the shop, the imaginary gujarati snack store these notes run on, has a new referrals table, one row per customer who came through a friend. round by round:

| round | rows found | why |
|---|---|---|
| 0 | Asha | the start query |
| 1 | Bhavin, Chirag | referred by Asha |
| 2 | Disha | referred by Bhavin |
| 3 | Esha | referred by Disha |
| 4 | nobody | nobody was referred by Esha, so stop |

its a while loop that ends on an empty list. the two queries are glued with [UNION ALL](./182-union-and-union-all.md) (stack rows, keep repeats), and the second one reads chain, the CTEs own name. its [inner joins](./156-inner-join-traced-by-hand.md) pair rows where ids match, and ch (chain), r (referrals) and cu (customers) are [nicknames](./158-table-aliases-short-nicknames-for-tables.md):

```sql
WITH RECURSIVE chain AS (SELECT customer_id, name, 0 AS depth FROM customers WHERE name = 'Asha' UNION ALL SELECT cu.customer_id, cu.name, ch.depth + 1 FROM chain AS ch JOIN referrals AS r ON r.referred_by = ch.customer_id JOIN customers AS cu ON cu.customer_id = r.customer_id) SELECT name, depth FROM chain ORDER BY depth, name
```

```result
name | depth
Asha | 0
Bhavin | 1
Chirag | 1
Disha | 2
Esha | 3
```

i expected a recursive query to need some special loop syntax, but its a plain UNION ALL where the second half is allowed to look at the CTE. each round only sees the rows the round before found, so depth, the number of hops from Asha, is the old depth plus 1.

the catch is the stop. Postgres docs say the repeat part has to eventually return no rows or the query loops indefinitely, so if Asha were listed as referred by Esha, this would never end.

---
prev: [202 retention, who came back the month after](./202-retention-who-came-back-the-month-after.md) | next: [204 arrays and UNNEST, lists inside a cell](./204-arrays-and-unnest-lists-inside-a-cell.md)
