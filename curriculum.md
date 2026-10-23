# curriculum

the map from zero to data engineer. one checkbox is one atom: one idea small enough for a 2 minute note. big concepts are already broken into several atoms in the order you need them, and a box still gets split further if it turns out bigger than it looks. arcs run in order, boxes inside an arc run in order, and each arc ends with a capstone that assembles its atoms. a ★ marks a concept that is important or easy to get wrong, so its note ends with check yourself questions. every capstone gets them too.

## THREAD
baton: 170 showed that a range join is an ON with a BETWEEN: a timestamp compared with a date end is read as midnight, so order 103 at 12:05 on the last day was missed until the CAST to a date, and a left join kept the 3 orders in no promo (7 in, 7 out). the next box is joins plus GROUP BY, revenue per customer
last visuals: two query and result pairs (range join), python block plus a query and result (cross join), python block plus a query and result (self join), two query and result pairs (anti join), two query and result pairs (NULL join keys), trace table plus a query and result (double counting), two query and result pairs (fan out), query and result plus a failing query (three tables), python block plus a query and result (full join), two query and result pairs (WHERE turns left join into inner), query and result (nulls a left join creates), python block plus a query and result (left join), query and result plus a failing query (table aliases), query and result (ON), trace table plus a query and result (inner join), python block plus a query and result (why joins), text diagram plus a query and result (capstone, orders per customer), trace table plus a query and result (full run order), query and result plus a small query and result (ROLLUP), before table plus two query and result pairs (pivoting), python block plus a query and result plus a small query and result (percentiles), python block plus two query and result pairs (median), query and result plus a small query and result (conditional aggregation), failing query plus trace table plus a query and result (WHERE vs HAVING), query and result plus python block plus a query and result (HAVING), failing query plus python block plus query and result (the GROUP BY rule), query and result plus a small query and result (grouping by more than one column), python block plus two query and result pairs (group by), query and result plus a small query and result (min and max), trace table plus two query and result pairs (nulls in sum and avg), python block plus two query and result pairs (sum and avg), python block plus two query and result pairs (count distinct), query and result plus a small query and result (count star vs count column), query and result plus a small query and result (aggregate functions), text assembly diagram plus a query and result (capstone, one query traced), comparison table plus a query and result (dialects), query and result plus a trace table (order SQL runs in), failing query plus query and result plus a small query and result (TRY_CAST), python block plus a query and result plus a small query and result (CAST), query and result plus a text block (integer division), query and result plus a small query and result (NULLIF), query and result plus a small query and result (date difference), query and result plus a small query and result (intervals), before and after table plus a small query and result (date_trunc), query and result plus a small query and result (date parts), hand traced letter positions plus a query and result (concatenating and substr), two query and result pairs (text functions), two query and result pairs (CASE WHEN), two query and result pairs (computed columns and AS), two query and result pairs plus a small query and result (DISTINCT)
last exits: stops (range join), stops (cross join), stops (self join), stops (anti join), stops (NULL join keys), stops (double counting), stops (fan out), forward (three tables), stops (full join), stops (WHERE turns left join into inner), stops (nulls a left join creates), forward (left join), stops (table aliases), stops (ON), forward (inner join), stops (why joins), forward (capstone, orders per customer), stops (full run order), stops (ROLLUP), forward (pivoting), stops (percentiles), stops (median), forward (conditional aggregation), stops (WHERE vs HAVING), stops (HAVING), stops (the GROUP BY rule), stops (grouping by more than one column), forward (group by), stops (min and max), stops (nulls in sum and avg), stops (sum and avg), stops (count distinct), forward (count star vs count column), stops (aggregate functions), forward (capstone, one query traced), stops (dialects), stops (order SQL runs in), stops (TRY_CAST), forward (CAST), stops (integer division), stops (NULLIF), stops (date difference), stops (intervals), forward (date_trunc), stops (date parts), stops (concatenating and substr), stops (text functions), stops (CASE WHEN), stops (computed columns and AS), forward (DISTINCT)
last reactions: i kept picturing a join as matching ids, and a range join is the cross join loop with a range check as the if, i expected a join with no condition to be an error, and it just runs, i assumed the database needed a real second copy of the table, and its one table with two nicknames, i assumed finding what is missing needed its own kind of join, and its the same left join with one filter, i expected a NULL to at least match its twin, and it doesnt, i figured DISTINCT would undo the copies, but it keeps one of each amount and drops real orders, i read a join as adding columns, and it can photocopy the row instead, i expected a special three way match, and its two ordinary inner joins one after the other, i expected a join to have a favorite side, and a full join just doesnt, i assumed a filter was a filter wherever i put it, and with a left join the spot decides what survives, i trusted count(*) because it never skips anything, and thats exactly why it bites here, i expected the missing partner to stop the row from existing, but the row stays and only the order side is empty, i assumed both names would work since nothing was deleted, and the nickname replaces the real name, i assumed ON had to be an equals between ids, and it takes whatever test you hand it, i kept picturing a direct lookup like customers[4], but the plain version tries every row and keeps the matches, i figured pulling in a second table would make the result bigger, but its 7 rows, the same as orders, i expected a missing customer to show up as a zero, but you cant count rows that dont exist, i kept reading the query top to bottom, and it works like a pipe going WHERE to HAVING to the rest, i expected the totals to need a second query glued on, and its the same query with one word wrapped around the columns, i assumed the columns would appear by themselves from whatever the data holds, they dont and you type every one, i kept reading 90th percentile as 90 percent of the biggest value, and it only cares about position, i figured the middle of an even list would just pick one, and it quietly makes up a number, i assumed a filter always meant losing rows, and this one filters inside the number, i assumed the two filters were interchangeable, and they change what gets counted, i kept reading HAVING as a fussy second WHERE, and it tests something a single row doesnt have yet, i assumed a database would quietly take the first value in the bucket like groups[1][0], and it refuses, i assumed i would get a row for every customer and status combo, and only the pairs that exist show up, i expected GROUP BY to be new machinery, and its the dictionary of lists i already write in python, i assumed max(price) would carry its row along, and it only returns the value, i assumed a missing rating would sit in the average as a quiet zero, and the row just isnt in the vote, i assumed avg was its own special operation, but its just sum over count, i assumed the null would count as its own value since SELECT DISTINCT keeps one, but count distinct skips it, i figured counting only nulls would give NULL like sum did, but count gives 0, i figured an aggregate would add a column next to the rows, but it replaces them, i expected a query this long to be hard to follow, and traced it is 5 small steps, i assumed a standard meant everyone follows it, and LIMIT isnt even in it, i expected SELECT to be first, and its third, i expected a failed cast to skip the row, and it keeps the row with a null in the number, i assumed casting to integer chopped off the decimals like python does, and in DuckDB it rounds, i assumed every database treats / the same way, and Postgres doesnt, i expected a database to refuse a division by zero, and DuckDB hands back nan and carries on, i assumed date_diff counted full days that passed, and it counts how many midnights you cross, i assumed 1 month was just a nickname for 30 days, and it means the same day number next month, i assumed truncating made the clock part disappear, and it just gets set to midnight, i expected the month to come back as the word April, i expected the month to come back as the word April, and its just the number 4, i assumed a missing city would leave a blank and keep the name, and gluing onto a null gives null for the whole label, i assumed a stray space would show up when i looked at the rows, and only the lengths give it away, i expected CASE to look at every branch and pick the best fit, and it just takes the first true one, i assumed a new column like this got saved somewhere, and it only exists in that one result, i read DISTINCT as belonging to the first column after it, and it covers the whole row, i guessed paging was something clever, and its two small words, i assumed every database agrees on where nulls go, and they dont, i expected a boring default, and its really whatever was fastest, i kept assuming a second sort column gets applied to the whole result, and it only breaks ties, i figured COALESCE was a cosmetic wrapper, and it quietly changed what avg divides by, i assumed IS was just a fussy spelling of =, and it turns out to be a different kind of test, one that cant be unknown, i assumed unknown would spread like a stain through everything it touches, and it only spreads when the other side cant settle it, i typed a capital K and got zero rows with no error, so LIKE is exact about letters, i kept reading BETWEEN like python range where the last number is left out, and here nothing is left out, i expected a list to be forgiving about nulls, and a null in the list is where it bites, i assumed NOT was a clean mirror where every row lands on one side, and a null row lands on neither, i expected the database to read left to right like i do, and it quietly grabs the AND first

