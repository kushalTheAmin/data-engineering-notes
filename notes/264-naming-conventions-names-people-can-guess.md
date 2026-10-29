# 264: naming conventions, names people can guess
builds on: [263 choosing column types, ask what you do with the value](./263-choosing-column-types-by-what-you-do-with-the-value.md), [256 one to one, when two tables share a key](./256-one-to-one-when-two-tables-share-a-key.md), [093 foreign key](./093-foreign-key.md), [157 ON, how a join decides which rows match](./157-on-how-a-join-decides-which-rows-match.md), [158 table aliases, short nicknames for tables](./158-table-aliases-short-nicknames-for-tables.md)
section: designing tables, part 11, ~2 min read

could you join customers to customer_contacts without opening customer_contacts? the shop (the imaginary gujarati snack store these notes run on) says yes, and the reason is just the names.

a naming convention is a set of habits for naming tables and columns so the next person can guess them. the shop uses two. lowercase words joined by underscores (snake_case, like ordered_at), and one fact keeps one name everywhere, so the [foreign key](./093-foreign-key.md) (a column pointing at another tables id) is customer_id in every table.

| messy | what it costs | clean |
|---|---|---|
| "Customer ID" | double quotes in every query | customer_id |
| CustID here, cust_no there | cant guess the join column | customer_id everywhere |
| "OrderDate" | Postgres only answers to the quoted spelling | ordered_at |

the guess, written before looking at the table from [256](./256-one-to-one-when-two-tables-share-a-key.md), using [aliases](./158-table-aliases-short-nicknames-for-tables.md) (short nicknames for tables) c and k:

```sql
SELECT c.name, k.phone FROM customers c JOIN customer_contacts k ON k.customer_id = c.customer_id ORDER BY c.customer_id
```

```result
name | phone
Asha | 555-0101
Bhavin | 555-0102
Disha | 555-0104
```

the [ON line](./157-on-how-a-join-decides-which-rows-match.md) wrote itself. a space in a name forces quotes, and Postgres, a popular server database, turns unquoted names into lowercase, so a column created as "OrderDate" breaks every query that forgets the quotes.

i figured naming was taste, but a name is a promise about what you will find, so keeping it saves everyone a trip to the schema. the next one is about two columns almost every table should carry.

---
prev: [263 choosing column types, ask what you do with the value](./263-choosing-column-types-by-what-you-do-with-the-value.md) | next: [265 created_at and updated_at, two timestamps every table carries](./265-created-at-and-updated-at-two-timestamps-every-table-carries.md)
