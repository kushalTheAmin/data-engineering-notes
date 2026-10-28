# curriculum

the map from zero to data engineer. one checkbox is one atom: one idea small enough for a 2 minute note. big concepts are already broken into several atoms in the order you need them, and a box still gets split further if it turns out bigger than it looks. arcs run in order, boxes inside an arc run in order, and each arc ends with a capstone that assembles its atoms. a ★ marks a concept that is important or easy to get wrong, so its note ends with check yourself questions. every capstone gets them too.

## THREAD
baton: 245 showed that changing a column type in Postgres (order_id INTEGER to BIGINT) normally rewrites the whole table and its indexes, since the bytes of every value change width (101 goes from 4 bytes to 8), and takes ACCESS EXCLUSIVE, the lock that blocks even a plain SELECT, with the docs adding up to double the disk space and a no-rewrite exception when stored values stay valid unchanged. the next box is changing a column type without downtime: add a new column, backfill it, swap. earlier baton: 244 showed a deadlock, two transactions that each hold a row lock the other wants: Asha locks 106 then wants 107 while Esha locks 107 then wants 106, so the waits form a circle; Postgres checks for one after deadlock_timeout (1 second by default), aborts one transaction with error 40P01 and rolls it back, and the docs say to lock rows in a consistent order or retry the aborted transaction. the next box is changing a column type on a big table. earlier baton: 243 showed SELECT ... FOR UPDATE, a Postgres read that locks the rows it returns until the transaction ends: Asha and Esha both read order 106 as pending and both send the email with a plain SELECT, but with FOR UPDATE in a BEGIN Esha waits, then at read committed Postgres rechecks the WHERE on the new row and she gets 0 rows; the docs add that with no BEGIN each statement is its own transaction so the lock ends with the SELECT. the next box is deadlocks, what happens when two transactions each hold a lock the other needs. earlier baton: 242 showed a row lock: Postgres UPDATE locks the row it changes until COMMIT or ROLLBACK, so Esha changing order 107 goes through while changing 106 waits for Asha, and a plain SELECT never waits on it; the docs say only the strongest table lock, taken by DROP TABLE and TRUNCATE, blocks a plain SELECT, and a forgotten COMMIT keeps locks held. the next box is SELECT FOR UPDATE, taking a row lock on purpose when you only read. earlier baton: 241 showed serializable, the strictest Postgres level where the result must match some one-at-a-time order: Asha and Esha both count 2 pending orders (106 real, 108 imagined) and each cancels a different one, which repeatable read allows (0 left) but serializable stops by failing one with error 40001 so the app reruns the whole transaction and the count then says 1; the docs add apps must be ready to retry and it can fail a transaction serial order would allow. the next box is row locks and table locks, the other way to deal with two people touching the same thing. earlier baton: 240 showed repeatable read, the Postgres level where Ashas picture is taken at her first query (not BEGIN) and kept until the transaction ends: a comparison table of counts 7, 8, 8 at read committed against 7, 7, 8 at repeatable read after Esha commits order 108, so non repeatable reads and phantoms cannot happen; the docs add that changing a row Esha already changed gives a serialization error and the app must retry. the next box is serializable, the strictest level, where the database acts as if transactions ran one at a time and fails some so you retry. earlier baton: 239 showed read committed, the Postgres default isolation level, takes its picture per query and not per transaction: Asha does BEGIN, Esha commits order 108, and Ashas first query already sees it, while an uncommitted 108 stays hidden (a trace table of counts 7, 7, 8); this is where non repeatable reads and phantoms come from, and the Postgres docs say a single SELECT never sees changes committed while it runs. the next box is repeatable read, the level where one picture lasts the whole transaction. earlier baton: 238 showed a phantom read is re-running the same query in one transaction and getting a different set of rows because someone committed a matching change (Asha lists pending orders in a python loop, gets [106], then order 108, imagined, is committed and she gets [106, 108]); the Postgres docs list it as possible at read committed and say its repeatable read does not show it, though the SQL standard allows it there; a check yourself count of pending orders is 1 and snacks is 3. the next box is isolation levels at read committed, the setting that decides which of these surprises you can see. earlier baton: 237 showed a non repeatable read is reading one row twice in a transaction and getting different values because someone committed a change in between (Asha reads dhokla at 6.00, Esha commits 7.00, Asha reads 7.00, both real committed prices, no draft involved); the Postgres docs list it as possible at read committed, where each query sees what was committed when that query began, and a check yourself total of all prices went from 38.00 to 39.00. the next box is phantoms, the same surprise with a set of rows appearing instead of one value changing. earlier baton: 236 showed a dirty read is reading a change another transaction hasnt committed, which may be rolled back and never have existed (a trace table where Esha sets dhokla to 60.00, Asha reads it, Esha rolls back and the committed price was 6.00 throughout); isolation is the promise that stops it, and the Postgres docs list dirty reads as allowed at read uncommitted but say Postgres behaves like read committed there, so it never shows one. the next box is non repeatable reads, where a value changes between two of your own reads. earlier baton: 235 showed a lost update is two people reading the same number and each writing back an answer worked out from it, so the later write erases the earlier (stock of 10 dhokla, Asha and Bhavin each read 10 and write 9 where 8 is right, with no error), that isolation does not stop it because both reads were of committed data, and that a single UPDATE left_over = left_over - 1 from each gives 8 because the database subtracts from the current value; Postgres docs say at read committed a second UPDATE of the row waits for the first to commit and then applies to the updated row; check yourself also showed a check done in one step and an update in another can still take 1 left to -1. the next box is dirty reads, the next kind of trouble two transactions can cause each other. earlier baton: 234 showed replaying is how the database fixes a table file left behind by a crash: on startup Postgres reads the WAL forward from a marker it saved earlier and redoes only the changes the table is missing (a python loop over two log records where record 1 is skipped because the table already has it and record 2 updates order 106 to delivered), since redoing an insert twice would put order 108 in twice; each block is stamped with the position of the last log record applied to it and Postgres source notes say a record is skipped when the block is already at or past it (the loop uses one number for the whole table). the next box is lost updates, the first of the trouble two transactions can cause each other. earlier baton: 233 showed the write ahead log, WAL, is the databases own list of changes whose one rule is log first: a change is flushed to the WAL before it may go into the table files (a step table where after the WAL flush Esha is told done while the table file still lacks 108, so the WAL is the only place 108 lives on disk), because the WAL is one cheap append at the end of a file while table updates jump to many blocks; Postgres docs say the WAL is written sequentially so syncing it costs much less than flushing data pages, and the rule is about order not timing (a table page may be written early, never before its WAL record). the next box is replaying the log after a crash. earlier baton: 232 showed durability means once COMMIT reports done the change is already flushed to disk, since a crash wipes memory: a sequence diagram of Esha, Postgres and the disk where a crash before the flush loses order 108 but she was never told done, and Postgres docs say synchronous_commit is on by default, off can lose recent commits but not corrupt the database, and what is flushed is a short record of the change not the whole table. the next box is the write ahead log, that short record written before the change. earlier baton: 231 showed isolation means transactions running at the same time dont see each others unfinished work: on two connections to a my_orders table of 7 rows, Esha inside her transaction counts 8 after inserting 108 while Asha counts 7 at once without waiting, still 7 after Esha rolls back, and 8 only after Esha commits; Postgres docs say read committed is the default and a query sees only data committed before it began, and serializable is the strictest level. the next box is durability, surviving a crash. earlier baton: 230 showed consistency means declared rules hold before and after a transaction: in a copy of products with CHECK (price > 0), a good dhokla change to 7.00 and a bad kaju katli change to -1 in one transaction both vanish (6.00 and 12.00 remain), but an undeclared rule goes unguarded (order 108 sits with no items), and Postgres docs say CHECK cannot reference other rows. the next box is isolation, two people at the same time. earlier baton: 229 showed ACID is four promises (atomicity, consistency, isolation, durability) with a shop failure for each: order 108 saved without items, a price of -5, Asha counting an order that later vanishes, Esha told her order is saved and then losing it; that consistency only guards rules somebody wrote down (600.00 passes CHECK (price > 0)); a crash before COMMIT is an atomicity question, after COMMIT a durability one; and that Postgres docs say read committed is the default isolation level. the next box is ACID consistency, the rules still hold after every change. earlier baton: 228 showed BEGIN opens a transaction, COMMIT keeps every change inside and ROLLBACK throws them all away (copies of orders and items: order 108 and its dhokla item both count 1 inside the transaction, then 0 and 0 after ROLLBACK, and the same steps ending in COMMIT keep both), that a ROLLBACK after a COMMIT has nothing to undo (109 stays, DuckDB errors), that in DuckDB a failed insert aborts the transaction so the good item is refused and COMMIT rolls back (order 110 gone), and that Postgres docs say an open transaction's updates are invisible to other sessions until it completes and that with no BEGIN each statement commits on its own. the next box is ACID, four promises a database makes. earlier baton: 227 showed a transaction is a group of changes where all happen or none do: on copies of orders and order_items, order 108 inserted fine, its item row naming product 99 broke the foreign key, and without a transaction the order row stayed with 0 item rows, while one statement alone is already all or nothing (an UPDATE adding 3 to product ids of order 102 failed and left 3 and 4). Postgres docs open with a bank payment as the example. the next box is COMMIT and ROLLBACK, how to actually write one. earlier baton: 226 showed TRUNCATE removes every row and keeps the table (menu of fafda, jalebi, masala chai truncated, then INSERT imarti works since the columns survived), DROP TABLE removes the table itself so a later SELECT errors on the name, and that Postgres docs say TRUNCATE skips scanning the rows so it is faster and frees disk space at once, but Postgres refuses to truncate or drop a table another table points at unless CASCADE is added. the next box is transactions, all or nothing. earlier baton: 225 showed ALTER TABLE menu ADD COLUMN vegan BOOLEAN adds a column to a table that has rows (menu of fafda, jalebi, masala chai) and every old row gets NULL, that ADD COLUMN in_stock BOOLEAN DEFAULT true fills the old rows with true too (unlike 215 where a default only filled a left out insert), that adding a name already there errors, and that Postgres docs say a constant default is kept in metadata so the ALTER is fast on large tables while a volatile one like clock_timestamp() rewrites the table. the next box is DROP and TRUNCATE. earlier baton: 224 showed an upsert is an INSERT with ON CONFLICT (name) DO UPDATE SET price = EXCLUDED.price, which updates the row when the key is already there and adds it when not (menu table keyed on name: jalebi 5.50 updated, imarti 6.00 added, 7 rows, same 7 on a second run), that EXCLUDED is the row you tried to insert, DO NOTHING skips the repeat, that a typo like chai for masala chai becomes a new row, and that with no key the upsert errors. the next box is ALTER TABLE: adding a column. earlier baton: 223 showed DELETE FROM removes the rows its WHERE matches, whole rows, and that DELETE FROM orders WHERE order_id = 104 is refused because a row in order_items still points at it, so the pointing row goes first (DELETE FROM order_items WHERE order_id = 104 works, leaving 103's two rows), that no WHERE empties the table but keeps it, that a test on NULL is unknown so DELETE WHERE stars < 4 on 5, 4, NULL, 3, NULL leaves 4 ratings, and that fafda (in no order) can be deleted while dhokla cant; the shop keeps 104 as cancelled instead of deleting it. the next box is upsert. earlier baton: 222 showed UPDATE changes values in rows that already exist, SET names the column and new value and WHERE picks the rows (orders: UPDATE orders SET status = 'cancelled' WHERE order_id = 106 changes only 106, 105 and 107 stay delivered), that leaving the WHERE off changes all 7 orders to cancelled with no error or warning, that a WHERE matching nothing changes 0 rows and is not an error in Postgres, that SET price = price + 1 reads the old value so running it twice adds 2 (jalebi 7.00, kaju katli 14.00), and that MySQL's client has --safe-updates against this. the next box is DELETE. earlier baton: 221 showed INSERT INTO a table followed by a SELECT adds the rows the query returns (delivered table filled from orders WHERE status = 'delivered', 5 rows: 101, 102, 103, 105, 107), matched to columns by position like in 220, and that running the same INSERT again gives 10 rows with only 5 different order_id because nothing remembers the first run, while a PRIMARY KEY would refuse the repeat. the next box is UPDATE and why the WHERE matters. earlier baton: 220 showed INSERT adds rows and matches values to columns: with no column list the values go by position in CREATE TABLE order, so (4, 3, date) meant for Chirag (3) and kaju katli (4) quietly stored Disha (4) with jalebi (3) because both are whole numbers and only the type is checked, naming the columns (product_id, customer_id) puts the meaning next to the value and a left out added_on becomes NULL with no DEFAULT, DuckDB refuses a wrong count of values while Postgres docs say it fills the first columns and gives the rest their default or NULL. the next box is INSERT from a SELECT. earlier baton: 219 showed a sequence is a counter the database keeps outside any table, nextval hands out the next number and never steps back (tickets table with id INTEGER PRIMARY KEY DEFAULT nextval('ticket_id'): Asha 1, Bhavin 2, a refused insert with no customer still used 3, so Chirag got 4), that a deleted row's id is not reused (Disha gets 5 after Chirag's 4 is deleted), that the sequence never looks at the table so hand-typed ids 101 and 102 do not move it (the next id is 1), and that Postgres docs say the same about gaps and that serial is a sequence plus DEFAULT nextval. the next box is INSERT. earlier baton: 218 showed a key rule only exists once it is written in CREATE TABLE: the same three shipment inserts all land in a table with no rules (shipment 1 twice, order 999 that does not exist) while PRIMARY KEY on shipment_id and order_id NOT NULL REFERENCES orders (order_id) refuse the repeat and the orphan, that a foreign key may repeat (two shipments for order 101) and a NULL pointer passes unless NOT NULL is added (Postgres docs agree), and that Snowflake standard tables accept these keys but do not enforce them. the next box is where ids come from: sequences and auto increment. earlier baton: 217 showed CHECK is a column rule with a true or false test (price DECIMAL CHECK (price > 0)): -7.50 and 0 are refused, but a NULL price is stored because the test gives unknown and only a false refuses (Postgres docs say the same), so a price that must exist and be positive needs NOT NULL CHECK. the next box is key constraints. earlier baton: 216 showed UNIQUE on a column makes the database refuse a value already there (login table: email VARCHAR UNIQUE, a second asha@example.com is refused as a duplicate key), that a primary key is that rule plus no NULL and a table has one primary key but many UNIQUE columns, and that NULLs never clash (two NULL emails both go in, count(*) 4, count(email) 2; Postgres does the same unless NULLS NOT DISTINCT). the next box is CHECK. earlier baton: 215 showed NOT NULL makes the database refuse a row whose column is NULL, and DEFAULT fills a column an insert leaves out (the cart table: quantity INTEGER NOT NULL DEFAULT 1, Asha's row gets 1), but a typed NULL is a chosen value, so the default does not rescue it and NOT NULL refuses it, while with no NOT NULL the typed NULL is kept; a NOT NULL DEFAULT 'unknown' city stores the text, so IS NULL finds 0 rows. the next box is UNIQUE and CHECK. earlier baton: 214 showed a temporary table (CREATE TEMP TABLE cheap AS SELECT * FROM products WHERE price < 6, 3 rows: jalebi, masala chai, fafda) belongs to one session, so Bhavin on the same Postgres server and Asha after reconnecting both get relation does not exist, and that a temp table named products hides the real 6-row products (DuckDB shows 3 rows; Postgres looks in its temporary schema first unless the schema name is written). the next box is NOT NULL and DEFAULT. earlier baton: 213 showed CREATE TABLE makes a new empty table from a name and a list of columns with types (the wishlist table: customer_id INTEGER, product_id INTEGER, added_on DATE, zero rows), that Postgres takes the same statement, and that CREATE TABLE IF NOT EXISTS only checks the name, so on the existing products table it does nothing and adds no column. the next box is temporary tables. earlier baton: 212 showed a connection (an open line from a program to the database) carries one session, a conversation with its own settings: Asha runs SET TIME ZONE 'Asia/Kolkata' and SHOW TIME ZONE gives Asia/Kolkata on her connection but UTC on Bhavins, and after she disconnects and reconnects it is UTC again; in transaction mode PgBouncer may hand the next statement to another connection, so SET is unsupported there. the next box is CREATE TABLE. earlier baton: 211 showed Postgres is a database server: its own always-running program that listens on port 5432 and alone opens the data files, while Ashas app, Bhavins app and a report script are clients that send SQL over connections (DuckDB is the opposite, a library inside your script), and Postgres starts a new process per connection. the next box is connections and sessions: one conversation with the database. earlier baton: 210 showed one docker run command starts Postgres (--name shop-db, -e POSTGRES_PASSWORD, -d, the postgres image), and that -p 5432:5432 forwards laptop port to container port, left number the laptop side (5433:5432 dodges a Postgres already on 5432), so without -p a running container is unreachable and the app gets connection refused; rows still vanish if the container is removed. the next box is a database server: Postgres, where most app data lives. earlier baton: 209 split a container from its image: the image is the frozen packed box that never runs and never changes, each container started from it is a running copy with its own private scratch space (shop-loader image, containers a, b, c; an edit inside a is invisible to b, and gone when a is removed, c starts clean), so rows a Postgres container writes inside itself vanish when it is removed. the next box is running Postgres in a container on your laptop. earlier baton: 208 opened the changing data section: a container is a program running in a walled-off box that carries its own python, libraries and settings (a script that works on a laptop fails on a server missing a library; packed in the box it doesnt), it is an ordinary process the operating system walls off, not a tiny virtual computer, and it still borrows the machines kernel; the official Postgres image can be started with Docker. the next box is images and containers: the packed box before it runs (the image) versus the running copy. earlier baton: 207 was the capstone for the bigger queries section: one query, a CTE joining customers to orders then ROW_NUMBER and day minus LAG over a PARTITION BY name window, gives each order its number inside the customer and the days since the customers previous one (Asha 1, 3, 8 april gives NULL, 2, 5; Bhavin NULL, 8; Chirag and Disha only a first order; Esha has no row), and it links every note from 174 to 206. the next box starts the changing data section: containers. earlier baton: 206 was practice: ten shop questions, easy to hard, sorted by what the words ask for (never means left join plus IS NULL, more than once means HAVING, second highest a scalar subquery, both A and B INTERSECT, latest per customer ROW_NUMBER, average of totals a CTE first, running a running total), where three have a believable wrong answer (fafda vanishes under an inner join, Esha passes an every-order-delivered test with no EXISTS guard, averaging item lines gives 9.73 instead of 18.07). the next box is the capstone: each customers first order and the days between orders. earlier baton: 205 showed ->> pulls one value out of a JSON string in a column, by a $.name path, always as text (so CAST before summing), using the new app_events table (4 rows; the two view events have no quantity so it comes back NULL, and a mistyped path gives NULL too, no error), and then it groups like a normal column (Asha 2, Bhavin 1). the next box is practice: ten interview style SQL questions on the shop. earlier baton: 204 showed an array (a list in one cell; DuckDB calls the variable length kind a list) can be unnested into one row per item, with the other columns copied on, using the product_tags table (6 products, 2 tags each except masala chai with an empty list), that an empty list gives zero rows so masala chai vanishes, and that unnested tags can be counted with a subquery in FROM and GROUP BY (savory 3, fried 2, sweet 2). the next box is querying JSON inside a column. earlier baton: 203 showed a recursive CTE is a CTE that reads its own rows: WITH RECURSIVE, a start query, UNION ALL, then a repeat query that joins the CTE's own name to the new referrals table (4 rows: Bhavin and Chirag from Asha, Disha from Bhavin, Esha from Disha), which runs round by round on only the previous round's rows (Asha, then Bhavin and Chirag, then Disha, then Esha, then nobody and it stops) giving depth 0, 1, 1, 2, 3, and that a cycle would loop forever because Postgres says the repeat part must eventually return no rows. the next box is arrays and UNNEST, lists inside a cell. earlier baton: 
last visuals: python block with output of ids as bytes plus two hidden answers (column type change), text block of two sessions plus a wait-for arrow picture (deadlocks), step trace table plus a Postgres text block (SELECT FOR UPDATE), comparison table of who waits in four cases (row and table locks), step trace table comparing two levels plus two hidden answers, one with a query and result (serializable), comparison table of counts at two levels plus a query and result (repeatable read), step trace table in a text block plus a query and result (isolation levels, read committed), python block with output run once (phantoms), annotated Postgres session in a text block plus a query and result (non repeatable reads), step trace table plus a query and result (dirty reads), python block with output run two ways (lost updates), python block with output (replaying the log), step table with a hidden query and result (write ahead log), mermaid sequence diagram of commit and flush (durability), python block with output plus two hidden answers, one with a query and result (isolation), step trace table plus a query and result plus a failing query plus a second query and result (ACID consistency), comparison table of four promises plus a query and result plus a failing query (ACID), query and result plus a second query and result plus a small comparison table (COMMIT and ROLLBACK), query and result plus a small comparison table plus a failing query (transactions), comparison table plus a query and result plus a failing query (DROP and TRUNCATE), query and result plus a second query and result plus a failing query (ALTER TABLE), comparison table plus a failing query plus a query and result (upsert), before and after slice table plus a failing query plus a query and result (DELETE), two query and results (UPDATE), query and result plus a second query and result (INSERT from a SELECT), query and result plus a failing query (INSERT), step trace table plus two query and results plus a failing query (sequences), comparison table of three inserts plus two query and results plus a failing query (key constraints), five row trace table plus a query and result plus a failing query (CHECK), query and result plus a failing query plus a second query and result (UNIQUE), query and result plus two failing queries (NOT NULL and DEFAULT), two column step by step trace table in a text block plus a query and result (temporary tables), query and result plus a second query and result (CREATE TABLE), two column step by step trace table in a text block (connections and sessions), text diagram of clients and a server (a database server), annotated command plus a small comparison table (running Postgres in a container), step by step trace table (images and containers), comparison table plus a text diagram (containers), text assembly diagram plus a query and result plus two hidden query and result answers (capstone, first order and days between), lookup table plus a query and result plus ten hidden query and result answers (practice, ten interview questions), query and result plus a second query and result (querying JSON), slice table plus a query and result plus a second query and result (arrays and UNNEST), traced round table plus a query and result (recursive CTEs), traced table per customer plus a query and result plus two hidden query and result answers (retention), before and after table plus a query and result plus two hidden query and result answers (cohorts), query and result plus two hidden query and result answers (session ids), query and result plus two hidden answers, one with a query and result (session starts), query and result plus two hidden query and result answers (date spines), query and result plus python block plus two hidden query and result answers (generate_series), text before and after table plus a query and result plus two hidden query and result answers (gaps and islands, one row per streak), python block plus a query and result plus two hidden query and result answers (gaps and islands), query and result plus two hidden query answers (removing duplicates with ROW_NUMBER)
last exits: forward (column type change), stops (deadlocks), stops (SELECT FOR UPDATE), stops (row locks and table locks), forward (serializable), stops (repeatable read), stops (isolation levels, read committed), stops (phantoms), stops (non repeatable reads), stops (dirty reads), stops (lost updates), stops (replaying the log), forward (write ahead log), forward (durability), stops (isolation), stops (ACID consistency), forward (ACID), stops (COMMIT and ROLLBACK), stops (transactions), stops (DROP and TRUNCATE), stops (ALTER TABLE), stops (upsert), stops (DELETE), stops (UPDATE), stops (INSERT from a SELECT), stops (INSERT), forward (sequences), stops (key constraints), stops (CHECK), stops (UNIQUE), stops (NOT NULL and DEFAULT), stops (temporary tables), stops (CREATE TABLE), stops (connections and sessions), stops (a database server), stops (running Postgres in a container), stops (images and containers), stops (containers), forward (capstone, first order and days between), stops (practice, ten interview questions), stops (querying JSON), stops (arrays and UNNEST), stops (recursive CTEs), stops (retention), forward (cohorts), stops (session ids), stops (session starts), stops (date spines), forward (generate_series), stops (gaps and islands, one row per streak), stops (gaps and islands), stops (removing duplicates with ROW_NUMBER)
last reactions: i assumed widening a number would be free like a bigger box, but the size is fixed per column so every row is stored again, i assumed the server would just hang until someone restarted it, but Postgres goes looking for the circle on its own, i expected Esha to get the row back and see delivered, but she gets nothing because the WHERE is rechecked, i assumed a lock meant nobody could look, but row locks block only writers, i figured strict meant waiting in line, but it lets both run and sends one back at the door, i expected stale data to be the bug, but here being out of date on purpose is the feature, i guessed BEGIN was the moment Asha gets her view, but the picture is taken per query, and i found it comforting that the surprise only lives between queries never inside one

