# 169: cross join, every row with every row
builds on: [155 why joins, the answer lives in more than one table](./155-why-joins-the-answer-lives-in-more-than-one-table.md), [157 ON, how a join decides which rows match](./157-on-how-a-join-decides-which-rows-match.md), [158 table aliases, short nicknames for tables](./158-table-aliases-short-nicknames-for-tables.md), [167 anti join, rows with no match](./167-anti-join-rows-with-no-match.md)
section: combining tables with joins, part 15, ~2 min read

what does a join return when you give it no test at all? i expected an error.

a plain JOIN with no ON is a syntax error in DuckDB, so you ask for it by name. written as CROSS JOIN, it returns every row of one table paired with every row of the other. [157](./157-on-how-a-join-decides-which-rows-match.md) got there with an [ON](./157-on-how-a-join-decides-which-rows-match.md) that was always true (the test that decides which pairs stay). a cross join is the same thing on purpose, so the loop inside a loop from [155](./155-why-joins-the-answer-lives-in-more-than-one-table.md) just loses its `if`. a slice of the shop (the imaginary gujarati snack store these notes run on), 2 customers and 3 products:

```python
customers = ["Asha", "Bhavin"]
products = ["dhokla", "khandvi", "jalebi"]
for c in customers:
    for p in products:
        print(c, p)
```

```output
Asha dhokla
Asha khandvi
Asha jalebi
Bhavin dhokla
Bhavin khandvi
Bhavin jalebi
```

2 customers times 3 products, 6 lines, nothing dropped. in SQL there is no ON to write, and the full tables, using the [aliases](./158-table-aliases-short-nicknames-for-tables.md) c and p (short nicknames):

```sql
SELECT count(*) AS pairs, count(DISTINCT c.name) AS customers, count(DISTINCT p.name) AS products FROM customers c CROSS JOIN products p
```

```result
pairs | customers | products
30 | 5 | 6
```

5 times 6. the row count is the two row counts multiplied, so 10,000 rows crossed with 10,000 rows is 100 million, which is why an accidental one can hang a query. writing `FROM customers, products` with a comma is the same cross join, and the Postgres docs (a server database) say so.

so why ever do it on purpose? it builds every combination that could happen. only 10 of those 30 customer and product pairs were ever ordered, so 20 never happened, and an [anti join](./167-anti-join-rows-with-no-match.md) (keeps rows with no match) on top of the cross join lists them, Esha with all 6.

---
prev: [168 self join, a table joined to itself](./168-self-join-a-table-joined-to-itself.md) | next: [170 joining on a range, matching a date to a period](./170-joining-on-a-range-matching-a-date-to-a-period.md)
