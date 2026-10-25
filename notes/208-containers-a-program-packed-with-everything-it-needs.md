# 208: containers, a program packed with everything it needs
builds on: [050 processes, a program while it runs](./050-processes.md), [051 the operating system, the program that shares the machine out](./051-the-operating-system.md), [207 capstone, each customers first order and the days between orders](./207-capstone-each-customers-first-order-and-the-days-between-orders.md)
section: changing data safely, part 1, ~2 min read

a script runs fine on my laptop and dies on the server, same file, same data. what could possibly differ?

[207](./207-capstone-each-customers-first-order-and-the-days-between-orders.md) wrapped up the queries section, and this next one is about changing data, which needs a real database running somewhere. containers are how people start one without installing it by hand.

a container is a program running inside a walled-off box that holds everything it needs: its own python, its own libraries (code other people wrote that your program calls), its own settings. the shop, the imaginary gujarati snack store these notes run on, has a script that totals its 7 orders. say it moves to a server (another computer):

| | my laptop | the server |
|---|---|---|
| python version | 3.12 | 3.8 |
| a library the script imports | installed | missing |
| the script | loader.py | loader.py, identical |
| result | prints the total | crashes, ModuleNotFoundError (library missing) |

the file is identical, so the machine around it was the problem. a container packs that machine part too:

```text
the box (a container)
  loader.py       the shop script
  python 3.12     its own copy
  the library     its own copy
  its settings
borrowed from the machine: the kernel (core of the operating system)
```

ship the box and the servers python and libraries stop mattering, because the script looks inside the box first. i kept picturing a tiny virtual computer inside the real one, and thats wrong. it is an ordinary [process](./050-processes.md) (a running copy of a program) that the [operating system](./051-the-operating-system.md) walls off from the others. so it borrows the machines kernel, the one thing the box cant pack (on mac and windows, Docker Desktop starts a small hidden linux machine and the boxes borrow its kernel).

the Postgres database the next notes use is published as a ready-made box. Docker, a tool that runs containers, starts it with one command, so you skip installing Postgres yourself. a later note does exactly that.

### check yourself

1. the shop loader runs in a container with python 3.12 and totals the 7 orders. the server only has python 3.8, and overnight someone upgrades it to 3.13. which python runs the script before and after?
<details><summary>answer</summary>

3.12 both times. the container carries its own python, so the servers version never gets asked. the tempting answer is 3.8 then 3.13, from picturing the box using the machines python.

</details>

2. you start 3 containers of the shop script on one server. how many kernels run them, and how many separate pythons are in play?
<details><summary>answer</summary>

1 kernel, shared by all three and borrowed from the machine, and 3 pythons, one packed in each box. the tempting answer is 3 kernels, from picturing each container as its own little computer.

</details>

---
prev: [207 capstone, each customers first order and the days between orders](./207-capstone-each-customers-first-order-and-the-days-between-orders.md) | next: [209 images and containers, the packed box and the running copy](./209-images-and-containers-the-packed-box-and-the-running-copy.md)