## NOTES
log of runs that failed the gate, newest last. format: YYYY-MM-DD: concept failed check: one line on why
2026-10-22: repo baseline failed checks/127.py: date_trunc on ordered_at returns datetime.date in duckdb 1.1 to 1.4.5 (the check expects datetime, with 1.2 and 1.1 also failing 114), so the gate fails before any change; needs a fix outside this run
2026-10-23: repo baseline failed checks/127.py again: same date_trunc type assert, no duckdb from 1.0 to 1.4.5 passes the whole gate, still needs a fix outside this run; mermaid render also failed so no diagrams today
2026-10-23: repo baseline failed checks/127.py: same date_trunc type assert on duckdb 1.4.5 (duckdb 2.0.0 also breaks 8 checks on fetchone), mermaid render failed again; no note written, needs a fix outside this run
2026-10-23: repo baseline failed checks/127.py again: same date_trunc type assert on duckdb 1.4.5 (python3 here is 3.11, duckdb 2.0.0 is only installed for 3.13), no note written, needs a fix outside this run
2026-10-23: repo baseline failed gate setup: python3 here is 3.11 with no duckdb (duckdb 2.0.0 sits only under 3.13 and breaks 8 checks on fetchone, a duckdb 1.4.5 install timed out), mermaid render failed again; no note written, needs a fix outside this run
2026-10-23: repo baseline failed checks/127.py: same date_trunc type assert on duckdb 1.4.5 (installed via python3 -m pip), no note written, needs a fix outside this run
2026-10-26: repo baseline failed checks/127.py, 201.py, 202.py: date_trunc on a DATE returns DATE not TIMESTAMP on duckdb 1.4.1 (python3 here is 3.11, plain pip installs duckdb for 3.13 only), no note written, needs a fix outside this run
2026-10-23: repo baseline failed checks/127.py: same date_trunc type assert on duckdb 1.4.5 (duckdb 2.0.0 breaks 8 checks on fetchone), mermaid render failed again; no note written, needs a fix outside this run
2026-10-24: repo baseline failed checks/008.py and 7 more: pip gives duckdb 2.0.0 for python3 (3.11) and it breaks 8 checks on fetchone (041 also asserts), mermaid render failed again; no note written, needs a fix outside this run
2026-10-24: repo baseline failed checks/008.py and 7 more: pip only gives duckdb 2.0.0 (python3.13) and it breaks 8 checks on fetchone (041 also asserts), no note written, needs a fix outside this run
2026-10-24: repo baseline failed checks/127.py: same date_trunc type assert on duckdb 1.4.5 (pip default is 2.0.0 which breaks 8 checks), mermaid render failed again; no note written, needs a fix outside this run
2026-10-28: repo baseline failed gate setup: gate fails on untouched repo (python3 is 3.11 without duckdb; duckdb 2.0.0 breaks 8 checks on fetchone and 041 asserts; duckdb 1.3.2 also fails 180 on a CTE name), mermaid render failed (chrome needs no-sandbox as root); no note written, needs a fix outside this run
2026-10-24: repo baseline failed checks/008.py and 7 more: only duckdb 2.0.0 is installed (for python 3.13) and it breaks 8 checks on fetchone (041 also asserts), mermaid render failed again; no note written, needs a fix outside this run
2026-10-24: repo baseline failed checks/011.py and 7 more: python3 is 3.11 with no duckdb, only duckdb 2.0.0 under python3.13 and it breaks 8 checks on fetchone (041 also asserts), no note written, needs a fix outside this run
2026-10-25: repo baseline failed checks/127.py and 201, 202: same date_trunc type asserts on duckdb 1.4.5 (1.4.0 to 1.4.1 fail the same 3, 2.0.0 breaks 8 checks on fetchone), mermaid render failed again; no note written, needs a fix outside this run
2026-10-25: repo baseline failed checks/127.py and 201, 202 again: same date_trunc type asserts on duckdb 1.4.5 (python3 is 3.11 and needs python3 -m pip for duckdb), mermaid not retried; no note written, needs a fix outside this run
2026-10-25: repo baseline failed checks/011.py and 7 more: python3 is 3.11, pip gives duckdb 2.0.0 which breaks 8 checks on fetchone (041 also asserts), 1.4.5 still fails 127, 201, 202 on date_trunc types, mermaid render failed again; no note written, needs a fix outside this run
2026-10-25: repo baseline failed checks/008.py and 7 more: python3 is 3.11 with no duckdb; duckdb 2.0.0 and 1.5.6 both break 8 checks on fetchone (041 also asserts), 1.4.5 fails 127, 201, 202 on date_trunc types, mermaid render failed again; no note written, needs a fix outside this run
2026-10-25: repo baseline failed checks/008.py and 7 more: python3 is 3.11 with no duckdb, duckdb 2.0.0 (python 3.13) breaks 8 checks on fetchone (041 also asserts), no older duckdb passes 127, 201, 202 on date_trunc types; no note written, needs a fix outside this run
2026-10-26: repo baseline failed checks/127.py and 201, 202: same date_trunc type asserts on duckdb 1.4.5 (pip default 2.0.0 breaks 8 checks on fetchone, 041 also asserts), no note written, needs a fix outside this run
2026-10-26: repo baseline failed checks/008.py and 7 more: /usr/bin/python3 has duckdb 2.0.0 which breaks 8 checks on fetchone (041 also asserts), python3 on PATH is 3.11 with no duckdb, no older duckdb passes 127, 201, 202 on date_trunc types; no note written, needs a fix outside this run
2026-10-26: repo baseline failed checks/127.py and 201, 202 again: duckdb 1.4.5 date_trunc type asserts, 2.0.0 breaks 8 checks on fetchone, no note written, needs a fix outside this run
2026-10-26: repo baseline failed checks/127.py and 201, 202 again: duckdb 1.4.5 date_trunc type asserts (python3 is 3.11, pip default 2.0.0 breaks 8 checks on fetchone), no note written, needs a fix outside this run
2026-10-26: repo baseline failed checks/127.py and 201, 202 yet again: duckdb 1.4.5 date_trunc type asserts, no note written, needs a fix outside this run
2026-10-26: repo baseline failed checks/008.py and 7 more: /usr/bin/python3 has duckdb 2.0.0 which breaks 8 checks on fetchone (041 also asserts), python3 on PATH is 3.11 with no duckdb, no note written, needs a fix outside this run
2026-10-26: repo baseline failed checks/127.py and 201, 202 again: duckdb 1.4.5 date_trunc type asserts (python3 is 3.11, pip default gives no duckdb for it), no note written, needs a fix outside this run
2026-10-26: repo baseline failed checks/008.py and 7 more: /usr/bin/python3 has duckdb 2.0.0 which breaks 8 checks on fetchone (041 also asserts), duckdb below 2 has no wheel here and its source build never finished, mermaid render failed again; no note written, needs a fix outside this run
2026-10-26: repo baseline failed checks/127.py and 201, 202 again: duckdb 1.4.5 date_trunc type asserts (python3 is 3.11, pip default gives no usable duckdb), no note written, needs a fix outside this run
2026-10-26: repo baseline failed checks/028.py, 029, 030, 041 and 4 more: pip gives duckdb 2.0.0 (fetchone on relations removed, 041 asserts), python3 on PATH is 3.11 with no duckdb, no note written, needs a fix outside this run
2026-10-27: repo baseline failed checks/127.py and 201, 202 again: duckdb 1.4.5 date_trunc type asserts (pip default 2.0.0 breaks 8 checks on fetchone, 041 also asserts), mermaid render ok; no note written, needs a fix outside this run
2026-10-27: repo baseline failed checks/127.py, 201.py, 202.py: date_trunc type asserts fail on duckdb 1.4.4 (1.3.2 and older fail more, 2.0.0 breaks fetchone), python3 here is 3.11 so plain pip installs duckdb for 3.13 only, mermaid render failed again; no note written, needs a fix outside this run
2026-10-27: repo baseline failed checks/180.py, 201.py, 202.py and 2 more: on duckdb 1.3.2 (installed with python3 -m pip, since python3 is 3.11) 180 errors on a CTE named orders and 201/202 assert, 2.0.0 breaks 8 checks on fetchone, mermaid render failed again; no note written, needs a fix outside this run
2026-10-27: repo baseline failed checks/127.py, 201.py, 202.py: date_trunc type asserts fail on duckdb 1.4.4 (python3 is 3.11, installed with python3 -m pip), no note written, needs a fix outside this run
2026-10-27: repo baseline failed checks/028.py, 029, 030, 041 and 4 more: /usr/bin/python3 has duckdb 2.0.0 (fetchone on relations removed, 041 asserts), python3 on PATH is 3.11 with no duckdb, 1.4.x fails 127, 201, 202 on date_trunc types, mermaid render failed again; no note written, needs a fix outside this run
2026-10-27: repo baseline failed checks/127.py, 180.py, 201.py, 202.py: on duckdb 1.3.2 date_trunc on a DATE returns DATE (127, 201, 202) and 180 hits a circular CTE name; duckdb 2.0.0 breaks 8 checks on fetchone; no duckdb version passes the whole gate, no note written, needs a fix outside this run
2026-10-28: repo baseline failed checks/127.py, 201.py, 202.py: date_trunc type asserts on duckdb 1.4.5 (python3 is 3.11, plain pip gives duckdb 2.0.0 for 3.13 only), mermaid render failed too; no note written, needs a fix outside this run

