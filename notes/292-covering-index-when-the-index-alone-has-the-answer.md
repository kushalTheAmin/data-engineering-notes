# 292: covering index, when the index alone has the answer
builds on: [291 the leftmost prefix rule, which questions a composite index can answer](./291-the-leftmost-prefix-rule-which-questions-a-composite-index-can-answer.md), [290 composite indexes, sorted by the first column, then the second](./290-composite-indexes-sorted-by-the-first-column-then-the-second.md), [286 index, a sorted shortcut to rows](./286-index-a-sorted-shortcut-to-rows.md), [284 how Postgres keeps a table on disk, rows packed into pages](./284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md)
section: inside a database server, part 9, ~2 min read

[291](./291-the-leftmost-prefix-rule-which-questions-a-composite-index-can-answer.md) was about which questions get the jump. but once the index finds Ashas entries, do you always have to go fetch the rows, even when the entry already shows what you asked for?

a covering index is an index that holds every column a query needs, so the answer comes straight out of the entries and the table is never touched. the same index covers one question and not another.

the shop, the imaginary gujarati snack store these notes run on. the index is the [composite index](./290-composite-indexes-sorted-by-the-first-column-then-the-second.md) on (customer_id, ordered_at), with order_id standing in for each rows [address](./284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md) in the table. two questions about Asha, customer 1:

```python
index = [
    (1, "2026-04-01 09:15:00", 101), (1, "2026-04-03 12:05:00", 103),
    (1, "2026-04-08 10:00:00", 106),
]
table = {101: "delivered", 103: "delivered", 106: "pending"}

def ask(column):
    answers, trips = [], 0
    for customer_id, ordered_at, order_id in index:
        if column == "ordered_at":
            answers.append(ordered_at)
        else:
            answers.append(table[order_id])
            trips += 1
    return len(answers), trips

print("SELECT ordered_at WHERE customer_id = 1:", "%d answers, %d trips to the table" % ask("ordered_at"))
print("SELECT status WHERE customer_id = 1:", "%d answers, %d trips to the table" % ask("status"))
```

```output
SELECT ordered_at WHERE customer_id = 1: 3 answers, 0 trips to the table
SELECT status WHERE customer_id = 1: 3 answers, 3 trips to the table
```

both find the same 3 entries. ordered_at is sitting in each one, so the first question reads and stops. status isnt in the index, so each entry costs a trip: follow the address, read a table page. at 7 rows that is nothing, on a big table those trips are the bill.

i assumed an index only ever pointed at the answer, but sometimes the index is the answer.

in Postgres, a database server, this is called an index-only scan, and INCLUDE adds a column to each entry without sorting by it:

```text
-- Postgres 16
CREATE INDEX orders_cust_idx ON orders (customer_id) INCLUDE (ordered_at);
```

one catch: Postgres only skips the table for pages it knows hold no recent changes, and visits the table for the rest. SELECT * almost never gets covered, since the index would need every column.

each extra column makes the entries fatter, and thats a bill too.

---
prev: [291 the leftmost prefix rule, which questions a composite index can answer](./291-the-leftmost-prefix-rule-which-questions-a-composite-index-can-answer.md) | next: [293 what indexes cost, slower writes and more disk](./293-what-indexes-cost-slower-writes-and-more-disk.md)
