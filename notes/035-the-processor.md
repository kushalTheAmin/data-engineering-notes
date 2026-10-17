# 035: the processor, the part that does the work
builds on: [004 bytes, 8 bits and 256 possible values](./004-bytes.md), [021 storing money as whole cents](./021-storing-money-as-whole-cents.md), [034 capstone, one shop order decoded down to bytes](./034-capstone-one-order-decoded-to-bytes.md)
section: memory, disks and files, part 1, ~2 min read

[034](./034-capstone-one-order-decoded-to-bytes.md) left order 101 as 35 bytes, but bytes just sit there. so what actually adds up the bill?

the processor (also called the CPU, central processing unit) is the part of the computer that does the work. its menu is tiny: put a number somewhere, add, multiply, compare two numbers, and a few more of that kind.

the shop, the imaginary gujarati snack store these notes run on, keeps prices as [whole cents](./021-storing-money-as-whole-cents.md), price times 100. order 101 is 2 dhokla at 600 and 2 masala chai at 300. here is the total, one tiny step at a time:

| step | tiny step | total | item |
|---|---|---|---|
| 1 | put 0 in total | 0 | |
| 2 | put 600 in item | 0 | 600 |
| 3 | multiply item by 2 | 0 | 1200 |
| 4 | add item to total | 1200 | 1200 |
| 5 | put 300 in item | 1200 | 300 |
| 6 | multiply item by 2 | 1200 | 600 |
| 7 | add item to total | 1800 | 600 |

1800 cents, so 18.00. seven steps for a two line bill. in python thats one line, and i kept forgetting it is several steps underneath.

total and item are my names. the real holding spots are called registers, a few tiny slots right inside the processor, and it only works on numbers there. so numbers out in the computers memory (its working space) get copied in first, and thats a hint about where the time goes later.

i assumed the processor knew what an order was. it knows nothing, even the instruction "add" is stored as a number, like everything else in [001](./001-data-is-facts-and-numbers.md).

it ticks several billion times a second (several gigahertz, giga being a billion), and a chip can hold several cores, each a full processor of its own. when you run a query that reads a billion rows, it repeats steps like these for each row.

---
prev: [034 capstone, one shop order decoded down to bytes](./034-capstone-one-order-decoded-to-bytes.md) | next: [036 memory vs disk, one forgets and one remembers](./036-memory-vs-disk.md)