2026-10-28: repo baseline failed checks/011.py and 7 more: pip gives only duckdb 2.0.0 for python 3.11 and it breaks 8 checks on fetchone (041 also asserts), mermaid render also fails (chromium refuses to run as root without --no-sandbox); no note written, needs a fix outside this run
2026-10-28: repo baseline failed checks/030.py and 041.py and note 180: duckdb 1.3.2 and 1.4.5 fail fetchone in 030, an assert in 041 and a circular CTE in 180, duckdb 2.0.0 breaks 8 checks on fetchone, mermaid render failed again; no note written, needs a fix outside this run
2026-10-28: repo baseline failed checks/127.py, 201.py, 202.py: date_trunc on a DATE asserts on duckdb 1.4.5 (2.0.0 breaks 8 checks on fetchone), mermaid render failed (chromium needs --no-sandbox as root); no note written, needs a fix outside this run
2026-10-28: repo baseline failed checks/030.py and 041.py and 6 more: pip gives duckdb 2.0.0 for python 3.11 (fetchone on relations removed, 041 asserts), mermaid render failed again; no note written, needs a fix outside this run

## arc 1: data at the atom level
after this arc: you know what a computer actually stores when it "saves" an order

- [x] data is facts written down, and a computer can only keep numbers (note 001)
- [x] bits: everything is a tiny switch, on or off (note 002)
- [x] counting in binary (note 003)
- [x] bytes: 8 bits, 256 possible values ★ (note 004)
- [x] hexadecimal: counting with sixteen digits (note 005)
- [x] one byte, two hex digits: why ff is 255 ★ (note 006)
- [x] text is numbers: one character, one number (note 007)
- [x] ASCII runs out: 128 characters isnt enough for the world (note 008)
- [x] unicode: one number for every character in every script ★ (note 009)
- [x] utf-8: storing those numbers in 1 to 4 bytes ★ (note 010)
- [x] why a gujarati letter takes 3 bytes and "g" takes 1 ★ (note 011)
- [x] combining marks: when one letter on screen is two numbers ★ (note 012)
- [x] negative numbers: the sign bit idea (note 013)
- [x] twos complement: how computers really store a minus (note 014)
- [x] integer sizes: 8, 16, 32 and 64 bit numbers (note 015)
- [x] overflow: what happens when a count goes past the top ★ (note 016)
- [x] fractions in binary: halves, quarters, eighths (note 017)
- [x] why 0.1 has no exact binary form ★ (note 018)
- [x] floating point: digits plus where the point sits (note 019)
- [x] why 0.1 + 0.2 is not exactly 0.3 ★ (note 020)
- [x] storing money as whole cents ★ (note 021)
- [x] exact decimal types: exact digits up to the scale you choose ★ (note 022)
- [x] true and false: the boolean (note 023)
- [x] UTC: the worlds reference clock ★ (note 024)
- [x] unix time: counting seconds from 1970 (note 025)
- [x] seconds, milliseconds, microseconds: one moment, three numbers ★ (note 026)
- [x] dates without times, and times without dates (note 027)
- [x] time zones: offsets from UTC ★ (note 028)
- [x] daylight saving: the hour that happens twice ★ (note 029)
- [x] store in UTC, show in local time ★ (note 030)
- [x] null: a marker for a missing value ★ (note 031)
- [x] null is not zero and not empty text ★ (note 032)
- [x] kilobytes to terabytes: how big data gets (note 033)
- [x] capstone: one shop order decoded down to bytes (note 034)

