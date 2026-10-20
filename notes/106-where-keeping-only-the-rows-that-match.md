# 106: WHERE, keeping only the rows that match
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [101 SQL, you describe the result, the database figures out how](./101-sql-you-describe-the-result.md), [104 SELECT and FROM, picking columns](./104-select-and-from-picking-columns.md)
section: asking questions with SQL, part 6, ~2 min read

can you filter on a column you never ask to see? i assumed not, because the filter would need that column in the answer.

WHERE keeps only the [rows](./079-a-table-rows-are-records-columns-are-fields.md) (one record each) where its condition is true, and drops the rest. [101](./101-sql-you-describe-the-result.md) used it once in SQL (the language for asking a database for rows), this is what it does underneath. the shop, the imaginary gujarati snack store these notes run on, has 7 orders. here is what WHERE status = 'delivered' does to them:

| order_id | status | kept? |
|---|---|---|
| 101 | delivered | yes |
| 102 | delivered | yes |
| 103 | delivered | yes |
| 104 | cancelled | no |
| 105 | delivered | yes |
| 106 | pending | no |
| 107 | delivered | yes |

```sql
SELECT order_id FROM orders WHERE status = 'delivered'
```

```result
order_id
101
102
103
105
107
```

status is not in the answer, and it still worked. WHERE is the if inside the loop from 101. it looks at the whole row, keeps or skips it, and only then does [SELECT](./104-select-and-from-picking-columns.md) (which columns to keep) pick from the survivors. so the order of work is FROM (which table to read), WHERE, SELECT, even though you write SELECT first.

rows 104 and 106 are gone, not blanked. the match is exact text, so 'Delivered' with a capital D matches nothing and you get zero rows, not an error.

i assumed the filter could only see what i was about to get back, and it sees the whole row.

a typo in a value gives you an empty result instead of an error. the = in the condition means exactly equal, and there are other tests besides that one.

### check yourself

1. products stores categories in lowercase, like 'snack'. a teammate runs the query below to list the snack products. how many rows come back, and does it error?

```sql
SELECT name FROM products WHERE category = 'Snack'
```
<details><summary>answer</summary>

```result
name
```

zero rows and no error. the stored value is 'snack' in lowercase, so the capital S never matches. the tempting answer is 3, from reading 'Snack' as the same word.

</details>

2. delivered orders belong to customers 1, 2, 1, 4 and 2. without running it, how many rows does this return, and why not 3?

```sql
SELECT customer_id FROM orders WHERE status = 'delivered'
```
<details><summary>answer</summary>

```result
customer_id
1
2
1
4
2
```

5 rows. WHERE keeps whole rows (5 orders are delivered), then SELECT picks one column from each, and a plain SELECT never merges repeats (see 104). the tempting answer is 3, from thinking of the distinct customers.

</details>

---
prev: [105 SELECT star, every column, and why you rarely want it](./105-select-star-every-column.md) | next: not written yet
