# 023: true and false, the boolean
builds on: [001 data is facts written down](./001-data-is-facts-and-numbers.md), [002 bits, everything is a tiny switch](./002-bits.md), [004 bytes, 8 bits and 256 possible values](./004-bytes.md)
section: data at the atom level, part 23, ~2 min read

the shop, the imaginary gujarati snack store these notes run on, keeps its orders in a table, rows with named columns. one column is status, with words like delivered. so what does the database hand back when you ask whether an order is delivered? not a word, and not a number you picked.

it hands back a boolean: a value that is true or false. thats nearly the whole type.

```sql
SELECT order_id, status, status = 'delivered' AS delivered FROM orders;
```

```result
order_id | status | delivered
101 | delivered | true
102 | delivered | true
103 | delivered | true
104 | cancelled | false
105 | delivered | true
106 | pending | false
107 | delivered | true
```

the third column is a new column the query made on the fly, and every comparison you will ever write gives one of these, unless a value is missing, which gives null, a third answer meaning unknown. SELECT lists columns, FROM names the table, and = asks if two things are equal. a flag column like is_delivered is the same thing saved in the table.

two states is one [bit](./002-bits.md), the on/off switch. i figured a boolean would cost one lonely bit, but computers hand out storage in [bytes](./004-bytes.md), groups of 8 bits, so Postgres, a server database, spends 1 whole byte on each boolean: https://www.postgresql.org/docs/current/datatype-boolean.html

and code that counts is happy with that, python treats True as 1 and False as 0:

```python
flags = [True, True, True, False, True, False, True]
print(sum(flags))
```

```output
5
```

5 delivered out of 7. the same page says Postgres also accepts yes, no, on, off, 1 and 0 as boolean input, so a messy file saying "yes" can quietly load as true. you might want that, you might not.

---
prev: [022 exact decimal types](./022-exact-decimal-types.md) | next: [024 UTC, the worlds reference clock](./024-utc.md)