## arc 2: memory, disks and files
after this arc: you know where data lives, why reading it is slow, and how to peek at it

- [x] the processor: the part that does the work (note 035)
- [x] memory vs disk: one forgets when the power goes off, one remembers (note 036)
- [x] disk is slow: memory vs SSD vs spinning disk, in real numbers ★ (note 037)
- [x] 1000 or 1024: why your drive looks smaller than the box said (note 038)
- [x] a file is a named list of bytes (note 039)
- [x] folders and paths (note 040)
- [x] text files vs binary files (note 041)
- [x] line endings: the invisible characters that break files ★ (note 042)
- [x] reading start to end vs jumping to a spot ★ (note 043)
- [x] disks read in blocks, never single bytes (note 044)
- [x] torn writes: what a half finished write leaves behind ★ (note 045)
- [x] writing safely: write a new file, then rename it ★ (note 046)
- [x] compression: making files smaller by spotting repeats (note 047)
- [x] compression trades processor time for disk space (note 048)
- [x] the terminal: running programs by typing (note 049)
- [x] processes: a program while it runs (note 050)
- [x] the operating system: the program that shares the machine out (note 051)
- [x] the working directory: where the terminal is standing (note 052)
- [x] absolute vs relative paths ★ (note 053)
- [x] head and tail: looking at the start and end of a file (note 054)
- [x] wc: counting lines (note 055)
- [x] grep: finding the lines that match (note 056)
- [x] standard input and output: how programs pass text along (note 057)
- [x] pipes: chaining small programs together ★ (note 058)
- [x] redirecting output into a file (note 059)
- [x] capstone: the life of one saved order, memory to disk and back (note 060)

