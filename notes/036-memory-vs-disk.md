# 036: memory vs disk, one forgets and one remembers
builds on: [004 bytes, 8 bits and 256 possible values](./004-bytes.md), [034 capstone, one shop order decoded down to bytes](./034-capstone-one-order-decoded-to-bytes.md), [035 the processor, the part that does the work](./035-the-processor.md)
section: memory, disks and files, part 2, ~2 min read

order 101 just arrived at the shop and the power cuts one second later. is the order still there?

it depends where it was sitting. memory (also called RAM) is the computers working space for running programs, and it forgets everything when the power goes off. disk (an SSD or a hard drive) keeps its [bytes](./004-bytes.md), groups of 8 on/off bits, with the power off.

the shop, the imaginary gujarati snack store these notes run on, has order 101 as the 35 byte line from [034](./034-capstone-one-order-decoded-to-bytes.md), `101,1,2026-04-01 09:15:00,delivered`. in [035](./035-the-processor.md) the processor, the part doing tiny steps on numbers, got its numbers copied in from memory. here is order 101s night:

| step | what happens | in memory | on disk |
|---|---|---|---|
| 1 | order 101 arrives | the line | nothing |
| 2 | program writes it out | the line | the line |
| 3 | power cut | gone | the line |
| 4 | restart | empty | the line |

skip step 2 and the disk never gets the line, so after the restart nothing has it. i assumed the difference was size, and memory usually is smaller, but the real difference is whether it survives the power.

one gotcha: "written" doesnt always mean on disk yet. the computer can hold a fresh write in memory for a moment first, and a program has to ask for a flush (fsync on linux, an operating system) to force it onto the disk. a power cut in that gap loses a save you thought you made.

this is why databases, programs that store your tables, normally put your rows on disk before saying "saved". how much slower that is, is the next one.

---
prev: [035 the processor, the part that does the work](./035-the-processor.md) | next: not written yet