## NOTES
log of runs that failed the gate, newest last. format: YYYY-MM-DD: concept failed check: one line on why
2026-10-22: repo baseline failed checks/127.py: date_trunc on ordered_at returns datetime.date in duckdb 1.1 to 1.4.5 (the check expects datetime, with 1.2 and 1.1 also failing 114), so the gate fails before any change; needs a fix outside this run

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
- [ ] joins plus GROUP BY: revenue per customer ★
- [ ] practice: five join questions on the shop, checking row counts ★
- [ ] capstone: the shop revenue report from four tables

## arc 8: bigger queries
after this arc: you can write the multi step queries real reports need

- [ ] subquery in WHERE ★
- [ ] subquery in FROM
- [ ] scalar subqueries: one value inside a query
- [ ] correlated subqueries: a query that depends on the outer row ★
- [ ] EXISTS and NOT EXISTS: semi joins and anti joins as questions ★
- [ ] NOT IN and the NULL trap ★
- [ ] CTEs: naming each step with WITH ★
- [ ] views: a saved query with a name ★
- [ ] UNION and UNION ALL ★
- [ ] INTERSECT and EXCEPT
- [ ] window functions: a total next to every row ★
- [ ] OVER: the window a function looks through
- [ ] PARTITION BY: a separate window per group ★
- [ ] ROW_NUMBER: numbering rows in order ★
- [ ] RANK vs DENSE_RANK: what ties do ★
- [ ] running totals ★
- [ ] window frames: ROWS BETWEEN ★
- [ ] the default frame trap: why adding ORDER BY turns MAX into a running max ★
- [ ] LAG and LEAD: looking at the row before ★
- [ ] top N per group ★
- [ ] removing duplicates with ROW_NUMBER ★
- [ ] gaps and islands: date minus row number stays constant inside a streak ★
- [ ] gaps and islands: grouping each island into one streak row ★
- [ ] date spines: filling in days with no orders ★
- [ ] sessionizing clicks with LAG and a running sum ★
- [ ] retention cohorts: who came back next month ★
- [ ] recursive CTEs: following a chain of rows
- [ ] arrays and UNNEST: lists inside a cell
- [ ] querying JSON inside a column
- [ ] practice: ten interview style SQL questions on the shop ★
- [ ] capstone: each customers first order and the days between orders