## arc 3: giving data a shape
after this arc: you can read and write the text formats data and config actually travel in

- [x] structure: why a pile of text is hard to ask questions of (note 061)
- [x] CSV: rows and columns separated by commas (note 062)
- [x] quoting: commas inside values ★ (note 063)
- [x] quotes inside quotes, and newlines inside values ★ (note 064)
- [x] the header row: naming the columns (note 065)
- [x] JSON: records with names on every value (note 066)
- [x] JSON types: strings, numbers, booleans, null, objects and arrays ★ (note 067)
- [x] nesting: records and lists inside records (note 068)
- [x] JSON lines: one record per line ★ (note 069)
- [x] flattening nested objects into columns ★ (note 070)
- [x] exploding lists into many rows ★ (note 071)
- [x] XML: the older cousin you will still meet (note 072)
- [x] YAML: indentation as structure (note 073)
- [x] YAML traps: when no means false ★ (note 074)
- [x] schema: the agreement about shape (note 075)
- [x] data types in a schema (note 076)
- [x] required vs optional fields ★ (note 077)
- [x] capstone: the shop orders as raw text, CSV and JSON side by side (note 078)

## arc 4: tables, keys and relationships
after this arc: you can look at four tables and see how they connect, before writing any SQL

- [x] a table: rows are records, columns are fields (note 079)
- [x] every column holds one type (note 080)
- [x] why a shared spreadsheet breaks when many people use it (note 081)
- [x] a database: a program that guards your data files (note 082)
- [x] schema on write vs schema on read ★ (note 083)
- [x] a network: computers sending bytes to each other (note 084)
- [x] addresses and ports: the right program on the right machine (note 085)
- [x] client and server: you ask, the database answers (note 086)
- [x] primary key: one unique id per row ★ (note 087)
- [x] natural keys vs made up ids ★ (note 088)
- [x] update anomalies: change it in one place, miss the other ★ (note 089)
- [x] insert and delete anomalies: losing facts by accident (note 090)
- [x] splitting into tables: each fact lives in one place (note 091)
- [x] relationships: one customer, many orders (note 092)
- [x] foreign key: a column that points at another tables key ★ (note 093)
- [x] what a foreign key stops: rows pointing at nothing (note 094)
- [x] composite keys: a key made of two columns ★ (note 095)
- [x] why many to many cant live in either table (note 096)
- [x] junction tables: the table in the middle ★ (note 097)
- [x] entity relationship diagrams: boxes and lines (note 098)
- [x] crows feet: reading one and many on the lines (note 099)
- [x] capstone: the whole shop as four connected tables (note 100)

## arc 5: asking questions with SQL
after this arc: you can pull exactly the rows and columns you want from one table

- [x] SQL: you describe the result, the database figures out how ★ (note 101)
- [x] a database in one file: setting up DuckDB (note 102)
- [x] your first query against the shop (note 103)
- [x] SELECT and FROM: picking columns (note 104)
- [x] SELECT star: everything, and why you rarely want it (note 105)
- [x] WHERE: keeping only the rows that match ★ (note 106)
- [x] comparisons: equal, not equal, bigger, smaller (note 107)
- [x] AND and OR (note 108)
- [x] parentheses: AND runs before OR, the precedence trap ★ (note 109)
- [x] NOT: flipping a condition ★ (note 110)
- [x] IN: matching against a list (note 111)
- [x] BETWEEN: ranges that include both ends ★ (note 112)
- [x] LIKE: matching text patterns (note 113)
- [x] three valued logic: true, false and unknown ★ (note 114)
- [x] IS NULL and IS NOT NULL (note 115)
- [x] COALESCE: a fallback when a value is NULL (note 116)
- [x] ORDER BY: sorting by one or more columns (note 117)
- [x] no ORDER BY, no promised order ★ (note 118)
- [x] where NULLs land when you sort ★ (note 119)
- [x] LIMIT and OFFSET: paging through rows (note 120)
- [x] DISTINCT: removing duplicate rows (note 121)
- [x] computed columns and AS (note 122)
- [x] CASE WHEN: if and else inside a query ★ (note 123)
- [x] text functions: lower, upper, length, trim (note 124)
- [x] concatenating text, and taking pieces of it (note 125)
- [x] date parts: pulling out the year, month and day (note 126)
- [x] truncating timestamps to a day or a month ★ (note 127)
- [x] adding and subtracting intervals ★ (note 128)
- [x] the difference between two dates (note 129)
- [x] NULLIF and dividing by zero (note 130)
- [x] integer division: when 7 / 2 gives 3 ★ (note 131)
- [x] CAST: changing a values type (note 132)
- [x] casts that fail, and TRY_CAST ★ (note 133)
- [x] the order SQL really runs in: FROM, WHERE, SELECT, ORDER BY, LIMIT ★ (note 134)
- [x] one language, many dialects: why SQL differs between databases (note 135)
- [x] capstone: one query traced clause by clause (note 136)

## arc 6: summarizing data
after this arc: you can turn thousands of rows into the few numbers someone actually asked for

- [x] aggregate functions: many rows in, one value out (note 137)
- [x] COUNT star vs COUNT of a column: nulls dont count ★ (note 138)
- [x] COUNT DISTINCT (note 139)
- [x] SUM and AVG (note 140)
- [x] what NULLs do to SUM and AVG ★ (note 141)
- [x] MIN and MAX (note 142)
- [x] GROUP BY: one group per value ★ (note 143)
- [x] grouping by more than one column (note 144)
- [x] the GROUP BY rule: every column is grouped or aggregated ★ (note 145)
- [x] HAVING: filtering whole groups (note 146)
- [x] WHERE vs HAVING: before grouping vs after ★ (note 147)
- [x] conditional aggregation: counting several things in one pass ★ (note 148)
- [x] median: the middle value after sorting ★ (note 149)
- [x] percentiles: the medians cousins, like the 90th ★ (note 150)
- [x] pivoting: turning rows into columns (note 151)
- [x] ROLLUP: subtotals and grand totals (note 152)
- [x] the full run order with GROUP BY and HAVING ★ (note 153)
- [x] capstone: orders per customer, traced from rows to groups (note 154)

## arc 7: combining tables with joins
after this arc: you can answer questions whose answers live across several tables, without double counting

- [x] why joins: the answer lives in more than one table (note 155)
- [x] inner join traced by hand ★ (note 156)
- [x] ON: how a join decides which rows match (note 157)
- [x] table aliases (note 158)
- [x] left join: keep every row from the left table ★ (note 159)
- [x] the nulls a left join creates (note 160)
- [x] a WHERE that quietly turns a left join into an inner join ★ (note 161)
- [x] right and full outer joins (note 162)
- [x] joining three tables (note 163)
- [x] fan out: when a join multiplies rows ★ (note 164)
- [x] double counting: why sums after a fan out lie ★ (note 165)
- [x] joining on columns that can be NULL ★ (note 166)
- [x] anti join: rows with no match ★ (note 167)
- [x] self join (note 168)
- [x] cross join: every row with every row (note 169)
- [x] joining on a range: matching a date to a period (note 170)
- [x] joins plus GROUP BY: revenue per customer ★ (note 171)
- [x] practice: five join questions on the shop, checking row counts ★ (note 172)
- [x] capstone: the shop revenue report from four tables (note 173)

## arc 8: bigger queries
after this arc: you can write the multi step queries real reports need

- [x] subquery in WHERE ★ (note 174)
- [x] subquery in FROM (note 175)
- [x] scalar subqueries: one value inside a query (note 176)
- [x] correlated subqueries: a query that depends on the outer row ★ (note 177)
- [x] EXISTS and NOT EXISTS: semi joins and anti joins as questions ★ (note 178)
- [x] NOT IN and the NULL trap ★ (note 179)
- [x] CTEs: naming each step with WITH ★ (note 180)
- [x] views: a saved query with a name ★ (note 181)
- [x] UNION and UNION ALL ★ (note 182)
- [x] INTERSECT and EXCEPT (note 183)
- [x] window functions: a total next to every row ★ (note 184)
- [x] OVER: the window a function looks through (note 185)
- [x] PARTITION BY: a separate window per group ★ (note 186)
- [x] ROW_NUMBER: numbering rows in order ★ (note 187)
- [x] RANK vs DENSE_RANK: what ties do ★ (note 188)
- [x] running totals ★ (note 189)
- [x] window frames: ROWS BETWEEN ★ (note 190)
- [x] the default frame trap: why adding ORDER BY turns MAX into a running max ★ (note 191)
- [x] LAG and LEAD: looking at the row before ★ (note 192)
- [x] top N per group ★ (note 193)
- [x] removing duplicates with ROW_NUMBER ★ (note 194)
- [x] gaps and islands: date minus row number stays constant inside a streak ★ (note 195)
- [x] gaps and islands: grouping each island into one streak row ★ (note 196)
- [x] generate_series: a column of consecutive days ★ (note 197)
- [x] date spines: left join the days to orders, empty days become 0 ★ (note 198)
- [x] session starts: LAG the time gap and flag the click that opens a new session ★ (note 199)
- [x] session ids: a running sum of the flags numbers each session ★ (note 200)
- [x] cohorts: the month each customer first showed up ★ (note 201)
- [x] retention: counting who came back the month after ★ (note 202)
- [x] recursive CTEs: following a chain of rows (note 203)
- [x] arrays and UNNEST: lists inside a cell (note 204)
- [x] querying JSON inside a column (note 205)
- [x] practice: ten interview style SQL questions on the shop ★ (note 206)
- [x] capstone: each customers first order and the days between orders (note 207)

## arc 9: changing data safely
after this arc: you can change data and know exactly what happens when two people do it at once

