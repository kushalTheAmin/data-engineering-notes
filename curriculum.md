# curriculum

the map from zero to data engineer. one checkbox is one atom: one idea small enough for a 2 minute note. big concepts are already broken into several atoms in the order you need them, and a box still gets split further if it turns out bigger than it looks. arcs run in order, boxes inside an arc run in order, and each arc ends with a capstone that assembles its atoms. a ★ marks a concept that is important or easy to get wrong, so its note ends with check yourself questions. every capstone gets them too.

## THREAD
baton: 280 drew the order ids 101 to 107 as a tree (root 104, 2 children per node, leaves 101 103 105 107), finding 107 follows one path of 3 looks and drops a whole side each step, matching the middles of the halving in 273, and the tree is tidy only because the ids were picked in a good order. the next box asks what happens to the depth when ids arrive in order, 101, 102, 103, and why it can be kept small.
last visuals: mermaid tree of the 7 order ids plus a text walk for 107 (trees), python block with its output of chained slots and four lookups plus two hidden answers (collisions), python block with its output of the 8 slots filled and three lookups plus two hidden answers (hash tables), worked trace by hand of dhokla into 8 slots plus a tiny comparison table of the six products and three hidden answers (hash functions), two tiny comparison tables, a 6 product rounds trace and a growth table of one pass vs sorting vs loop inside a loop (why sorting costs more), python block with its output of merge sort rounds on 6 prices plus two hidden answers (merge sort), python block with its output of merging two sorted price lists plus two hidden answers (merging), worked trace by hand of halving for order 107 plus a tiny comparison table of hunt vs halving and two hidden answers (binary search), python block with its output of orders against 6 products vs orders against orders plus two hidden answers (a loop inside a loop), python block with its output of straight line vs curving up looks at 7, 70 and 700 orders plus two hidden answers (curving up), python block with its output of jump vs hunt at 7, 70, 700 and 7000 orders plus three hidden answers (flat and straight line), python block with its output of find steps at 7, 70, 700 and 7000 orders plus two hidden answers (big O), decision table with a CREATE TABLE and a query and result plus two hidden answers (capstone, product reviews), query and result with CREATE SCHEMA and a bare name versus full names, plus a USE query and result (schemas as namespaces), tiny comparison table of hard delete vs soft delete plus query and result of live vs all counts and two hidden answers (soft deletes), query and result of order_tracking timestamps plus a text UPDATE line and two hidden answers (created_at and updated_at), tiny comparison table of messy vs clean names plus query and result of a guessed join (naming conventions)
last exits: forward (trees), stops (collisions), forward (hash tables), forward (hash functions), stops (why sorting costs more), forward (merge sort), stops (merging), stops (binary search), forward (a loop inside a loop), stops (curving up), forward (flat and straight line), stops (big O), forward (capstone, product reviews), stops (schemas as namespaces), stops (soft deletes), stops (created_at and updated_at)
last reactions: i assumed a tree was some fancy structure, but its the halving i knew with the middles drawn as boxes, i assumed a collision was an error the table had to avoid, but its normal and the table is built to expect it, i assumed a miss would be the slow case, like in a list, but here it costs the same as a hit, i expected a hash function to be some scary scrambling, but this one is addition and a remainder, i assumed sorting was either cheap or expensive, but it sits in between and rounds only grow by one each time the data doubles, i expected sorting to need a brand new trick, but it is the same merge run again and again starting from lists too small to be wrong, i expected combining two lists to need a nested loop, but the sorted order is what lets one pass do it, i assumed throwing half away was a gamble, but the sort order is what makes it safe, i assumed any loop inside a loop was the slow shape, but it only curves when both lists grow, i assumed slow code was just more of the same, but 49 looks turning into 490000 feels like a different program, i expected the flat shape to need some clever trick, but it is just knowing where to jump, i expected the interesting number to be how fast one lookup is, but the useful one is what happens to the steps when the data gets 10 times bigger, i figured a design this size would be a pile of fresh decisions, but most columns were already decided by the notes above and the key was the one i had to think about, i assumed a table name was just the name of the table, but its only a name inside a folder, i expected a delete to be its own kind of thing, but this one is an UPDATE and the row carries on like any other, i assumed updated_at worked like a files modified time, kept by the system, but nothing moves it unless somebody writes to it, i figured naming was taste, but a name is a promise about what you will find, i assumed a column full of digits was a number column, but the test is whether adding two of them means anything, i assumed breaking the rules meant sloppy design, but the careful version is knowing which copy is the true one, i expected the one column key to protect it like in 260, but the leak runs sideways through customer_id, i assumed a rule this strict would bite everywhere, but a one column key passes for free, i figured a list cell was harmless since it holds the data fine, but it cant refuse anything, i assumed about the key was a vague feeling, but its a lookup that must never have two answers, i heard third normal form as a grade like B+, but its a checklist you can run by hand one cell at a time, i read one to one as a perfect pairing, but 2 of 5 customers have nobody on the other side, i assumed entity or attribute was a fixed label on the thing, but its decided by whether you want facts about it, i figured design started with picking column types, but its one question asked again and again, i used to think the transaction was the safety, but it only makes a group all or nothing, i assumed the log was scrap thrown away after a crash, but here its the thing you keep, i assumed restore meant undoing the mistake, but it only takes you back to the copy, i assumed a bigger id meant newer, but a snapshot is a list of whos done and not a timeline, i assumed UPDATE was a dictionary overwrite, but its appending a new dictionary and crossing out the old one, i kept waiting for the expensive step, and the swap is just two labels trading places, i found it odd that the order of two steps matters more than either step, i expected the safe way to be one careful command, but its lots of small ones, i assumed widening a number would be free like a bigger box, but the size is fixed per column so every row is stored again, i assumed the server would just hang until someone restarted it, but Postgres goes looking for the circle on its own, i expected Esha to get the row back and see delivered, but she gets nothing because the WHERE is rechecked, i assumed a lock meant nobody could look, but row locks block only writers, i figured strict meant waiting in line, but it lets both run and sends one back at the door, i expected stale data to be the bug, but here being out of date on purpose is the feature, i guessed BEGIN was the moment Asha gets her view, but the picture is taken per query, and i found it comforting that the surprise only lives between queries never inside one

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
2026-10-30: repo baseline failed gate setup: pip gives duckdb 2.0.0 which breaks 8 checks on fetchone, checks/041.py and 268.py also assert, no note written, needs a fix outside this run
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
2026-10-28: repo baseline failed gate setup: python3 here is 3.11 with no duckdb (pip installs duckdb 2.0.0 for 3.13 only, which breaks 8 checks on fetchone), mermaid render failed again; no note written, needs a fix outside this run
2026-10-29: repo baseline failed checks/008.py and 7 more: pip gives duckdb 2.0.0 which breaks 8 checks on fetchone (041 also asserts), mermaid render failed again; no note written, needs a fix outside this run
2026-10-29: repo baseline failed checks/008.py and 7 more: python3 is 3.11 and pip gives duckdb 2.0.0, which breaks 8 checks on fetchone (041 also asserts); no note written, needs a fix outside this run
2026-10-29: repo baseline failed checks/127.py, 201.py, 202.py: date_trunc type asserts on duckdb 1.4.5 (python3 is 3.11, plain pip gives duckdb 2.0.0 which breaks 8 checks on fetchone); no note written, needs a fix outside this run
2026-10-30: repo baseline failed checks/011.py and 7 more: pip gives duckdb 2.0.0 for python 3.11 (fetchone on relations removed, 041 asserts); no note written, needs a fix outside this run
2026-10-30: repo baseline failed checks/127.py, 201.py, 202.py: date_trunc on a DATE returns DATE not TIMESTAMP on duckdb 1.4.1 and 1.4.5, and 1.3.2 and 1.2.2 fail other checks (180, 197), duckdb 2.0.0 breaks 8 on fetchone; mermaid render also failed; no note written, needs a fix outside this run
2026-10-30: repo baseline failed checks/127.py, 201.py, 202.py: date_trunc on a DATE returns DATE not TIMESTAMP on duckdb 1.4.5 (python3 is 3.11, mermaid render also failed); no note written, needs a fix outside this run
2026-10-30: repo baseline failed checks/008.py and 8 more: pip gives duckdb 2.0.0 for python 3.11 (fetchone on relations removed, 041 and 268 assert), mermaid render failed (chromium needs no-sandbox as root); no note written, needs a fix outside this run
2026-10-30: repo baseline failed checks/008.py and 8 more: pip gives duckdb 2.0.0 (fetchone on relations removed, 041 and 268 assert), mermaid render failed (chromium needs no-sandbox as root); no note written, needs a fix outside this run
2026-10-30: repo baseline failed gate setup: python3 is 3.11 with no duckdb, python3 -m pip gives duckdb 2.0.0 which breaks 8 checks on fetchone (041 and 268 also assert); no note written, needs a fix outside this run
2026-10-30: repo baseline failed checks/008.py and 8 more: duckdb 2.0.0 (the only one installed) removed fetchone on relations and 041 and 268 assert, mermaid render failed (chromium needs no-sandbox as root); no note written, needs a fix outside this run
2026-10-30: repo baseline failed checks/127.py, 201.py, 202.py: date_trunc type asserts on duckdb 1.4.2 (python3 is 3.11, plain pip hangs building duckdb from source, only a pinned wheel installs); no note written, needs a fix outside this run
2026-10-31: repo baseline failed checks/127.py, 201.py, 202.py: date_trunc on a DATE returns DATE not TIMESTAMP on duckdb 1.4.5 (python3 is 3.11, pinned wheel installs fine, mermaid render ok); no note written, needs a fix outside this run
2026-10-31: repo baseline failed checks/008.py and 8 more: only duckdb 2.0.0 is available (under /usr/bin/python3, python3 on PATH is 3.11 with none), fetchone on relations removed and 041 and 268 assert; no note written, needs a fix outside this run

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
- [x] changing a column type without downtime: add a new column and backfill it in batches ★ (note 246)
- [x] changing a column type without downtime: keeping the new column in sync with new writes ★ (note 247)
- [x] changing a column type without downtime: the swap, renaming in one short transaction ★ (note 248)
- [x] MVCC: every row keeps versions ★ (note 249)
- [x] transaction snapshots: what your transaction is allowed to see ★ (note 250)
- [x] backups: a copy you can restore from (note 251)
- [x] point in time recovery: a backup plus the replayed log (note 252)
- [x] capstone: placing an order as one transaction (note 253)

