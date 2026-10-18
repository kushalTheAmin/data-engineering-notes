# 053: absolute vs relative paths
builds on: [040 folders and paths](./040-folders-and-paths.md), [052 the working directory, where the terminal is standing](./052-the-working-directory.md)
section: memory, disks and files, part 19, ~2 min read

the same path, ../backup/orders.csv, finds the right file from one folder and a file that doesnt exist from another. how does a path know where it starts?

last time the [working directory](./052-the-working-directory.md), the folder a process stands in, decided which orders.csv a bare name meant. now the rule behind it. an absolute [path](./040-folders-and-paths.md), the folder names walked from the top to a file, starts with a slash and always begins at the root, the top folder holding everything. a relative path has no leading slash and begins at the working directory. the .. is not special magic: it just means the parent folder, the one holding this one. (this is the linux and mac way, windows paths start with a drive like C:\ instead.)

here it is in the shop, the imaginary gujarati snack store these notes run on, with its exports and backup folders:

| standing in | path written | lands on |
|---|---|---|
| /shop/exports | orders.csv | /shop/exports/orders.csv |
| /shop/backup | orders.csv | /shop/backup/orders.csv |
| /shop/exports | /shop/backup/orders.csv | /shop/backup/orders.csv |
| /shop/exports | ../backup/orders.csv | /shop/backup/orders.csv |

rows 1 and 2 are the same words landing on different files. row 3 ignores where you stand. row 4 goes up one folder to /shop, then down into backup. now stand one folder too high:

```python
import os.path
print(os.path.normpath(os.path.join("/shop", "../backup/orders.csv")))
```

```output
/backup/orders.csv
```

i assumed .. would stay inside whatever project i was in, and it just climbs one folder, wherever that is.

so which is better? an absolute path always means the same file, but it breaks the day the data moves to another machine with different folders. a relative path travels with the project, but only if whatever launches your script stands in the right place. both fail in real pipelines.

### check yourself

1. you are standing in /shop/backup. which file does ../exports/orders.csv point to, and why is /shop/backup/exports/orders.csv the wrong guess?
<details><summary>answer</summary>

/shop/exports/orders.csv. the .. climbs from backup up to /shop first, and only then walks down into exports. the tempting wrong answer reads the path as going down into backup, as if relative meant "inside here", but .. goes up before anything goes down.

</details>

2. your python script opens "/home/asha/shop/orders.csv" and works on your laptop. a teammate runs it on a server where the project lives in /srv/shop. it fails. would switching to "shop/orders.csv" fix it for sure? defend your answer.
<details><summary>answer</summary>

no. the absolute path names a folder only your laptop has, so moving it breaks. the relative one no longer names a machine, but it is looked up from the working directory, so it works only if the server starts the script from the folder holding shop. the tempting answer is yes, because relative paths feel portable, but portable also needs the right place to stand.

</details>

---
prev: [052 the working directory, where the terminal is standing](./052-the-working-directory.md) | next: [054 head and tail, looking at the start and end of a file](./054-head-and-tail.md)
