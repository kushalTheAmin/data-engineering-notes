# 118: no ORDER BY, no promised order
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [101 SQL, you describe the result, the database figures out how](./101-sql-you-describe-the-result.md), [104 SELECT and FROM, picking columns](./104-select-and-from-picking-columns.md), [117 ORDER BY, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md)
section: asking questions with SQL, part 18, ~2 min read

i assumed a query with no ORDER BY hands rows back in table order, every time. would you have trusted that too?

it isnt a promise. without [ORDER BY](./117-order-by-sorting-by-one-or-more-columns.md) (the clause that sorts rows), a [query](./101-sql-you-describe-the-result.md) may return rows in any order it likes. here is the products [table](./079-a-table-rows-are-records-columns-are-fields.md) of the shop, the imaginary gujarati snack store these notes run on, in DuckDB, the database these notes run their SQL in:

```sql
SELECT name, category FROM products
```

```result
name | category
dhokla | snack
khandvi | snack
jalebi | sweet
kaju katli | sweet
masala chai | drink
fafda | snack
```

tidy here, but thats just the order the rows were stored, and DuckDB isnt promising it. think of the table as a bag of rows (a list has an order, a bag doesnt), and two ways of pulling them out are both correct (dhokla, a steamed savory cake, khandvi and fafda, chickpea flour snacks, jalebi, a syrupy sweet, kaju katli, a cashew sweet):

```python
rows = ["dhokla", "khandvi", "jalebi", "kaju katli", "masala chai", "fafda"]
plan_a = list(rows)
plan_b = list(reversed(rows))
print(plan_a)
print(plan_b)
print(sorted(plan_a) == sorted(plan_b))
```

```output
['dhokla', 'khandvi', 'jalebi', 'kaju katli', 'masala chai', 'fafda']
['fafda', 'masala chai', 'kaju katli', 'jalebi', 'khandvi', 'dhokla']
True
```

same rows, different order, and SQL allows both. Postgres, a server database, says in its docs that the order then depends on how it fetches the rows, and must not be relied on. i expected a boring default, and its really "whatever was fastest". the classic bug is a report that works on a small table, then the data grows, the database fetches rows another way, and the order flips.

it bites even with ORDER BY: sorting by category alone leaves the 3 snacks tied, and a tie has no promised order either, so add a second column, as [117](./117-order-by-sorting-by-one-or-more-columns.md) did, here just to settle ties.

### check yourself

1. a test says "ORDER BY category puts dhokla, then khandvi, then fafda" and passes today. whats wrong with it, and what would you write?

<details><summary>answer</summary>

the three snacks tie on category, so their order isnt promised and the test can break any day. add a column that tells them apart, like name:

```sql
SELECT name FROM products ORDER BY category, name
```

```result
name
masala chai
dhokla
fafda
khandvi
jalebi
kaju katli
```

the tempting answer is "its fine, it passed", but passing once proves nothing about a promise.

</details>

2. a friend runs one query with no ORDER BY on a laptop and on a server, gets two orders, and says one database is broken. who is right?

<details><summary>answer</summary>

neither is broken, both orders are legal because no order was asked for. the tempting answer is blaming a bug in one of them, but even identical data can come back in different orders.

</details>

---
prev: [117 ORDER BY, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md) | next: not written yet
