# 299: hash join, build a hash table then look up each row
builds on: [298 nested loop join, for each outer row search the inner side](./298-nested-loop-join-for-each-outer-row-search-the-inner-side.md), [278 hash tables, how a dictionary finds a key without searching](./278-hash-tables-how-a-dictionary-finds-a-key-without-searching.md), [296 the query planner, picking the cheapest plan](./296-the-query-planner-picking-the-cheapest-plan.md)
section: inside a database server, part 16, ~2 min read

in [298](./298-nested-loop-join-for-each-outer-row-search-the-inner-side.md) the join of orders to customers stayed a nested loop (search the inner side once per outer row) with one order, then switched at 100000. what does Postgres, the database server these notes use, do instead of searching 5 customers 100000 times?

a hash join first loads one side into a [hash table](./278-hash-tables-how-a-dictionary-finds-a-key-without-searching.md) (slots where a keys hash picks the place to look). that is the build. then it reads the other side once, and each row looks up its match in about one look. that is the probe. here the inner side is the 5 customers, the outer is the 7 orders; Postgres loads the inner side and probes with the outer ([docs](https://www.postgresql.org/docs/16/planner-optimizer.html)).

the shop, the imaginary gujarati snack store these notes run on, with its real 7 orders and 5 customers. a python dictionary is a hash table:

```python
customers = [(1, "Asha"), (2, "Bhavin"), (3, "Chirag"), (4, "Disha"), (5, "Esha")]
orders = [(101, 1), (102, 2), (103, 1), (104, 3), (105, 4), (106, 1), (107, 2)]

nested = 0
for order_id, cid in orders:
    for c_id, name in customers:
        nested += 1

table = {}
for c_id, name in customers:
    table[c_id] = name

for order_id, cid in orders:
    print(order_id, table[cid])

print("nested loop looks:", nested)
print("hash join looks:", len(customers) + len(orders))
print("at 100000 orders:", 100000 * 5, "vs", 5 + 100000)
```

```output
101 Asha
102 Bhavin
103 Asha
104 Chirag
105 Disha
106 Asha
107 Bhavin
nested loop looks: 35
hash join looks: 12
at 100000 orders: 500000 vs 100005
```

5 to build, 7 to probe, same rows as the loop. i expected the speedup to be in the searching, but each search became one slot and the cost moved to a build paid once. toy counts. planner costs from 298 at 100000 orders were 2126.11 for the hash join against 3940.88 for the loop, so the [planner](./296-the-query-planner-picking-the-cheapest-plan.md) picked the hash; with one order the loop won.

the catch: a hash only finds equal values, so you cant ask for bigger or smaller. a join whose only test is order date after joined date has no slot to jump to, so it cant be a hash join ([docs](https://www.postgresql.org/docs/16/xoper-optimization.html)).

### check yourself

1. a hash join builds the table from customers and probes with the 7 orders. which customer sits in the table and never gets looked up?

```sql
SELECT name FROM customers WHERE customer_id NOT IN (SELECT customer_id FROM orders)
```

<details><summary>answer</summary>

```result
name
Esha
```

Esha has no orders, so no probe ever asks for customer 5. the tempting answer is nobody, because every entry was built to be used, but the probes decide what gets touched.

</details>

2. a teammate says hash joins are fast, so (joined date before order date, no other test) should use one. what is wrong?

<details><summary>answer</summary>

a hash lookup only finds equal values, and a less-than has no single slot to jump to. so the loop inside a loop from 298 still runs. the tempting answer is that hashing is fast enough to handle any condition, but speed is not the issue, the hash simply carries no order.

</details>

---
prev: [298 nested loop join, for each outer row search the inner side](./298-nested-loop-join-for-each-outer-row-search-the-inner-side.md) | next: not written yet
