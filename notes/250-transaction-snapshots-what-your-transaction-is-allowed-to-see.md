# 250: transaction snapshots, what your transaction is allowed to see
builds on: [249 MVCC, an update writes a new row version](./249-mvcc-an-update-writes-a-new-row-version.md), [240 repeatable read, rows dont change under you mid transaction](./240-repeatable-read-rows-dont-change-under-you-mid-transaction.md), [239 isolation levels, read committed](./239-isolation-levels-read-committed.md), [227 transactions, all or nothing](./227-transactions-all-or-nothing.md), [228 COMMIT and ROLLBACK, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md)
section: changing data safely, part 43, ~2 min read

Asha is changing order 106 in transaction 739, not committed yet. Bhavin starts later as 740, adds order 108 and commits. Esha sees 108 but not Ashas change, so does the bigger transaction id win? how does Postgres (a database that runs as its own server) decide?

with a snapshot: Postgres noting which [transactions](./227-transactions-all-or-nothing.md) (groups of changes that all happen or none do) had finished when a query began. a [row version](./249-mvcc-an-update-writes-a-new-row-version.md) (one stored copy of a row) is visible if its creator, the xmin transaction, had committed and its ender, the xmax one, hadnt. the shop, the imaginary snack store these notes run on, 108 imagined:

```python
def done(x, snap):
    return x < snap["xmin"] or (x < snap["xmax"] and x not in snap["running"])

def visible(v, snap):
    slot, order, status, xmin, xmax = v
    return done(xmin, snap) and not (xmax != 0 and done(xmax, snap))

versions = [
    (6, 106, "pending", 738, 739),
    (7, 107, "delivered", 738, 0),
    (8, 106, "delivered", 739, 0),
    (9, 108, "pending", 740, 0),
]
first = {"xmin": 739, "xmax": 741, "running": [739]}
later = {"xmin": 741, "xmax": 741, "running": []}

print("slot order status     first  later")
for v in versions:
    print(f"{v[0]:<4} {v[1]:<5} {v[2]:<10} {str(visible(v, first)):<6} {visible(v, later)}")
```

```output
slot order status     first  later
6    106   pending    True   False
7    107   delivered  True   True
8    106   delivered  False  True
9    108   pending    True   True
```

Eshas first snapshot prints as 739:741:739 (xmin, xmax, running ids): everything below 739 is finished, nothing from 741 up is, and 739 is still running. that xmin means lowest running id, not the row stamp from 249. ids are numbered in order but transactions finish in any order. at read committed Esha gets the later snapshot once 739 commits. at [repeatable read](./240-repeatable-read-rows-dont-change-under-you-mid-transaction.md) she keeps the first.

caveats: finished can mean rolled back, which my code counts as committed, and it ignores that you always see your own changes.

i assumed a bigger id meant newer, but a snapshot is a list of whos done, not a timeline.

so what: the Postgres docs say a version stays while another transaction may still see it, so a long query or open repeatable read transaction holds its snapshot and VACUUM (cleanup) cant remove them.

### check yourself

1. Esha takes the snapshot 739:741:739. right after, Bhavin commits transaction 741, which adds an imagined order 109. does Esha see 109 in her next query at repeatable read (one snapshot kept all transaction)? at read committed (a new snapshot per query)?

<details><summary>answer</summary>

repeatable read: no, 741 is not below xmax 741, so it hadnt finished when her snapshot was taken, and she keeps that snapshot. read committed: yes, her next query takes a new snapshot. the tempting yes for both reads "committed" as "visible", but visible depends on the snapshot.

</details>

2. same setup as the note, but Bhavins transaction 740 ends with ROLLBACK, not COMMIT. Esha takes a new snapshot afterwards. the code above says slot 9 is visible. what does Postgres show Esha?

<details><summary>answer</summary>

no. 740 finished, so the code says visible, but a rolled back transaction never counts, which is the caveat. the tempting yes trusts the code, which only models finished transactions that committed.

</details>

---
prev: [249 MVCC, an update writes a new row version](./249-mvcc-an-update-writes-a-new-row-version.md) | next: [251 backups, a copy you can restore from](./251-backups-a-copy-you-can-restore-from.md)
