# 212: connections and sessions, one conversation with the database
builds on: [086 client and server, you ask, the database answers](./086-client-and-server.md), [102 a database in one file, setting up DuckDB](./102-a-database-in-one-file.md), [211 a database server, Postgres where most app data lives](./211-a-database-server-postgres-where-most-app-data-lives.md)
section: changing data safely, part 5, ~2 min read

if Asha changes her time zone setting on the database, does Bhavin see the change too? same server, same shop, so i guessed yes.

[211](./211-a-database-server-postgres-where-most-app-data-lives.md) had three clients connected to one Postgres server. each [connection](./102-a-database-in-one-file.md) (an open line from a program to a database) carries one session: the conversation that starts when the line opens, ends when it closes, and keeps its own settings in between. the word is new here, because in [199](./199-session-starts-flag-the-click-after-a-long-gap.md) a session meant a run of someones clicks.

here is the shop, the imaginary gujarati snack store these notes run on, with two apps on the Postgres server from [210](./210-running-postgres-in-a-container-on-your-laptop.md). this is Postgres, not DuckDB, and say the server is set to default to UTC:

```text
step  Ashas app (connection 1)               Bhavins app (connection 2)
1     connect                                connect
2     SET TIME ZONE 'Asia/Kolkata';
3     SHOW TIME ZONE;  ->  Asia/Kolkata      SHOW TIME ZONE;  ->  UTC
4     disconnect
5     connect again
6     SHOW TIME ZONE;  ->  UTC
```

step 3 is the answer: one server, two answers. the Postgres docs say SET only affects the value used by the current session. step 6 is the other half, since a new connection is a new session and the setting died with the old one. i assumed SET changed the database, but it only changes my side of the conversation.

so what: apps often reuse a few open connections instead of opening one per request, and a tool in the middle can hand your next statement to a different connection. PgBouncer, a popular connection pooler for Postgres, does this in transaction mode, and its docs list SET as unsupported there. so a SET you ran a minute ago can quietly be gone.

---
prev: [211 a database server, Postgres where most app data lives](./211-a-database-server-postgres-where-most-app-data-lives.md) | next: not written yet