- [x] containers: a program packed with everything it needs ★ (note 208)
- [x] images and containers: the packed box and the running copy ★ (note 209)
- [x] running Postgres in a container on your laptop (note 210)
- [x] a database server: Postgres, where most app data lives (note 211)
- [x] connections and sessions: one conversation with the database (note 212)
- [x] CREATE TABLE (note 213)
- [x] temporary tables (note 214)
- [x] NOT NULL and DEFAULT: required columns and fallback values ★ (note 215)
- [x] UNIQUE: no two rows may share a value ★ (note 216)
- [x] CHECK: a rule every value must pass ★ (note 217)
- [x] key constraints the database enforces for you ★ (note 218)
- [x] where ids come from: sequences and auto increment ★ (note 219)
- [x] INSERT (note 220)
- [x] INSERT from a SELECT (note 221)
- [x] UPDATE, and why the WHERE matters so much ★ (note 222)
- [x] DELETE ★ (note 223)
- [x] upsert: insert, or update if the row is already there ★ (note 224)
- [x] ALTER TABLE: adding a column (note 225)
- [x] DROP and TRUNCATE (note 226)
- [x] transactions: all or nothing ★ (note 227)
- [x] COMMIT and ROLLBACK (note 228)
- [x] ACID: four promises a database makes ★ (note 229)
- [x] ACID consistency: the rules still hold after every change (note 230)
- [x] isolation: two people at the same time ★ (note 231)
- [x] durability: surviving a crash (note 232)
- [x] the write ahead log: write down the plan before the change ★ (note 233)
- [x] replaying the log after a crash (note 234)
- [x] lost updates ★ (note 235)
- [x] dirty reads ★ (note 236)
- [x] non repeatable reads ★ (note 237)
- [x] phantoms ★ (note 238)
- [x] isolation levels: read committed ★ (note 239)
- [x] repeatable read: rows dont change under you mid transaction ★ (note 240)
- [x] serializable: as if one at a time, and retrying the failures ★ (note 241)
- [x] row locks and table locks (note 242)
- [x] SELECT FOR UPDATE: locking on purpose ★ (note 243)
- [x] deadlocks ★ (note 244)
- [x] changing a column type: the table rewrite and the lock ★ (note 245)
- [ ] changing a column type without downtime: add, backfill, swap ★
- [ ] MVCC: every row keeps versions ★
- [ ] transaction snapshots: what your transaction is allowed to see ★
- [ ] backups: a copy you can restore from
- [ ] point in time recovery: a backup plus the replayed log
- [ ] capstone: placing an order as one transaction

## arc 10: designing tables
after this arc: you can design the tables for a new feature and defend every choice

- [ ] modeling: deciding the tables before writing them
- [ ] entities and attributes
- [ ] one to one: when two tables share a key
- [ ] normal forms: the rules behind splitting tables ★
- [ ] functional dependency: when one column decides another ★
- [ ] first normal form: one value per cell ★
- [ ] second normal form ★
- [ ] third normal form ★
- [ ] denormalization: copying data on purpose ★
- [ ] choosing column types well ★
- [ ] naming conventions
- [ ] created_at and updated_at ★
- [ ] soft deletes: marking a row gone instead of removing it ★
- [ ] schemas as namespaces: folders for tables
- [ ] capstone: modeling product reviews for the shop

## arc 11: tricks that make data fast
after this arc: you know the handful of ideas every database, index and big data tool is built on

- [ ] big O in plain words: how work grows as data grows ★
- [ ] the shapes of growth: flat, straight line, curving up ★
- [ ] a loop inside a loop: why some code gets slow so fast ★
- [ ] binary search: finding one item in sorted data by halving ★
- [ ] sorting: how merge sort splits and merges ★
- [ ] why sorting costs more than one pass over the data
- [ ] hash functions: turning anything into a number in a fixed range ★
- [ ] hash tables: how a dictionary finds a key without searching ★
- [ ] collisions: when two keys land in the same spot
- [ ] trees: data that branches
- [ ] balanced trees: why the depth stays small ★
- [ ] the trade off: faster reads usually mean slower writes ★
- [ ] capstone: the same lookup done three ways, scan, halving and hash

## arc 12: inside a database server
after this arc: you know what happens inside Postgres between sending a query and getting rows back, and why some queries are slow

- [ ] how Postgres keeps a table on disk: rows packed into pages
- [ ] full table scan: reading every page ★
- [ ] index: a sorted shortcut ★
- [ ] B tree: pages that point to pages ★
- [ ] one lookup traced through a B tree ★
- [ ] how a B tree stays balanced as rows arrive
- [ ] composite indexes: sorted by the first column, then the second ★
- [ ] the leftmost prefix rule ★
- [ ] covering index
- [ ] what indexes cost: slower writes, more disk ★
- [ ] selectivity: when an index doesnt help ★
- [ ] queries that cant use the index: functions on a column ★
- [ ] the query planner ★
- [ ] statistics: how the planner guesses row counts
- [ ] nested loop join ★
- [ ] hash join ★
- [ ] merge join
- [ ] reading EXPLAIN: the plan as a tree ★
- [ ] EXPLAIN ANALYZE: the planners guesses vs what really happened ★
- [ ] the buffer pool: keeping hot pages in memory
- [ ] vacuum: how Postgres cleans up old row versions ★
- [ ] capstone: one query from SQL text to rows on disk

## arc 13: talking over a network
after this arc: you can explain how data travels between machines safely, and what an API really is

- [ ] DNS: turning names into addresses
- [ ] URLs and query parameters
- [ ] request and response ★
- [ ] HTTP methods: GET, POST and friends ★
- [ ] HTTP headers: notes attached to a request
- [ ] status codes: what 200, 404 and 500 mean ★
- [ ] APIs: a program built to be asked questions ★
- [ ] JSON over HTTP: what an API answer looks like
- [ ] API keys: a password for programs ★
- [ ] tokens that expire: access tokens and refresh tokens ★
- [ ] OAuth in one picture: getting a token without sharing a password ★
- [ ] encryption: locking data so only a key opens it ★
- [ ] public and private keys: locking without sharing a secret ★
- [ ] cryptographic hashes: fingerprints you cant reverse ★
- [ ] certificates: proving whose public key it is
- [ ] encryption in transit: TLS and https
- [ ] latency and bandwidth: slow vs narrow ★
- [ ] capstone: one shop order fetched from an imaginary API, hop by hop

## arc 14: python for data work
after this arc: you can write, run and test real python scripts that move data between files, APIs and a database

- [ ] modules and imports: using code from other files
- [ ] running a python script from the terminal
- [ ] packages and venvs: other peoples code, kept per project
- [ ] git: commits as snapshots of your code ★
- [ ] git branches: trying something without breaking main
- [ ] pushing and pulling: sharing code through a remote
- [ ] pull requests and merge conflicts ★
- [ ] errors in scripts: catching them without hiding them ★
- [ ] with: opening and closing things safely ★
- [ ] classes in one picture: data and functions together
- [ ] functions as values: passing and returning functions
- [ ] decorators: the @ shorthand for wrapping a function ★
- [ ] reading a CSV in python, row by row
- [ ] reading JSON in python
- [ ] environment variables: settings that live outside the code ★
- [ ] calling an API from python ★
- [ ] practice: dedupe and count orders in plain python ★
- [ ] a dataframe: a table in memory
- [ ] filter, select and sort in pandas, next to the SQL
- [ ] groupby in pandas ★
- [ ] merging dataframes: joins again ★
- [ ] connecting python to a database
- [ ] connection pools: why opening a connection is expensive
- [ ] parameters, never string building: SQL injection ★
- [ ] bulk loading: COPY instead of one INSERT per row ★
- [ ] generators: one row at a time ★
- [ ] data bigger than memory: reading in chunks ★
- [ ] dates and time zones in python ★
- [ ] logging: leaving a trail for later
- [ ] tests: code that checks your code ★
- [ ] testing a transformation with a tiny input table ★
- [ ] SQL or dataframe: picking the tool ★
- [ ] capstone: a tested script that loads a CSV into a table

## arc 15: cleaning messy data
after this arc: you can take data from the real world and make it trustworthy

- [ ] why real data is messy: where the mess comes from
- [ ] garbled text: bytes read with the wrong encoding ★
- [ ] standardizing text: case, spaces, spelling ★
- [ ] parsing dates written ten different ways ★
- [ ] missing values in the wild: blanks, "N/A" and 9999 ★
- [ ] type problems: numbers stored as text ★
- [ ] units and currencies
- [ ] exact duplicates vs near duplicates ★
- [ ] matching records: exact keys vs fuzzy matching ★
- [ ] similarity scores: how close is close enough
- [ ] outliers: wrong, or just rare ★
- [ ] regular expressions: character classes, repeats and anchors
- [ ] capture groups: pulling pieces out of messy text
- [ ] never clean in place: keep the raw copy ★
- [ ] capstone: a messy export of shop orders, cleaned step by step

## arc 16: databases built for analysis
after this arc: you know why analytics databases store data sideways, and how that makes big questions cheap

- [ ] OLTP vs OLAP: running the app vs answering questions ★
- [ ] row storage: whole rows together
- [ ] column storage: whole columns together ★
- [ ] why column storage makes SUM fast ★
- [ ] why columns compress so well
- [ ] run length encoding ★
- [ ] dictionary encoding ★
- [ ] Parquet: a file stored by column ★
- [ ] row groups and min max stats: skipping data you dont need ★
- [ ] Avro: rows with the schema attached
- [ ] partitioning files by date ★
- [ ] partition pruning ★
- [ ] the data warehouse ★
- [ ] capstone: the same question on a row store and a column store

## arc 17: modeling for analytics
after this arc: you can design the tables a dashboard reads from

