# 168: self join, a table joined to itself
builds on: [031 null, a marker for a missing value](./031-null.md), [155 why joins, the answer lives in more than one table](./155-why-joins-the-answer-lives-in-more-than-one-table.md), [157 ON, how a join decides which rows match](./157-on-how-a-join-decides-which-rows-match.md), [158 table aliases, short nicknames for tables](./158-table-aliases-short-nicknames-for-tables.md), [166 joining on columns that can be NULL](./166-joining-on-columns-that-can-be-null.md)
section: combining tables with joins, part 14, ~2 min read

which customers live in the same city as another customer? every name and every city sits in one table (rows and columns), so what do you join it to?

to itself. a join pairs up rows of two tables, and a self join is a table paired with a copy of itself, and the copy is just the same table under a second [alias](./158-table-aliases-short-nicknames-for-tables.md) (a short nickname for one query). start with the loop inside a loop from [155](./155-why-joins-the-answer-lives-in-more-than-one-table.md), except both loops walk the shop (the imaginary gujarati snack store these notes run on) customers:

```python
customers = [
    {"name": "Asha", "city": "Jersey City"},
    {"name": "Bhavin", "city": "Edison"},
    {"name": "Chirag", "city": "Jersey City"},
    {"name": "Disha", "city": "Hoboken"},
    {"name": "Esha", "city": None},
]
for a in customers:
    for b in customers:
        if a["city"] is not None and a["city"] == b["city"]:
            print(a["name"], b["name"])
```

```output
Asha Asha
Asha Chirag
Bhavin Bhavin
Chirag Asha
Chirag Chirag
Disha Disha
```

6 lines, and only one idea in there is what i wanted. 4 are a customer paired with herself, and Asha Chirag comes back mirrored as Chirag Asha. Esha is missing because her city is [NULL](./031-null.md) (a missing value) and [166](./166-joining-on-columns-that-can-be-null.md) showed a NULL never matches. the fix is a second test in [ON](./157-on-how-a-join-decides-which-rows-match.md), which takes any test, not only equals:

```sql
SELECT a.name, b.name AS lives_near FROM customers a JOIN customers b ON a.city = b.city AND a.customer_id < b.customer_id
```

```result
name | lives_near
Asha | Chirag
```

customer_id is each customers unique number, Asha is 1 and Chirag is 3. nobody has a smaller id than herself, so the 4 self pairs are dropped, and of Asha Chirag and Chirag Asha only the first has the smaller id on the left, so the mirror is dropped too. i assumed the database needed a real second copy of the table, and its one table with two nicknames.

another classic use is a people table where each row holds its mothers id, so child and mother are the same table joined to itself.

---
prev: [167 anti join, rows with no match](./167-anti-join-rows-with-no-match.md) | next: not written yet
