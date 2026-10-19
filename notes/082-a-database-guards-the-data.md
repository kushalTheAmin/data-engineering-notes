# 082: a database, a program that guards your data
builds on: [039 a file is a named list of bytes](./039-a-file-is-a-named-list-of-bytes.md), [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [081 why a shared spreadsheet breaks when many people use it](./081-why-a-shared-spreadsheet-breaks.md)
section: tables, keys and relationships, part 4, ~2 min read

what if nobody was allowed to save the file at all? in [081](./081-why-a-shared-spreadsheet-breaks.md) Bhavins save wiped out Ashas fix to order 106, a lost update, because he wrote back a whole stale copy.

a database is a program that owns the [files](./039-a-file-is-a-named-list-of-bytes.md) holding your [tables](./079-a-table-rows-are-records-columns-are-fields.md). nobody else opens them. you send it a small request, and it changes its one copy. here it is as a toy in python, with the same two orders from 081 (a slice: 106 pending, 107 delivered):

```python
class Database:
    def __init__(self, rows):
        self.rows = rows

    def set_status(self, order_id, status):
        for r in self.rows:
            if r["order_id"] == order_id:
                r["status"] = status

db = Database([
    {"order_id": 106, "status": "pending"},
    {"order_id": 107, "status": "delivered"},
])
db.set_status(106, "delivered")  # Asha
db.set_status(107, "returned")   # Bhavin
print(db.rows)
```

```output
[{'order_id': 106, 'status': 'delivered'}, {'order_id': 107, 'status': 'returned'}]
```

| | shared file | database |
|---|---|---|
| who writes the file | everyone | only the program |
| what you send | the whole table | one change |
| what a stale copy can do | overwrite other peoples rows | nothing, you never hold one |

both fixes survived. Asha and Bhavin never held a copy, they each asked for one row to change, and the program applied the requests one after another to the current data. i kept looking for the clever lock and the trick is smaller than that: stop letting people write the file.

caveat, if both change the same row, the later request still wins. the difference is that it only touches the row it names, so nobody loses work they never edited.

Postgres and MySQL are databases in this sense (SQLite runs inside the program using it, so it is the exception), and real ones do far more than this toy: crashes, speed, many requests at once. but "one program guards the files" is the part everything else hangs on.

how do those requests actually reach it? thats a later note.

---
prev: [081 why a shared spreadsheet breaks when many people use it](./081-why-a-shared-spreadsheet-breaks.md) | next: [083 schema on write vs schema on read](./083-schema-on-write-vs-schema-on-read.md)
