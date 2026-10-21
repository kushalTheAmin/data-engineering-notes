# 135: one language, many dialects
builds on: [101 SQL, you describe the result, the database figures out how](./101-sql-you-describe-the-result.md), [102 a database in one file, setting up DuckDB](./102-a-database-in-one-file.md), [119 where NULLs land when you sort](./119-where-nulls-land-when-you-sort.md), [120 LIMIT and OFFSET, paging through rows](./120-limit-and-offset-paging-through-rows.md), [125 concatenating text, and taking pieces of it](./125-concatenating-text-and-taking-pieces-of-it.md), [131 integer division, when 7 / 2 gives 3](./131-integer-division-when-7-divided-by-2-gives-3.md)
section: asking questions with SQL, part 35, ~2 min read

i copied a LIMIT 2 query from a tutorial into another database and got a syntax error on a line that looked perfectly fine. so is SQL one language or not?

a dialect is one databases own version of [SQL](./101-sql-you-describe-the-result.md) (the language you send a database to ask for rows). there is a written standard, but almost no database follows it fully, and each adds its own spellings. the core, SELECT, FROM, WHERE, ORDER BY, reads the same nearly everywhere. the edges are where it splits. one ask on the shop, the imaginary gujarati snack store these notes run on: the 2 priciest products.

| database | how it says "first 2 rows" |
|---|---|
| the SQL standard | FETCH FIRST 2 ROWS ONLY |
| Postgres, a server database | LIMIT 2, or the standard one |
| MySQL, another server database | LIMIT 2 |
| SQL Server, Microsofts server database | SELECT TOP 2 name, price, or the standard one after OFFSET 0 ROWS |
| [DuckDB](./102-a-database-in-one-file.md), the one these notes run | LIMIT 2, or the standard one |

so the standard one runs here too, and gives what [LIMIT](./120-limit-and-offset-paging-through-rows.md) did:

```sql
SELECT name, price FROM products ORDER BY price DESC FETCH FIRST 2 ROWS ONLY
```

```result
name | price
kaju katli | 12.00
khandvi | 7.50
```

```text
-- SQL Server, not DuckDB
SELECT TOP 2 name, price FROM products ORDER BY price DESC;
```

i assumed a standard meant everyone follows it, and LIMIT, the one i use daily, isnt even in it. the Postgres docs call LIMIT and OFFSET Postgres-specific syntax that MySQL also uses.

and this was far from the first time. [131](./131-integer-division-when-7-divided-by-2-gives-3.md) had / differ, [125](./125-concatenating-text-and-taking-pieces-of-it.md) had || differ, [119](./119-where-nulls-land-when-you-sort.md) had nulls sorting differently. when a note says "in DuckDB", that is often a dialect warning.

so when you move a query between databases, the core survives and the edges are what you recheck, and a tutorial for one database is only a tutorial for that one.

---
prev: [134 the order SQL really runs in](./134-the-order-sql-really-runs-in.md) | next: [136 capstone, one query traced clause by clause](./136-capstone-one-query-traced-clause-by-clause.md)