- [ ] fact tables: the measurements ★
- [ ] grain: what one row means ★
- [ ] additive measures: safe to sum
- [ ] semi additive measures: balances you cant sum over time ★
- [ ] non additive measures: ratios and averages ★
- [ ] dimension tables: the context ★
- [ ] the four step design: process, grain, dimensions, facts ★
- [ ] star schema ★
- [ ] snowflake schema
- [ ] surrogate keys in the warehouse ★
- [ ] the date dimension
- [ ] slowly changing dimensions: what if a customer moves ★
- [ ] SCD type 1: overwrite
- [ ] SCD type 2: a new row for every change ★
- [ ] valid from, valid to and the current flag ★
- [ ] joining a fact to the right version of a dimension ★
- [ ] the unknown member: facts that arrive before their dimension ★
- [ ] transaction fact tables
- [ ] periodic snapshot fact tables ★
- [ ] accumulating snapshot fact tables ★
- [ ] factless fact tables: recording that something happened
- [ ] role playing dimensions: one date table, three meanings
- [ ] bridge tables: many to many in a star
- [ ] conformed dimensions ★
- [ ] one big table vs a star ★
- [ ] modeling event data for product analytics ★
- [ ] data vault in one picture
- [ ] practice: model shop returns from a one paragraph request ★
- [ ] capstone: the shop as a star schema

## arc 18: the cloud in plain words
after this arc: you know what "in the cloud" means when someone says the data lives there

- [ ] the cloud: renting someone elses computers
- [ ] regions and zones: where the computers are
- [ ] virtual machines and serverless functions
- [ ] managed services: paying someone to run the database
- [ ] private networks and firewalls in the cloud
- [ ] identities: users and service accounts
- [ ] roles and policies: what an identity may do ★
- [ ] paying for what you use: how cloud bills work ★
- [ ] object storage: files in buckets ★
- [ ] how a bucket differs from a disk ★
- [ ] reading and writing a bucket from python ★
- [ ] capstone: the shop moved to the cloud, piece by piece

## arc 19: moving data with pipelines
after this arc: you can design a pipeline that survives reruns, late data and changing sources

- [ ] a pipeline: getting data from where it is to where its useful
- [ ] events: something happened, at a time
- [ ] sources: databases, files, APIs and events
- [ ] extract, transform, load ★
- [ ] ETL vs ELT ★
- [ ] full extract vs incremental extract ★
- [ ] the high water mark: remembering where you left off ★
- [ ] why updated_at high water marks miss deletes ★
- [ ] pulling from an API: pagination ★
- [ ] rate limits: what a 429 response tells you
- [ ] retries with exponential backoff: which errors to retry and how long to wait ★
- [ ] files dropped by partners: landing zones
- [ ] managed connectors: Fivetran and Airbyte
- [ ] change data capture: reading the database change log ★
- [ ] what a change event looks like: before, after and operation
- [ ] staging tables ★
- [ ] append loads ★
- [ ] overwrite loads: replacing a whole partition ★
- [ ] merge loads: applying a batch of changes with MERGE ★
- [ ] idempotency: running twice gives the same result ★
- [ ] making a load idempotent: delete then insert, or merge ★
- [ ] duplicates from reruns and retries: dedup keys ★
- [ ] backfills: rerunning the past ★
- [ ] late arriving data ★
- [ ] schema drift: when the source changes shape ★
- [ ] batch sizes and micro batches
- [ ] practice: an incremental load you can run twice safely ★
- [ ] capstone: a daily orders pipeline end to end

## arc 20: data quality
after this arc: you catch bad data before someone makes a decision with it

- [ ] what bad data looks like
- [ ] warehouses accept keys but dont enforce them ★
- [ ] null checks and uniqueness checks
- [ ] orphan checks: foreign keys that point at nothing ★
- [ ] range checks and accepted values
- [ ] row counts and reconciliation ★
- [ ] freshness: is the data late ★
- [ ] volume anomalies: when today looks nothing like yesterday ★
- [ ] where checks go in a pipeline ★
- [ ] quarantine bad rows or stop the pipeline ★
- [ ] data diffs: comparing a table before and after a change ★
- [ ] data contracts ★
- [ ] capstone: a quality gate on the orders pipeline

## arc 21: orchestration
after this arc: you can run many pipelines on a schedule, in the right order, and know when one breaks

- [ ] scheduling: cron in one line
- [ ] tasks and dependencies
- [ ] DAG: a graph with no loops ★
- [ ] retries and timeouts ★
- [ ] task states: success, failed, skipped
- [ ] tasks hand data over through storage ★
- [ ] sensors: waiting for data to land
- [ ] Jinja: templates that fill in text
- [ ] Airflow: a DAG written as a python file ★
- [ ] operators and tasks in Airflow
- [ ] connections and hooks: credentials outside the DAG
- [ ] the Airflow scheduler and workers
- [ ] logical dates: how an orchestrator replays the past ★
- [ ] catchup and backfills in Airflow ★
- [ ] assets: scheduling by data instead of by task
- [ ] other orchestrators: Dagster and Prefect
- [ ] alerting: who finds out, and how
- [ ] capstone: the orders pipeline as a DAG

## arc 22: transformations in the warehouse
after this arc: you can turn raw tables into clean, tested, documented tables people trust

- [ ] layers: raw, cleaned, business ready ★
- [ ] dbt: SQL files as a pipeline ★
- [ ] ref: how dbt knows what runs first ★
- [ ] sources and source freshness ★
- [ ] staging models
- [ ] materializations: view, table, incremental ★
- [ ] incremental models: only process whats new ★
- [ ] incremental strategies: merge, delete and insert, microbatch ★
- [ ] incremental model traps: late rows and full refreshes ★
- [ ] dbt snapshots: keeping history for you
- [ ] tests in dbt ★
- [ ] dbt unit tests: fixed input, expected output ★
- [ ] macros: reusable SQL snippets
- [ ] docs and the lineage graph
- [ ] practice: a dbt project on the shop with sources, marts and tests ★
- [ ] capstone: raw orders to a revenue table, layer by layer

## arc 23: when one machine isnt enough
after this arc: you know what changes when data lives on many machines

- [ ] scale up vs scale out ★
- [ ] replication: copies of the same data ★
- [ ] leader and followers
- [ ] replication lag ★
- [ ] reading your own writes ★
- [ ] sharding: splitting rows across machines ★
- [ ] choosing a shard key ★
- [ ] hot spots ★
- [ ] network partitions: when machines cant reach each other ★
- [ ] CAP: when the network breaks, pick consistency or availability ★
- [ ] what CAP does not say ★
- [ ] eventual consistency ★
- [ ] clocks drift: why two machines disagree on the time ★
- [ ] ordering without clocks: logical clocks
- [ ] consensus: getting machines to agree
- [ ] leader election
- [ ] capstone: the shop running on three machines

## arc 24: other kinds of databases
after this arc: you can pick the right kind of database for a job

- [ ] key value stores
- [ ] document databases ★
- [ ] wide column stores: not the same as column storage ★
- [ ] search indexes: the inverted index ★
- [ ] graph databases
- [ ] time series databases
- [ ] caches: a fast copy in memory
- [ ] cache invalidation: when the copy goes stale ★
- [ ] unstructured data: documents, images and audio
- [ ] machine learning models in one picture
- [ ] embeddings: turning text into a list of numbers ★
- [ ] vector databases: searching by meaning ★
- [ ] picking a database for the job ★
- [ ] capstone: the shop data spread across the right stores

## arc 25: distributed processing
after this arc: you can reason about a job that runs on a hundred machines

- [ ] parallelism: many workers, one job ★
- [ ] Spark partitions: splitting data across workers ★
- [ ] map: work on each piece alone
- [ ] reduce: combine the pieces
- [ ] shuffle: moving data so matching keys meet ★
- [ ] why shuffles are expensive ★
- [ ] HDFS and MapReduce: where big data started
- [ ] Spark: the driver and the executors ★
- [ ] dataframes in Spark
- [ ] Spark SQL and the dataframe API build the same plan ★
- [ ] lazy evaluation: transformations vs actions ★
- [ ] jobs, stages and tasks ★
- [ ] narrow vs wide transformations ★
- [ ] repartition vs coalesce ★
- [ ] data skew: one worker gets everything ★
- [ ] salting: spreading a hot key ★
- [ ] sort merge join: the default for two big tables ★
- [ ] broadcast join ★
- [ ] python UDFs: why theyre slow ★
- [ ] caching in Spark: keeping a reused dataframe in memory
- [ ] reading the Spark UI
- [ ] partitionBy: how many files a write makes ★
- [ ] the small files problem ★
- [ ] compressed files, and why some cant be split ★
- [ ] memory spills: when a worker runs out of room
- [ ] practice: revenue per product in PySpark, then fix a skewed join ★
- [ ] capstone: units sold per product, traced across three workers

## arc 26: lakes and lakehouses
after this arc: you know how cheap file storage became a real database

- [ ] the data lake
- [ ] why a lake turns into a swamp
- [ ] table formats: data files plus metadata files ★
- [ ] manifests: the list of files in one version ★
- [ ] the table catalog: who knows where the current version is ★
- [ ] optimistic commits: swapping one pointer ★
- [ ] two writers at once: who wins ★
- [ ] time travel: reading an old version
- [ ] schema evolution in table formats ★
- [ ] copy on write: rewriting files to change rows ★
- [ ] merge on read: delete files applied at query time ★
- [ ] compaction ★
- [ ] Delta Lake, Iceberg and Hudi by name ★
- [ ] Databricks: Spark, Delta and a catalog as one product ★
- [ ] the lakehouse ★
- [ ] capstone: one write to a lakehouse table, traced

## arc 27: streaming
after this arc: you can process data the moment it happens, and handle events that show up late