## arc 9: changing data safely
after this arc: you can change data and know exactly what happens when two people do it at once

- [ ] containers: a program packed with everything it needs ★
- [ ] running Postgres in a container on your laptop
- [ ] a database server: Postgres, where most app data lives
- [ ] connections and sessions: one conversation with the database
- [ ] CREATE TABLE
- [ ] temporary tables
- [ ] NOT NULL and DEFAULT: required columns and fallback values ★
- [ ] UNIQUE and CHECK: rules every value must pass ★
- [ ] key constraints the database enforces for you ★
- [ ] where ids come from: sequences and auto increment ★
- [ ] INSERT
- [ ] INSERT from a SELECT
- [ ] UPDATE, and why the WHERE matters so much ★
- [ ] DELETE ★
- [ ] upsert: insert, or update if the row is already there ★
- [ ] ALTER TABLE: adding a column
- [ ] DROP and TRUNCATE
- [ ] transactions: all or nothing ★
- [ ] COMMIT and ROLLBACK
- [ ] ACID: four promises a database makes ★
- [ ] ACID consistency: the rules still hold after every change
- [ ] isolation: two people at the same time ★
- [ ] durability: surviving a crash
- [ ] the write ahead log: write down the plan before the change ★
- [ ] replaying the log after a crash
- [ ] lost updates ★
- [ ] dirty reads ★
- [ ] non repeatable reads ★
- [ ] phantoms ★
- [ ] isolation levels: read committed ★
- [ ] repeatable read: rows dont change under you mid transaction ★
- [ ] serializable: as if one at a time, and retrying the failures ★
- [ ] row locks and table locks
- [ ] SELECT FOR UPDATE: locking on purpose ★
- [ ] deadlocks ★
- [ ] changing a column type on a big table ★
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
