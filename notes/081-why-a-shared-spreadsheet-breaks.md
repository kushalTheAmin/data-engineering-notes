# 081: why a shared spreadsheet breaks when many people use it
builds on: [039 a file is a named list of bytes](./039-a-file-is-a-named-list-of-bytes.md), [046 writing safely, write a new file then rename it](./046-writing-safely.md), [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md)
section: tables, keys and relationships, part 3, ~2 min read

two people each fix one row of the same shared file, both save, and one fix is just gone. no error, no warning. how?

in [080](./080-every-column-holds-one-type.md) a [table](./079-a-table-rows-are-records-columns-are-fields.md) fixed what goes in each column. but a table kept as a plain [file](./039-a-file-is-a-named-list-of-bytes.md), like a spreadsheet or csv on a shared drive, has no guard, and saving it means writing the whole file back. the shop, the imaginary gujarati snack store these notes run on, keeps a slice of orders that way: 106 pending and 107 delivered. Asha and Bhavin both open it, each gets their own copy in memory, and each fixes a different row.

| step | Asha has | Bhavin has | file on disk |
|---|---|---|---|
| both open it | 106 pending, 107 delivered | 106 pending, 107 delivered | 106 pending, 107 delivered |
| Asha sets 106 delivered, saves | 106 delivered, 107 delivered | 106 pending, 107 delivered | 106 delivered, 107 delivered |
| Bhavin sets 107 returned, saves | 106 delivered, 107 delivered | 106 pending, 107 returned | 106 pending, 107 returned |

the last row is the bug. Bhavins copy never saw Ashas change, so saving it wrote 106 back as pending. here it is as code, using the [safe write](./046-writing-safely.md) (new file, then rename):

```python
import os, tempfile
path = os.path.join(tempfile.mkdtemp(), "orders.csv")
with open(path, "w") as f:
    f.write("106,pending\n107,delivered\n")

def load():
    return [line.split(",") for line in open(path).read().split("\n") if line]

def save(rows):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write("".join(",".join(r) + "\n" for r in rows))
    os.replace(tmp, path)

asha, bhavin = load(), load()
asha[0][1] = "delivered"
bhavin[1][1] = "returned"
save(asha)
save(bhavin)
print(open(path).read().strip())
```

```output
106,pending
107,returned
```

i assumed the safe write from 046 would cover this, and it doesnt. that fixes a torn file, every save here is whole and clean, it just replaces the other one. the name is a lost update, last save wins.

every editor works on a stale copy and nothing checks. you only notice when someone asks why 106 is still pending. what you want is one program standing between everyone and the file, taking each change one at a time. thats what a database is.

---
prev: [080 every column holds one type](./080-every-column-holds-one-type.md) | next: [082 a database, a program that guards your data](./082-a-database-guards-the-data.md)
