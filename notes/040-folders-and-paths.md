# 040: folders and paths
builds on: [039 a file is a named list of bytes](./039-a-file-is-a-named-list-of-bytes.md), [036 memory vs disk, one forgets and one remembers](./036-memory-vs-disk.md)
section: memory, disks and files, part 6, ~2 min read

two files on the same disk (storage that keeps bytes without power, see [036](./036-memory-vs-disk.md)) are both called orders.csv. so when you say orders.csv, which one do you get?

in [039](./039-a-file-is-a-named-list-of-bytes.md) a file was a name plus its bytes in order, and i skipped where it sits. it sits in a folder, a named place on disk that holds files and other folders (directory means the same). the shop, the imaginary gujarati snack store these notes run on, could keep its exports like this:

```text
/
  shop
    exports
      orders.csv
    backup
      orders.csv
```

on linux and mac the single / at the top is the root, the folder that holds everything else. a path is the names you walk through from the top down to the file, with a slash between each. here is the walk for the first orders.csv:

| step | standing in | look for | find |
|---|---|---|---|
| 1 | / | shop | a folder |
| 2 | /shop | exports | a folder |
| 3 | /shop/exports | orders.csv | a file |

so the path is /shop/exports/orders.csv. the other one is /shop/backup/orders.csv, a different walk ending at a different file with its own bytes, even though the name matches. a bare name doesnt say which file, the whole path does.

i kept picturing folders as boxes, but reading a path as left to right directions fits better. (windows has one root per drive, so it writes the same idea as C:\shop\exports\orders.csv.)

this bites in real code. a path without the leading / starts from the folder you launched the program from, so open("orders.csv") in python works when you launch it from the exports folder and says file not found on another machine (a server), because you launched it from a different folder.

---
prev: [039 a file is a named list of bytes](./039-a-file-is-a-named-list-of-bytes.md) | next: not written yet
