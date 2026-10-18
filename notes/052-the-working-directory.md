# 052: the working directory, where the terminal is standing
builds on: [040 folders and paths](./040-folders-and-paths.md), [049 the terminal, running programs by typing](./049-the-terminal.md), [050 processes, a program while it runs](./050-processes.md)
section: memory, disks and files, part 18, ~2 min read

you open orders.csv in python, get the wrong file, and the code never changed. so what did?

the working directory is the folder a [process](./050-processes.md), one running copy of a program, is currently standing in. the [shell](./049-the-terminal.md), the program in the terminal that runs your typed lines, has one. pwd prints it, ls lists the files in it, and cd moves it. a bare name like orders.csv (a data file) is looked up from there. thats the "folder you launched from" that [040](./040-folders-and-paths.md) mentioned.

here is a session ($ is the shells prompt, waiting for you) in the shop, the imaginary gujarati snack store these notes run on, using the two folders from [040](./040-folders-and-paths.md):

```text
$ pwd
/shop/exports
$ ls
orders.csv
$ cd /shop/backup
$ pwd
/shop/backup
$ ls
orders.csv
```

ls with nothing after it means "this folder", so both times it shows a file called orders.csv, and they are two different files. open("orders.csv") in python reads whichever one is in the folder you stand in when you run it.

i expected cd to be a program like the others, and it cant be. every process has its own working directory, copied from the process that started it, so a program that changes its own leaves the shell where it was. thats why cd is built into the shell itself.

so a script that works when you run it from the exports folder can fail when something else starts it from a different folder. same code, different place to stand.

the next one is about writing paths that dont care where you stand.

---
prev: [051 the operating system, the program that shares the machine out](./051-the-operating-system.md) | next: not written yet