- [ ] batch vs streaming ★
- [ ] the log: an append only list of events ★
- [ ] Kafka topics
- [ ] producers and consumers
- [ ] Kafka partitions and ordering ★
- [ ] message keys: keeping related events together ★
- [ ] offsets: a bookmark for each reader ★
- [ ] consumer groups ★
- [ ] retention and compacted topics
- [ ] schemas for events: Avro and a schema registry ★
- [ ] at most once vs at least once ★
- [ ] dead letter queues: where bad events go
- [ ] exactly once: why its hard ★
- [ ] idempotent producers: retried sends without duplicates ★
- [ ] Kafka transactions: output and offsets committed together ★
- [ ] exactly once end to end: the sink matters too ★
- [ ] stream processors: Flink and Spark streaming
- [ ] event time vs processing time ★
- [ ] tumbling windows ★
- [ ] sliding windows
- [ ] session windows ★
- [ ] stream watermarks: deciding a window is done ★
- [ ] allowed lateness: what to do with stragglers ★
- [ ] state: remembering between events ★
- [ ] checkpoints: saving state so a crash loses nothing ★
- [ ] joining a stream to a table ★
- [ ] backpressure: when consumers cant keep up ★
- [ ] Kafka Connect and Debezium: tables into Kafka
- [ ] change data capture as a stream ★
- [ ] capstone: live orders per minute

## arc 28: cloud warehouses and cost
after this arc: you can make a slow, expensive query fast and cheap

- [ ] separating storage from compute ★
- [ ] Snowflake, BigQuery and Redshift: same idea, different knobs
- [ ] loading files from a bucket in bulk ★
- [ ] paying for compute time vs bytes scanned ★
- [ ] virtual warehouses: sizing and auto suspend ★
- [ ] clustering and partitioning in the warehouse ★
- [ ] materialized views ★
- [ ] result caching
- [ ] approximate answers: counting distinct users cheaply ★
- [ ] reading a warehouse query profile ★
- [ ] zero copy clones and time travel in the warehouse ★
- [ ] cost traps: the queries that burn money ★
- [ ] the AWS data services by name: S3, Glue, Athena, EMR, Redshift, Kinesis ★
- [ ] the same services on Google Cloud and Azure
- [ ] capstone: making one expensive query cheap

## arc 29: serving data
after this arc: you know how the data you built reaches people and products

- [ ] dashboards and BI tools: where most data ends up
- [ ] metrics: one definition of revenue for everyone ★
- [ ] the semantic layer ★
- [ ] pre aggregation: choosing which summaries to build ★
- [ ] reverse ETL: sending data back into the apps
- [ ] features: the columns a model learns from ★
- [ ] training sets without peeking at the future ★
- [ ] serving data to an app through an API ★
- [ ] pipelines for AI: chunking documents and loading embeddings ★
- [ ] capstone: one revenue number traced from the dashboard back to the raw order

## arc 30: running data in production
after this arc: you can ship a pipeline other people depend on, and keep it running

- [ ] deployment environments: dev, staging, prod ★
- [ ] code review for data code
- [ ] testing pipelines: more than unit tests ★
- [ ] CI: checks on every change ★
- [ ] a GitHub Actions workflow that tests every pull request ★
- [ ] a Dockerfile, line by line ★
- [ ] images and registries
- [ ] docker compose: Postgres and Airflow together ★
- [ ] Kubernetes in one picture
- [ ] infrastructure as code ★
- [ ] secrets: keeping passwords out of code ★
- [ ] configuration files: one pipeline, many environments
- [ ] logs and metrics ★
- [ ] data observability tools: watching every table at once ★
- [ ] SLAs and SLOs for data: promises about freshness ★
- [ ] on call and runbooks
- [ ] a broken dashboard, debugged step by step ★
- [ ] postmortems: learning without blame
- [ ] capstone: the production checklist for the orders pipeline

## arc 31: governance, security and privacy
after this arc: you handle peoples data like its yours

- [ ] PII: data that points at a person ★
- [ ] least privilege: only the access you need ★
- [ ] access control: who can see what ★
- [ ] row and column level security ★
- [ ] encryption at rest
- [ ] masking: hiding part of a value
- [ ] hashing for privacy ★
- [ ] tokenizing: swapping a value for a stand in
- [ ] why hashing an email doesnt make it anonymous ★
- [ ] privacy laws in plain words: GDPR and CCPA ★
- [ ] retention: keeping data only as long as needed
- [ ] deletion requests: erasing one person from every copy ★
- [ ] audit logs: who looked at what
- [ ] the data catalog: a search engine for your tables
- [ ] capstone: locking down the shop customer data

## arc 32: thinking like a data engineer
after this arc: you can design a data platform from a business question and defend every choice

- [ ] start from the question the data has to answer ★
- [ ] back of the envelope: estimating data size and cost ★
- [ ] batch or streaming: choosing for a real requirement ★
- [ ] lambda and kappa architectures
- [ ] warehouse, lake or lakehouse: choosing ★
- [ ] build vs buy: managed tools ★
- [ ] cost vs freshness vs complexity ★
- [ ] data mesh: who owns the data
- [ ] migrating a pipeline without breaking anyone ★
- [ ] writing down a design decision
- [ ] reading a full data platform diagram ★
- [ ] the interview loop: SQL, python, modeling, design, behavioral ★
- [ ] a design interview: requirements before boxes ★
- [ ] practice: two design interviews out loud, clickstream and Postgres to warehouse ★
- [ ] the shop pipeline on GitHub as a portfolio ★
- [ ] the job: data engineer, analytics engineer and analyst
- [ ] capstone: the whole journey on one map, every arc capstone linked
2026-10-25: repo baseline failed checks/008.py and 7 more: python3 is 3.11, pip gives duckdb 2.0.0 which breaks 8 checks on fetchone (041 also asserts), older duckdb fails 127, 201, 202 on date_trunc types; no note written, needs a fix outside this run
2026-10-26: repo baseline failed checks/008.py and 8 more: duckdb 1.1.3, 1.3.2, 1.5.6 and 2.0.0 all fail (fetchone on relations, 041 assert, 180 CTE circular reference), mermaid render failed; no note written, needs a fix outside this run
2026-10-26: repo baseline failed checks/028.py, 029, 030, 041 and 4 more: only duckdb 2.0.0 is available (fetchone on relations breaks 8 checks, 041 also asserts) and mermaid render failed; no note written, needs a fix outside this run
2026-10-26: repo baseline failed checks/127.py, 201.py, 202.py: date_trunc on a DATE returns DATE not TIMESTAMP on duckdb 1.4.5 (1.3.2 also fails 180 CTE name, 1.2 and 1.1 fail 197; python3 here is 3.11, duckdb 2.0.0 sits only under 3.13 and breaks 8 checks on fetchone), mermaid render failed; no note written, needs a fix outside this run
2026-10-27: repo baseline failed checks/127.py, 201.py, 202.py: same date_trunc DATE vs TIMESTAMP assert on duckdb 1.4.1 (duckdb 2.0.0 breaks 8 checks on fetchone), mermaid render failed too; no note written, needs a fix outside this run
2026-10-27: repo baseline failed gate setup: python3 is 3.11 where only /usr/bin/python3 has duckdb 2.0.0, which breaks checks/008.py to 030.py on fetchone and 041.py, and mermaid render failed; no note written, needs a fix outside this run
2026-10-27: repo baseline failed checks/008.py and 7 more: duckdb 2.0.0 (only version available here) breaks 8 checks on fetchone and 041 asserts, 1.4.x fails the date_trunc asserts in 127, 201, 202; no note written, needs a fix outside this run
2026-10-27: repo baseline failed checks/127.py, 201, 202: duckdb 1.4.5 date_trunc type asserts (pip default 2.0.0 breaks 8 checks on fetchone, 041 also asserts), mermaid render produced no svg; no note written, needs a fix outside this run
2026-10-27: repo baseline failed checks/127.py, 201, 202: duckdb 1.4.2 (2.0.0 breaks 8 checks on fetchone) fails the date_trunc on a DATE type asserts; mermaid render ok; no note written
2026-10-28: repo baseline failed checks/127.py, 201.py, 202.py: date_trunc type assert on duckdb 1.4.0 and 1.4.4 (1.3.2 also breaks 180, 2.0.0 breaks 8 on fetchone), mermaid render failed too; no note written, needs a fix outside this run
2026-10-28: repo baseline failed checks/011.py, 026 to 030, 041: only duckdb 2.0.0 installs here (python3 is 3.11, fetchone on relations breaks 8 checks), mermaid render failed too; no note written, needs a fix outside this run
2026-10-28: repo baseline failed checks/011.py, 026 to 030, 041: duckdb 2.0.0 breaks 8 checks on fetchone, 1.5.6 and 1.2.2 still fail some (1.2.2 also breaks 180 and 041), mermaid render failed too; no note written, needs a fix outside this run
2026-10-28: repo baseline failed checks/127.py, 201.py, 202.py: date_trunc on a DATE type asserts on duckdb 1.4.1 (2.0.0 is the pip default here and breaks 8 checks on fetchone), mermaid render failed too; no note written, needs a fix outside this run
2026-10-28: repo baseline failed checks/127.py, 201.py, 202.py: same date_trunc type asserts on duckdb 1.4.5 (python3 is 3.11, duckdb 2.0.0 only exists for 3.13), mermaid render failed again; no note written, needs a fix outside this run
2026-10-28: repo baseline failed checks/127.py, 201.py, 202.py: date_trunc on a DATE asserts TIMESTAMP on duckdb 1.4.5 (2.0.0 breaks 8 checks on fetchone), mermaid render fails as root without --no-sandbox; no note written, needs a fix outside this run
2026-10-28: repo baseline failed checks/127.py, 201.py, 202.py: same date_trunc type assert on duckdb 1.4.5 under python3.13 (python3 is 3.11 with no duckdb), no note written, needs a fix outside this run
2026-10-28: repo baseline failed gate: no duckdb works (2.0.0 breaks 8 checks on fetchone, 1.4.1 fails 127/201/202 on date_trunc type, 0.10.3 and 1.0.0 fail 22), mermaid render also failed; no note written, needs a fix outside this run