## arc 10: designing tables
after this arc: you can design the tables for a new feature and defend every choice

- [x] modeling: deciding the tables before writing them (note 254)
- [x] entities and attributes (note 255)
- [x] one to one: when two tables share a key (note 256)
- [x] normal forms: the rules behind splitting tables ★ (note 257)
- [x] functional dependency: when one column decides another ★ (note 258)
- [x] first normal form: one value per cell ★ (note 259)
- [x] second normal form ★ (note 260)
- [x] third normal form ★ (note 261)
- [x] denormalization: copying data on purpose ★ (note 262)
- [x] choosing column types well ★ (note 263)
- [x] naming conventions (note 264)
- [x] created_at and updated_at ★ (note 265)
- [x] soft deletes: marking a row gone instead of removing it ★ (note 266)
- [x] schemas as namespaces: folders for tables (note 267)
- [x] capstone: modeling product reviews for the shop (note 268)

## arc 11: tricks that make data fast
after this arc: you know the handful of ideas every database, index and big data tool is built on

- [x] big O in plain words: how work grows as data grows ★ (note 269)
- [x] flat and straight line: the two shapes of growth ★ (note 270)
- [x] curving up: when 10 times the data means 100 times the steps ★ (note 271)
- [x] a loop inside a loop: why some code gets slow so fast ★ (note 272)
- [x] binary search: finding one item in sorted data by halving ★ (note 273)
- [x] merging two sorted lists into one ★ (note 274)
- [x] merge sort: split down to single items, then merge back up ★ (note 275)
- [x] why sorting costs more than one pass over the data (note 276)
- [x] hash functions: turning anything into a number in a fixed range ★ (note 277)
- [x] hash tables: how a dictionary finds a key without searching ★ (note 278)
- [x] collisions: when two keys land in the same spot (note 279)
- [x] trees: data that branches (note 280)
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
2026-10-29: repo baseline failed gate setup: duckdb 2.0.0 (3.13) breaks 8 checks on fetchone and plain python3 here is 3.11 without it, duckdb 1.1.3 and 1.4.5 also fail 041 and note 180, mermaid render failed again; no note written, needs a fix outside this run
2026-10-29: repo baseline failed checks/127.py, 201.py, 202.py: date_trunc type asserts on duckdb 1.4.5 (/usr/bin/python3; pip default 2.0.0 breaks 8 checks on fetchone), mermaid render failed (chromium needs --no-sandbox as root); no note written, needs a fix outside this run
2026-10-29: repo baseline failed gate setup: duckdb 2.0.0 breaks 8 checks on fetchone, 1.5.6 and 1.1.3 still fail 041 and some fetchone checks, note 180 fails on 1.1.3, plain python3 is 3.11 without duckdb, mermaid render hangs; no note written, needs a fix outside this run
2026-10-30: repo baseline failed gate setup: no duckdb version passes (2.0.0 breaks 8 checks on fetchone, 1.2.2 and 1.3.2 fail 127/180/201/202 and 197, 1.4.5 fails 127/201/202 and 041/268), same as the last 3 days; no note written, needs a fix outside this run
2026-10-30: repo baseline failed checks/008.py and 8 more: pip gives duckdb 2.0.0 for python 3.11 (fetchone on relations removed, 041 and 268 assert); no note written, needs a fix outside this run
2026-10-30: repo baseline failed checks/127.py, 201.py, 202.py: no duckdb version passes (1.1.3 fails 11 checks, 1.3.0 fails 180 too, 1.4.5 fails these 3, 2.0.0 breaks 8 on fetchone); no note written, needs a fix outside this run
2026-10-31: repo baseline failed checks/127.py, 201.py, 202.py: duckdb 1.4.5 is the best version available (2.0.0 breaks 8 checks on fetchone, 1.4.5 fails these 3 on date_trunc type asserts); no note written, needs a fix outside this run
2026-10-31: repo baseline failed checks/127.py, 201.py, 202.py: date_trunc on a DATE asserts on duckdb 1.4.5 (python3 is 3.11, pip default 2.0.0 breaks 8 checks on fetchone, 041 and 268 assert), mermaid render ok; no note written, needs a fix outside this run
