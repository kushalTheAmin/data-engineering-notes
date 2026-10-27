# 235: lost updates
builds on: [231 isolation, two people at the same time](./231-isolation-two-people-at-the-same-time.md), [222 UPDATE, changing rows and why the WHERE matters](./222-update-changing-rows-and-why-the-where-matters.md), [227 transactions, all or nothing](./227-transactions-all-or-nothing.md), [212 connections and sessions, one conversation with the database](./212-connections-and-sessions-one-conversation-with-the-database.md), [081 why a shared spreadsheet breaks when many people use it](./081-why-a-shared-spreadsheet-breaks.md)
section: changing data safely, part 28, ~2 min read

10 dhokla are left at the shop, the imaginary gujarati snack store these notes run on. Asha and Bhavin each buy one at the same moment. the stock should say 8, and it says 9, with no error anywhere.

thats a lost update: two people read the same number, each works out a new one from it, and the later write erases the earlier. its the same bug as the file in [081](./081-why-a-shared-spreadsheet-breaks.md), now inside a database. here are two [connections](./212-connections-and-sessions-one-conversation-with-the-database.md) (open lines to the database), run both ways:

```python
import duckdb
db = duckdb.connect()
db.execute("CREATE TABLE stock (product VARCHAR, left_over INTEGER)")
db.execute("INSERT INTO stock VALUES ('dhokla', 10)")
asha, bhavin = db.cursor(), db.cursor()
read = lambda who: who.execute("SELECT left_over FROM stock").fetchone()[0]

# way 1: read it, do the subtraction in python, write the answer back
a = read(asha)
b = read(bhavin)
asha.execute(f"UPDATE stock SET left_over = {a - 1}")
bhavin.execute(f"UPDATE stock SET left_over = {b - 1}")
print("read then write:", read(asha))

# way 2: hand the subtraction to the database
db.execute("UPDATE stock SET left_over = 10")
asha.execute("UPDATE stock SET left_over = left_over - 1")
bhavin.execute("UPDATE stock SET left_over = left_over - 1")
print("one UPDATE each:", read(asha))
```

```output
read then write: 9
one UPDATE each: 8
```

in way 1 both read 10 before either wrote, so both wrote 9. i figured [isolation](./231-isolation-two-people-at-the-same-time.md) was the whole fix, but nothing unfinished was hidden here: both reads were of a real, committed 10. isolation hides half done work, it doesnt notice two people building on the same stale number.

way 2 works because the number never visits python. as in [222](./222-update-changing-rows-and-why-the-where-matters.md), `left_over - 1` reads the current value when the UPDATE runs. my demo runs one after the other, but the Postgres docs say that at [read committed](./231-isolation-two-people-at-the-same-time.md), the Postgres default, a second UPDATE of the same row waits for the first to commit, then applies to the new row.

so what: if you ever write code that SELECTs a value, calculates, then UPDATEs it, you can lose updates.

### check yourself

1. two apps read the price of dhokla, 6.00. the app of Asha adds 1 and the app of Bhavin adds 0.50. if both compute in python and write, what ends up stored if Bhavin writes last? and if each sends `SET price = price + ...` instead?

```sql
SELECT price + 1 + 0.5 AS both_added FROM products WHERE name = 'dhokla'
```

<details><summary>answer</summary>

```result
both_added
7.50
```

that 7.50 is the SQL way. the python way stores 6.50, since Bhavin never saw Ashas 7.00 and Ashas rise is lost. 7.50 for python is the tempting wrong answer.

</details>

2. 1 jalebi is left. two buyers each check `left_over > 0`, see 1, then both run `SET left_over = left_over - 1`. what is stored, with nothing else guarding it?

<details><summary>answer</summary>

-1. the subtraction is safe, but the check ran on the old 1. the tempting 0 forgets the check and the update are separate steps. a CHECK rule or a WHERE left_over > 0 on the UPDATE closes it.

</details>

---
prev: [234 replaying the log after a crash](./234-replaying-the-log-after-a-crash.md) | next: [236 dirty reads](./236-dirty-reads.md)
