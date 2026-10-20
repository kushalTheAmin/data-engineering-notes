# 119: where NULLs land when you sort
builds on: [031 null, a marker for a missing value](./031-null.md), [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [117 ORDER BY, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md)
section: asking questions with SQL, part 19, ~2 min read

i sorted the shop customers by city, biggest first, and expected Esha, who has no city, to land somewhere obvious. where would you guess?

a [null](./031-null.md) (a missing value) isnt bigger or smaller than anything, so [ORDER BY](./117-order-by-sorting-by-one-or-more-columns.md) needs a rule for where it goes, and the rule is NULLS FIRST or NULLS LAST. here is the customers [table](./079-a-table-rows-are-records-columns-are-fields.md) of the shop, the imaginary gujarati snack store these notes run on, in DuckDB:

```sql
SELECT name, city FROM customers ORDER BY city DESC
```

```result
name | city
Asha | Jersey City
Chirag | Jersey City
Disha | Hoboken
Bhavin | Edison
Esha | NULL
```

Esha is last even though the sort is DESC. DuckDB puts nulls last by default, ASC or DESC. now say where you want her:

```sql
SELECT name, city FROM customers ORDER BY city NULLS FIRST, name
```

```result
name | city
Esha | NULL
Bhavin | Edison
Disha | Hoboken
Asha | Jersey City
Chirag | Jersey City
```

i assumed every database agrees on this, and they dont. Postgres, a server database, treats null as bigger than every value, so its nulls go last on ASC but first on DESC, per its docs. so the same DESC query that put Esha last here would put her at the top there.

that is how a report quietly changes when you move it between databases, and why people write NULLS LAST out loud whenever it matters. Jersey City is a tie, so Asha before Chirag is only guaranteed here because of the name column, same lesson as [118](./118-no-order-by-no-promised-order.md).

### check yourself

1. whats the first row of this query, and the last?

```sql
SELECT name FROM customers ORDER BY city DESC NULLS FIRST, name
```

<details><summary>answer</summary>

```result
name
Esha
Asha
Chirag
Disha
Bhavin
```

first is Esha, last is Bhavin. the tempting answer is Esha last, from remembering that DuckDB defaults to nulls last, but the NULLS FIRST you write overrides the default.

</details>

2. a report ends with ORDER BY city DESC and shows Esha last in DuckDB. someone reruns it on Postgres. what do they see, and what is the fix?

<details><summary>answer</summary>

Esha moves to the top, since Postgres sorts null as larger and DESC puts larger first. the fix is writing NULLS LAST in the query, so both databases agree. the tempting answer is "same output, its the same SQL", but the default isnt part of what you wrote.

</details>

---
prev: [118 no ORDER BY, no promised order](./118-no-order-by-no-promised-order.md) | next: [120 LIMIT and OFFSET, paging through rows](./120-limit-and-offset-paging-through-rows.md)
