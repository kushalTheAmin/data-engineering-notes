# 255: entities and attributes
builds on: [254 modeling, deciding the tables before writing them](./254-modeling-deciding-the-tables-before-writing-them.md), [098 entity relationship diagrams](./098-entity-relationship-diagrams.md), [089 update anomalies](./089-update-anomalies.md), [091 splitting into tables](./091-splitting-into-tables.md)
section: designing tables, part 2, ~2 min read

customers has a city column, but orders points at a customer with an id. so why is a customer its own table and a city just a column?

in [254](./254-modeling-deciding-the-tables-before-writing-them.md) i asked of each receipt fact what it was a fact about. the answer is an [entity](./098-entity-relationship-diagrams.md) (a kind of thing you keep facts about, one table), and each fact is an attribute, one fact about one entity, stored as a column.

in the shop, the imaginary gujarati snack store, name, city and joined_on are all attributes of a customer. count the cities:

```sql
SELECT city, count(*) AS customers FROM customers GROUP BY city ORDER BY city;
```

```result
city | customers
Edison | 1
Hoboken | 1
Jersey City | 2
NULL | 1
```

GROUP BY makes one group per city and count(*) counts its rows. the NULL is Esha, who has no city (no value). as a column this is fine. now say the shop wants a delivery fee per city. the fee isnt a fact about Asha, its a fact about Jersey City. put it in customers and it gets written on Asha and Chirag both, the copy bug from [089](./089-update-anomalies.md). so city stops being an attribute and becomes an entity with its own table, and customers keeps just an id, the split from [091](./091-splitting-into-tables.md).

i assumed entity or attribute was a fixed label on the thing itself, but its decided by whether you want to keep facts about it. test it on a value: would i ever store something about this? status, probably not, it stays a column. a table for every column is its own mess.

---
prev: [254 modeling, deciding the tables before writing them](./254-modeling-deciding-the-tables-before-writing-them.md) | next: not written yet
