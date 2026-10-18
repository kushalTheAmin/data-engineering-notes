# 051: the operating system, the program that shares the machine out
builds on: [035 the processor, the part that does the work](./035-the-processor.md), [036 memory vs disk, one forgets and one remembers](./036-memory-vs-disk.md), [050 processes, a program while it runs](./050-processes.md)
section: memory, disks and files, part 17, ~2 min read

if the shop runs its order loader and a report at the same time, but the machine has one processor core, who is doing which?

the operating system is the software that starts programs and shares the machine between them. it hands out the [processor](./035-the-processor.md), the part doing tiny steps on numbers, in short turns (slices of time), and it does the same for [memory](./036-memory-vs-disk.md), the working space that forgets at power off. every [process](./050-processes.md), one running copy of a program, gets its turn.

the shop, the imaginary gujarati snack store these notes run on, loads orders with one process and builds a report with another. say the loader needs 3 turns of work and the report needs 2, and the system alternates evenly (real ones dont, this is simplified):

| turn | on the processor | loader left | report left |
|---|---|---|---|
| start | | 3 | 2 |
| 1 | loader | 2 | 2 |
| 2 | report | 2 | 1 |
| 3 | loader | 1 | 1 |
| 4 | report | 1 | 0 |
| 5 | loader | 0 | 0 |

only one thing ran at any moment. turns are so short that it looks simultaneous, and a chip with several cores (each a full processor of its own) really does run several at once.

i assumed the two processes just ran side by side, and with one core nobody ever does. the report finishes at turn 4, not 2, because it waited. a busy neighbor slows you down even when your code is fine.

the other half of the job is that a normal program doesnt reach the disk itself. it asks the operating system, "open this file", and the system does it and hands the bytes back.

---
prev: [050 processes, a program while it runs](./050-processes.md) | next: [052 the working directory, where the terminal is standing](./052-the-working-directory.md)
