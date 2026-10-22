# 162: right and full outer joins
builds on: [031 null, a marker for a missing value](./031-null.md), [124 text functions, lower, upper, length and trim](./124-text-functions-lower-upper-length-and-trim.md), [159 left join, keep every row from the left table](./159-left-join-keep-every-row-from-the-left-table.md), [160 the nulls a left join creates](./160-the-nulls-a-left-join-creates.md)
section: combining tables with joins, part 8, ~2 min read

a left join protects one side. what if the rows you care about sit unmatched on both?

a full join is a [left join](./159-left-join-keep-every-row-from-the-left-table.md) (keeps every row of the first table) that also keeps unmatched right rows, with [NULL](./031-null.md) (a missing value) on the left. a right join keeps only the unmatched right rows, so it is a left join with the two tables swapped. the shop (the imaginary gujarati snack store these notes run on) has its 5 customers and a signups table (names as typed into the form). here is 159s loop plus one more loop, matching on name:

```python
customers = ["Asha", "Bhavin", "Chirag", "Disha", "Esha"]
signups = ["Asha", "bhavin ", "CHIRAG ", "Disha"]
used = []
for c in customers:
    found = False
    for s in signups:
        if c == s:
            print((s, c))
            found = True
            used.append(s)
    if not found:
        print((None, c))
for s in signups:
    if s not in used:
        print((s, None))
```

```output
('Asha', 'Asha')
(None, 'Bhavin')
(None, 'Chirag')
('Disha', 'Disha')
(None, 'Esha')
('bhavin ', None)
('CHIRAG ', None)
```

the last loop is the only new part. in SQL it is one word, with quote marks added so the stray spaces show:

```sql
SELECT '"' || s.typed_name || '"' AS typed, c.name FROM customers c FULL JOIN signups s ON c.name = s.typed_name ORDER BY c.name, s.typed_name
```

```result
typed | name
"Asha" | Asha
NULL | Bhavin
NULL | Chirag
"Disha" | Disha
NULL | Esha
"CHIRAG " | NULL
"bhavin " | NULL
```

7 rows, which is 5 customers plus 4 signups minus the 2 pairs that matched. i expected a join to have a favorite side, and a full join just doesnt. it shows both halves of one failure: Bhavin and "bhavin " look like the same person, but a capital letter and a stray space stop the match, so each lands alone with a NULL. [124](./124-text-functions-lower-upper-length-and-trim.md) has the fix, lower and trim.

with right join, `signups s RIGHT JOIN customers c` gives the 5 customer rows, same as customers on the left. i just swap the tables and use LEFT, so joins always read one way.

a full join also compares two lists: a NULL on one side means the other list lacks that row.

---
prev: [161 a WHERE that quietly turns a left join into an inner join](./161-a-where-that-quietly-turns-a-left-join-into-an-inner-join.md) | next: not written yet
