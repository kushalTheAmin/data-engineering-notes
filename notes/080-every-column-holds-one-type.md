# 080: every column holds one type
builds on: [027 dates without times, and times without dates](./027-dates-and-times-apart.md), [031 null, a marker for a missing value](./031-null.md), [076 data types in a schema](./076-data-types-in-a-schema.md), [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md)
section: tables, keys and relationships, part 2, ~2 min read

how does a database add up a whole price column without first checking that every value in it is a number?

it doesnt have to, because in a [table](./079-a-table-rows-are-records-columns-are-fields.md) the [data type](./076-data-types-in-a-schema.md), the kind of value allowed, is chosen once per column, not per value. every row gets the same kind in the same spot. here is Esha from the shop, the imaginary gujarati snack store these notes run on, with the type of each column (typeof asks the database for it, VARCHAR is its word for text):

```sql
SELECT typeof(customer_id) AS id_type, typeof(name) AS name_type, city, typeof(city) AS city_type, typeof(joined_on) AS joined_type FROM customers WHERE customer_id = 5
```

```result
id_type | name_type | city | city_type | joined_type
INTEGER | VARCHAR | NULL | VARCHAR | DATE
```

Eshas city is [NULL](./031-null.md), no value, and the column is still text. NULL fits in a column of any type. joined_on is a DATE, a calendar day with no time, like [027](./027-dates-and-times-apart.md) built.

so what happens if a bad value turns up? the database refuses it instead of storing it:

```sql
-- fails on purpose
SELECT CAST('free' AS DECIMAL(6, 2)) AS price
```

i expected the type to belong to each value, the way it does in python. in a table it belongs to the column, and values have to fit it.

this is the opposite of a csv or a JSON record, where each value just arrives as it is. SQLite is a known exception, it lets the type ride with the value, so a text word can sit in a number column unless you add a rule.

---
prev: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md) | next: not written yet
