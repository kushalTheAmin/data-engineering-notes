# 084: a network, computers sending bytes to each other
builds on: [004 bytes](./004-bytes.md), [005 hexadecimal](./005-hexadecimal.md), [010 utf-8](./010-utf-8.md), [082 a database, a program that guards your data](./082-a-database-guards-the-data.md)
section: tables, keys and relationships, part 6, ~2 min read

Asha taps "mark delivered" on her phone, and the [database](./082-a-database-guards-the-data.md) program (the one that guards the data files) is on a different machine. so what physically crosses the gap?

a network is just a way to move bytes from one computer to another, over a cable or over wifi. nothing else crosses. no objects, no rows, no "order 106", only [bytes](./004-bytes.md), groups of 8 bits. so a request has to be turned into bytes first, the same way [utf-8](./010-utf-8.md) turns text into numbers. here is Ashas request, a made up one from the toy in 082, traced by hand (the bytes are shown in [hex](./005-hexadecimal.md), counting with sixteen digits):

```text
phone (Asha)                      the wire                 server (database)
text:   SET 106 delivered
bytes:  53 45 54 20 31 30 36 20 64 65 6c 69 76 65 72 65 64
        -------------- 17 bytes leave the phone ------------->
                                                           17 bytes arrive
                                                           decode as utf-8
                                                           text: SET 106 delivered
```

look at the middle. the wire never sees the word delivered, only 64 65 6c 69 76 65 72 65 64, and nothing on it says those bytes are utf-8 text. would you guess that from the numbers alone?

i expected something smarter, like shared memory between machines. its not, the receiver gets a copy of the bytes and the two sides must agree beforehand how to read them.

one caveat, real messages get cut into small chunks on the way and put back together, but the programs still just see bytes. Postgres sends and receives its own byte format, where most messages start with a type byte then a length (the very first one a client sends has no type byte), not readable text like my toy. the network doesnt care, bytes are bytes.

---
prev: [083 schema on write vs schema on read](./083-schema-on-write-vs-schema-on-read.md) | next: [085 addresses and ports](./085-addresses-and-ports.md)
