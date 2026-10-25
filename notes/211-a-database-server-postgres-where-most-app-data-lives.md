# 211: a database server, Postgres where most app data lives
builds on: [086 client and server, you ask, the database answers](./086-client-and-server.md), [102 a database in one file, setting up DuckDB](./102-a-database-in-one-file.md), [210 running Postgres in a container on your laptop](./210-running-postgres-in-a-container-on-your-laptop.md)
section: changing data safely, part 4, ~2 min read

DuckDB lets one running program write to its file at a time. so how does the shop, the imaginary snack store these notes run on, take orders from Asha and Bhavin in the same second?

[210](./210-running-postgres-in-a-container-on-your-laptop.md) left a Postgres container running. Postgres is a database server: a database that runs as its own program, listens on a [port](./086-client-and-server.md) (a number picking which program gets the bytes; 5432 unless you change it), and is the only thing that ever opens the data files. everyone else is a [client](./086-client-and-server.md) (a program that sends a request and waits), and it asks.

```text
DuckDB (102)                     Postgres
                                 Ashas app ------+
my script                        Bhavins app ----+--> postgres server --> data files
  opens shop.duckdb directly     report script --+    listens on 5432     only it touches them
```

with [DuckDB](./102-a-database-in-one-file.md) the database is a library inside your script, so whoever opens the file is the one touching it. with Postgres, three clients can be connected at the same moment and none of them ever opens a file. each one sends SQL (the language for asking a database) down its connection and gets rows back.

the Postgres docs say it starts a new process (a running program) for each connection, while one original process keeps listening. i assumed a server database was just a bigger DuckDB, but the real difference is who opens the file.

this is why a react or .NET backend reaches its database by an address and port, not a file path. the notes on locks and transactions from here describe Postgres, while shop queries still get checked in DuckDB.

---
prev: [210 running Postgres in a container on your laptop](./210-running-postgres-in-a-container-on-your-laptop.md) | next: not written yet
