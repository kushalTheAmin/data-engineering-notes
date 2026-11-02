# 301: reading EXPLAIN, the plan as a tree
builds on: [300 merge join, walk two sorted lists side by side](./300-merge-join-walk-two-sorted-lists-side-by-side.md), [299 hash join, build a hash table then look up each row](./299-hash-join-build-a-hash-table-then-look-up-each-row.md), [296 the query planner, picking the cheapest plan](./296-the-query-planner-picking-the-cheapest-plan.md), [285 full table scan, reading every page](./285-full-table-scan-reading-every-page.md), [280 trees, data that branches](./280-trees-data-that-branches.md), [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md)
section: inside a database server, part 18, ~2 min read

the last three notes each showed one join method, but EXPLAIN prints 8 lines for a single join and a GROUP BY, indented like stairs. which of those lines do you think actually touches the tables?

a plan is a [tree](./280-trees-data-that-branches.md) (boxes linked parent to children). each box, a node, does one job and hands its rows up to the node above. EXPLAIN, the command that prints the [plan](./296-the-query-planner-picking-the-cheapest-plan.md) Postgres picked, writes each child indented under its parent ([docs](https://www.postgresql.org/docs/16/using-explain.html)).

the shop, the imaginary gujarati snack store these notes run on, with its real 7 orders. how many delivered orders per customer?

```sql
SELECT c.name, count(*) AS delivered
FROM customers c JOIN orders o ON o.customer_id = c.customer_id
WHERE o.status = 'delivered' GROUP BY c.name;
```

```result
name | delivered
Asha | 2
Bhavin | 2
Disha | 1
```

and the plan, Postgres 16, with my arrows added:

```text
-- Postgres 16
EXPLAIN (COSTS OFF) <the same query>

 HashAggregate                          <- last: GROUP BY, 5 rows in, 3 out
   Group Key: c.name
   ->  Hash Join                        <- pairs orders with customers, 5 rows
         Hash Cond: (o.customer_id = c.customer_id)
         ->  Seq Scan on orders o       <- reads 7, hands up the 5 delivered
               Filter: ((status)::text = 'delivered'::text)
         ->  Hash                       <- lookup table of the customers
               ->  Seq Scan on customers c    <- reads 5
```

read it from the deepest lines up. only the two [Seq Scans](./285-full-table-scan-reading-every-page.md) (read every page) touch a table. everything above works on rows handed up, and the Hash Join is the [one from 299](./299-hash-join-build-a-hash-table-then-look-up-each-row.md), orders probing a table built from customers. the WHERE is not its own node, its the Filter line inside the orders scan, so the 2 other orders never reach the join.

i assumed the top line ran first since thats where my eye goes, but the top node is the last to see any rows, and the stairs are the data flowing up.

one more thing: a nodes cost includes its children, so the top line is the total for the whole plan (the docs say so). here that is 2.30 once the cost is switched on.

### check yourself

1. you change the query to WHERE o.status = 'cancelled'. Postgres may pick other join nodes, but the orders Seq Scan keeps the Filter. how many rows does it hand up, and what does the query return?

```sql
SELECT c.name, count(*) AS cancelled
FROM customers c JOIN orders o ON o.customer_id = c.customer_id
WHERE o.status = 'cancelled' GROUP BY c.name;
```

<details><summary>answer</summary>

```result
name | cancelled
Chirag | 1
```

the scan still reads all 7 but hands up 1, because the Filter lives inside it, so the query returns 1 row. the tempting answer is 7 handed up, from thinking the scan returns the table and something later filters.

</details>

2. in the delivered plan, Esha has no delivered orders. at which node does she drop out?

<details><summary>answer</summary>

the Hash Join. the customers scan and the Hash still hold all 5 customers, but no delivered order carries customer 5, so nothing pairs with her. the tempting answer is the orders scan, but that filters orders and has never seen customers.

</details>

---
prev: [300 merge join, walk two sorted lists side by side](./300-merge-join-walk-two-sorted-lists-side-by-side.md) | next: not written yet
