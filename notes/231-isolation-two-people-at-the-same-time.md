# 231: isolation, two people at the same time
builds on: [229 ACID, four promises a database makes](./229-acid-four-promises-a-database-makes.md), [228 COMMIT and ROLLBACK, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md), [227 transactions, all or nothing](./227-transactions-all-or-nothing.md), [212 connections and sessions, one conversation with the database](./212-connections-and-sessions-one-conversation-with-the-database.md)
section: changing data safely, part 24, ~2 min read

Esha is halfway through placing order 108 and Asha counts the orders at that exact moment. does Asha get 7 or 8? the answer is a rule, not luck.

isolation, the third promise in [ACID](./229-acid-four-promises-a-database-makes.md) (four promises a database makes about changes), means [transactions](./227-transactions-all-or-nothing.md) (changes that all happen or none do) running at the same time dont see each others unfinished work. the shop, the imaginary gujarati snack store these notes run on, has Asha and Esha each on their own [connection](./212-connections-and-sessions-one-conversation-with-the-database.md), an open line to the database:

```python
import duckdb
db = duckdb.connect()
db.execute("CREATE TABLE my_orders AS SELECT 101 + range AS order_id FROM range(7)")
asha = db.cursor()
esha = db.cursor()
count = lambda who: who.execute("SELECT count(*) FROM my_orders").fetchone()[0]

esha.execute("BEGIN")
esha.execute("INSERT INTO my_orders VALUES (108)")
print("esha, mid transaction:", count(esha))
print("asha, same moment:", count(asha))
esha.execute("ROLLBACK")
print("asha, after esha rolls back:", count(asha))
esha.execute("BEGIN")
esha.execute("INSERT INTO my_orders VALUES (108)")
esha.execute("COMMIT")
print("asha, after esha commits:", count(asha))
```

```output
esha, mid transaction: 8
asha, same moment: 7
asha, after esha rolls back: 7
asha, after esha commits: 8
```

Esha sees her own 108 straight away, Asha doesnt, and nobody made Asha wait. i expected the database to hold her query until Esha finished, but she just gets the last finished picture, 7. if Esha had rolled back, Asha would never have counted an order that vanished. only [COMMIT](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md) (keep the changes) puts 108 in front of Asha.

this is the promise that makes a dashboard trustworthy while orders pour in. but isolation isnt on or off, you pick how strict it is. Postgres, a database that runs as its own server, defaults to read committed: unfinished work stays hidden, but a count can change between two of your own queries. its strictest level, serializable, makes transactions act as if they ran one after another.

### check yourself

1. Disha opens a transaction, sets order 105 to cancelled, and hasnt committed. Bhavin counts delivered orders on his own connection. what does he get, and why not 4?

```sql
SELECT count(*) AS delivered FROM orders WHERE status = 'delivered'
```

<details><summary>answer</summary>

```result
delivered
5
```

5, the picture from before Dishas change. 4 is tempting because her update already "happened" on her side, but until COMMIT nobody else sees it.

</details>

2. on Postgres defaults, Asha counts orders, Esha commits order 108, then Asha counts again, all inside Ashas one transaction. 7 then 7, or 7 then 8? is that an isolation failure?

<details><summary>answer</summary>

7 then 8. each query at read committed sees whatever was committed when it started, so the second sees 108. not a failure, just the default level. the tempting 7 then 7 needs a stricter level.

</details>

---
prev: [230 ACID consistency, the rules still hold after every change](./230-acid-consistency-the-rules-still-hold-after-every-change.md) | next: not written yet
