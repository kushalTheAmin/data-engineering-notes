# 209: images and containers, the packed box and the running copy
builds on: [050 processes, a program while it runs](./050-processes.md), [208 containers, a program packed with everything it needs](./208-containers-a-program-packed-with-everything-it-needs.md)
section: changing data safely, part 2, ~2 min read

start the same box twice and edit a file inside one. does the other change too?

[208](./208-containers-a-program-packed-with-everything-it-needs.md) said a container is a walled-off [process](./050-processes.md) (a running copy of a program) holding its own python and libraries. but a process comes from a program sitting on disk, so what does a container come from? an image: the packed box before anything runs, one frozen package with python, libraries, settings and the script. a container is a running copy made from it, same split as program and process.

the shop, the imaginary gujarati snack store these notes run on, packs its order loader into an image called shop-loader. watch what happens to the counts (Docker is the tool that runs containers, and every docker run makes a new container from an image):

| step | what i do | images | containers | has my edit to loader.py |
|---|---|---|---|---|
| 1 | build shop-loader | 1 | 0 | none |
| 2 | run it twice, a and b | 1 | 2 | none |
| 3 | edit loader.py inside a | 1 | 2 | a |
| 4 | remove a | 1 | 1 | none |
| 5 | run it again, c | 1 | 2 | none |

each container gets its own private scratch space on top of the image. the edit in step 3 lands there, so b never sees it, and the image is never touched. the image just sits there and never runs. i assumed the image was the thing running and a container was only a nickname for it.

this bites with databases. a Postgres container (Postgres is a database) that stores rows inside itself loses them when you remove it. the real image parks them in an unnamed volume (a disk area docker manages) that a fresh container never reuses, so the loss looks the same. keep the data somewhere you name, and a later note does that.

### check yourself

1. you run 2 containers from the shop-loader image, and in one you delete the file holding the 7 shop orders. a third container starts afterward. how many orders can the other two see?
<details><summary>answer</summary>

7 in the untouched one, and 7 in the new third one. the delete happened in one containers private scratch space, and the image underneath never changed. the tempting answer is 0 for the new one, from thinking the delete changed the image.

</details>

2. a team removes their Postgres container to upgrade, then starts a fresh one from the same image. their orders were stored inside the old container. where are the orders now?
<details><summary>answer</summary>

the new container starts with none. they were written inside the old container, into the unnamed volume from above, which a fresh container never reuses, and the image never held them. the tempting answer is that they come back, from thinking the image remembers what its containers did.

</details>

---
prev: [208 containers, a program packed with everything it needs](./208-containers-a-program-packed-with-everything-it-needs.md) | next: [210 running Postgres in a container on your laptop](./210-running-postgres-in-a-container-on-your-laptop.md)
