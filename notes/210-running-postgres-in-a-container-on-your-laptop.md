# 210: running Postgres in a container on your laptop
builds on: [085 addresses and ports, the right program on the right machine](./085-addresses-and-ports.md), [208 containers, a program packed with everything it needs](./208-containers-a-program-packed-with-everything-it-needs.md), [209 images and containers, the packed box and the running copy](./209-images-and-containers-the-packed-box-and-the-running-copy.md)
section: changing data safely, part 3, ~2 min read

the container says it is running, but your app gets "connection refused". is the database broken?

[209](./209-images-and-containers-the-packed-box-and-the-running-copy.md) split the frozen image (the packed box) from the running container made from it. Postgres, a database, is published as an image, so starting one on your laptop is a single command. the shop, the imaginary gujarati snack store these notes run on, gets its own:

```text
docker run --name shop-db -e POSTGRES_PASSWORD=snacks -p 5432:5432 -d postgres

docker run                       make a container from an image and start it
--name shop-db                   a name, so i can find it later
-e POSTGRES_PASSWORD=snacks      a setting handed in from outside; the image wont start without one unless you switch passwords off
-p 5432:5432                     laptop port : container port
-d                               run in the background, give the terminal back
postgres                         the image
```

the one that bit me is -p. the container has its own ports, and [a port picks which program on a machine gets the bytes](./085-addresses-and-ports.md). inside the box Postgres listens on 5432, but nothing on your laptop is wired to it.

| flags | laptop port 5432 | app on the laptop |
|---|---|---|
| no -p | nothing listening | connection refused |
| -p 5432:5432 | forwards to the box | connects |
| -p 5433:5432 | nothing, 5433 forwards | connects on 5433 |

the left number is the laptop side, so 5433:5432 is how you dodge a Postgres already installed on 5432. i assumed a running database was a reachable database, but running only means the process is alive inside the walls.

and the catch from [209](./209-images-and-containers-the-packed-box-and-the-running-copy.md) still holds: rows you create land in an unnamed volume (a disk area docker manages) that a fresh container never reuses, so removing shop-db and starting again gives an empty shop.

---
prev: [209 images and containers, the packed box and the running copy](./209-images-and-containers-the-packed-box-and-the-running-copy.md) | next: [211 a database server, Postgres where most app data lives](./211-a-database-server-postgres-where-most-app-data-lives.md)
