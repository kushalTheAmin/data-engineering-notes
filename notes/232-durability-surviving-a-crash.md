# 232: durability, surviving a crash
builds on: [229 ACID, four promises a database makes](./229-acid-four-promises-a-database-makes.md), [228 COMMIT and ROLLBACK, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md), [036 memory vs disk, one forgets and one remembers](./036-memory-vs-disk.md), [037 disk is slow, memory vs SSD vs spinning disk in real numbers](./037-disk-is-slow.md)
section: changing data safely, part 25, ~2 min read

Esha orders from the shop, the imaginary snack store these notes run on, and gets "order saved". a blink later the power dies. is order 108 still there? it depends on what the database did before it said saved.

durability, the last promise in [ACID](./229-acid-four-promises-a-database-makes.md) (four promises a database makes), means once [COMMIT](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md) (the command that keeps your changes) reports done, a crash cant undo it. a crash is anything that wipes [memory](./036-memory-vs-disk.md), the working space that forgets at power off. only [disk](./036-memory-vs-disk.md), storage that keeps bytes without power, survives. so "done" has to wait until the change is flushed, forced onto disk. this is about Postgres.

| step | 108 on disk | Esha told done | crash right now |
| --- | --- | --- | --- |
| COMMIT arrives | no | no | 108 lost, nobody lied to |
| flush finishes | yes | no | 108 stays |
| done sent | yes | yes | 108 stays |
| wrong order: done sent first | no | yes | 108 lost, Esha lied to |

the order of the steps is the whole promise. say done first and flush later, and a crash in between leaves her holding a confirmation for an order that doesnt exist. i figured saving was one instant, but the database has to pick an order between telling Esha and writing it down.

so what: every commit waits on a [slow disk](./037-disk-is-slow.md), and for short transactions the Postgres docs call that wait a major part of the time. Postgres has a setting, synchronous_commit, on by default. turn it off and it says done without waiting, and the docs say a crash can lose the last few commits, but not corrupt anything: the database looks as if they were cleanly cancelled.

what gets flushed is a log of the change, not the table files. a later note covers why.

---
prev: [231 isolation, two people at the same time](./231-isolation-two-people-at-the-same-time.md) | next: not written yet
