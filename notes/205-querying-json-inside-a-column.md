# 205: querying JSON inside a column
builds on: [031 null, a marker for a missing value](./031-null.md), [066 JSON, records with names on every value](./066-json-records-with-names-on-every-value.md), [083 schema on write vs schema on read](./083-schema-on-write-vs-schema-on-read.md), [132 CAST, changing a values type](./132-cast-changing-a-values-type.md), [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md)
section: bigger queries, part 32, ~2 min read

the shop app logs every click as one JSON string, so how do you ask for the customer when there is no customer column?

the arrow ->> reaches into a [JSON](./066-json-records-with-names-on-every-value.md) string (text with a name on every value) and pulls one value out as text. the shop, the imaginary gujarati snack store these notes run on, has a new app_events table (a table is rows with the same columns, like a list of dictionaries). 4 rows, each an id and a payload column holding one string, like this:

```text
{"type": "add_to_cart", "customer": "Asha", "product": "dhokla", "quantity": 2}
```

ORDER BY event_id sorts the rows. the path after the arrow says where: $ means the whole record, so $.customer means the value named customer. type is view or add_to_cart, and AS just names the output column:

```sql
SELECT event_id, payload ->> '$.customer' AS customer, payload ->> '$.quantity' AS quantity FROM app_events ORDER BY event_id
```

```result
event_id | customer | quantity
1 | Asha | NULL
2 | Asha | 2
3 | Disha | NULL
4 | Bhavin | 1
```

the two view events never had a quantity, so those cells are [NULL](./031-null.md) (a marker for no value). i expected a missing name to raise an error, like a python dictionary does, but ->> quietly hands back NULL. that includes a typo: '$.custmer' would give NULL on all 4 rows and nothing would warn you.

the 2 is text, not a number. so [CAST](./132-cast-changing-a-values-type.md) (converts a value to another type) it before adding, then it works like any column with [GROUP BY](./143-group-by-one-group-per-value.md) (one bucket per value), and WHERE keeps only the add_to_cart rows:

```sql
SELECT payload ->> '$.customer' AS customer, sum(CAST(payload ->> '$.quantity' AS INTEGER)) AS added FROM app_events WHERE payload ->> '$.type' = 'add_to_cart' GROUP BY customer ORDER BY customer
```

```result
customer | added
Asha | 2
Bhavin | 1
```

this is [schema on read](./083-schema-on-write-vs-schema-on-read.md) (shape checked only when you query). Postgres (another database) has ->> on its json columns too, but it takes a bare key like 'quantity', not a $. path.

---
prev: [204 arrays and UNNEST, lists inside a cell](./204-arrays-and-unnest-lists-inside-a-cell.md) | next: [206 practice, ten interview style SQL questions on the shop](./206-practice-ten-interview-style-sql-questions-on-the-shop.md)
