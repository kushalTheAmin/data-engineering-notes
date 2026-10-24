# curriculum

the map from zero to data engineer. one checkbox is one atom: one idea small enough for a 2 minute note. big concepts are already broken into several atoms in the order you need them, and a box still gets split further if it turns out bigger than it looks. arcs run in order, boxes inside an arc run in order, and each arc ends with a capstone that assembles its atoms. a ★ marks a concept that is important or easy to get wrong, so its note ends with check yourself questions. every capstone gets them too.

## THREAD
baton: 198 showed that left joining the 9 generate_series days onto orders (matching on CAST(ordered_at AS DATE)) and grouping by day with count(o.order_id) gives 9 rows where april 2, 5 and 7 read 0, that count(*) would show 1 for those days because the join fills in one row, that a WHERE on an orders column (like status = 'delivered') runs after the join and drops the empty days again leaving 4 rows, and that the average per day is 7 over 9 (about 0.78) on the spine against 7 over 6 (about 1.17) without it. the next box is sessionizing clicks with LAG and a running sum. earlier baton: 197 showed generate_series(start, stop, step) in FROM makes one row per step from start to stop with both ends included, so DATE 2026-04-01 to 2026-04-09 with INTERVAL 1 DAY gives the 9 days (DuckDB returns timestamps so CAST to DATE), step 2 from april 2 gives 2, 4, 6, 8 because the stop is only in if a step lands on it, a start after the stop gives zero rows, range() leaves the stop out, orders has 7 rows over 6 different days so 3 of the 9 days (april 2, 5, 7) have no order, and Postgres has generate_series too. the next box is date spines: left join the 9 generated days to the orders counted per day so the empty days show up with 0. earlier baton: 196 showed that GROUP BY the 195 label (inside a subquery in FROM) with min(day), max(day) and count(*) turns the 6 order days of daily_orders into 4 streak rows (april 1 alone, april 3 to 4, april 6 alone, april 8 to 9), that the label is only scaffolding and not in the output, that a streak of n days has a span of n minus 1, and that grouping by day instead gives 6 rows. the next box is date spines: filling in days with no orders, so the empty days (april 2, 5 and 7) show up as rows with 0. earlier baton: 195 showed that taking only the days with orders (6 of the 9 in daily_orders), numbering them with ROW_NUMBER and subtracting that many days from each date gives a label that stays the same inside a streak (april 3 and 4 share 2026-04-01, april 8 and 9 share 2026-04-03, april 1 and april 6 are alone), that the WHERE runs before the numbering so empty days are not counted, that it needs one row per day, and that DuckDB needs the row number cast to INTEGER before a date minus it. the next box is grouping each island into one streak row: GROUP BY the label and take min(day), max(day) and count(*) per streak, the labels from 195 are the group keys. earlier baton: 194 showed DISTINCT only drops rows that match on every column, so city_feed (Asha twice with Jersey City and Hoboken, Bhavin twice as an exact copy, Disha once) gives 4 rows with DISTINCT and Asha still twice, while row_number() OVER (PARTITION BY customer_id ORDER BY changed_at DESC) with rn = 1 outside keeps 3 rows (Asha Hoboken, Bhavin Edison, Disha Hoboken), rn > 1 shows the 2 dropped rows, the ORDER BY inside OVER picks which copy survives, and identical or tied rows need a second sort column for a promised winner. the next box is gaps and islands, date minus row number stays constant inside a streak. earlier baton: 193 showed you cant filter on a window function in WHERE because windows run after it, so top N per group is number inside and filter outside: SELECT ... FROM (SELECT ..., row_number() OVER (PARTITION BY category ORDER BY price DESC) AS rn FROM products) AS t WHERE rn <= 2 gives 5 rows (masala chai alone in drinks, khandvi and dhokla, kaju katli and jalebi, fafda cut), rn <= 1 gives the priciest per category, and dropping PARTITION BY gives the top 2 overall (kaju katli, khandvi). the next box is removing duplicates with ROW_NUMBER. earlier baton: 192 showed LAG and LEAD hand a value from the row before or after in the ORDER BY order, so lag(placed) OVER (ORDER BY day) on daily_orders is the placed column pushed down one row (NULL on april 1, then 2, 0, 1, 1, 0, 1, 0, 1), lead is pushed up (NULL on april 9), placed - lag(placed) gives the day over day change (-2, 1, 0, -1, 1, -1, 1, 0), lag(placed, 2) reaches two rows back and lag(placed, 1, 0) swaps the edge NULL for 0, before means the row before in the ORDER BY and not the day before, and a WHERE runs first so april 6 looks back at april 4 and shows 1 when only those two days are kept. the next box is top N per group, ROW_NUMBER with PARTITION BY and a filter on the outside. earlier baton: 191 showed that with ORDER BY inside OVER and no frame the frame stops at the current row, so max(cancelled) OVER (ORDER BY day) on daily_orders is a running max (0 until april 4, then 1) where OVER () gives 1 on every row, adding UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING brings the whole window back, and last_value then returns the current rows own value (april 5 shows 0, not april 9's 1). the next box is LAG and LEAD, looking at the row before. earlier baton: 190 showed a window frame is the slice of the window a function adds up, so sum(placed) OVER (ORDER BY day ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) on daily_orders gives 2, 2, 3, 2, 2, 2, 1, 2, 2 (april 6 is april 4, 5, 6 = 1 + 0 + 1) beside the 189 running total, the first rows just have fewer rows to use, avg over the frame on april 1 divides by its 1 row (2.0 not 0.67), ROWS counts rows and not days so a missing day or a WHERE that drops april 5 makes the frame reach further back (april 6 shows 3), and 1 PRECEDING AND 1 FOLLOWING on april 6 gives 0 + 1 + 0 = 1. the next box is the default frame trap, why adding ORDER BY turns MAX into a running max. earlier baton: 189 showed a running total is sum(placed) OVER (ORDER BY day), so daily_orders placed 2, 0, 1, 1, 0, 1, 0, 1, 1 gives 2, 2, 3, 4, 4, 5, 5, 6, 7 where OVER () gives 7 on every row, ORDER BY day DESC counts from the other end (april 1 shows 7, april 9 shows 1), a WHERE on the same level runs first so a one-day filter makes a running total of cancelled 0 where the real one is 1, and repeated ORDER BY values are only flagged as a later note. the next box is window frames, ROWS BETWEEN. earlier baton: 188 showed RANK and DENSE_RANK give tied rows the same number and differ only after the tie, so order_items for orders 102 and 105 ranked by quantity gives the two quantity 2 rows 1 and 1, then RANK gives the three quantity 1 rows 3 (2 rows are ahead, the Postgres docs call it the row_number of the first tied row) where DENSE_RANK gives 2, and for top N rk <= 2 keeps 2 rows while dr <= 2 keeps all 5. the next box is running totals. earlier baton: 187 showed row_number() OVER (ORDER BY price DESC) numbers rows 1, 2, 3 in the order the ORDER BY inside OVER sets, so kaju katli is 1 and dhokla 3 even when rows come out in product_id order, the number is a label and not an output position, tied rows get numbers in an unspecified order (Postgres docs) so add a tiebreaker, and PARTITION BY category restarts the count at 1 per category. the next box is RANK vs DENSE_RANK, what ties do. earlier baton: 186 showed PARTITION BY inside OVER cuts the window into one group per value, so avg(price) OVER (PARTITION BY category) gives snacks 6.00, sweets 8.50 and masala chai, alone in drink, its own 3.00, all 6 rows stay where GROUP BY gives 3, and PARTITION BY name makes every window one row so price minus the average is 0 everywhere. the next box is ROW_NUMBER, numbering rows in order. earlier baton: 185 showed the window is the set of rows a window function looks at for the current row, picture a loop that builds a fresh window for every row, and OVER () makes it every row, so price minus avg(price) OVER () gives dhokla -0.33 and kaju katli 5.67 against the 6.33 average, the average never changes but the price is the current rows own. the next box is PARTITION BY, a separate window per group. earlier baton: 184 showed a window function is an aggregate followed by OVER () that keeps every row and adds the answer beside it, so each of the 6 products shows the 38.00 total of all prices, and it runs after WHERE so a snack-only filter makes the total 18.00 and filtering on a window result needs a subquery in FROM. the next box is OVER, the window a function looks through. earlier baton: 183 showed INTERSECT keeps rows found in both queries and EXCEPT keeps first query rows missing from the second, so delivered customer ids (1, 2, 4) against the rest (1, 3) give 1 for INTERSECT, 2 and 4 for EXCEPT and 3 when the sides swap, both drop repeated rows like UNION, and EXCEPT treats two NULLs as the same so a NULL city is removed where NOT IN would empty the result. the next box is window functions, a total next to every row. earlier baton: 182 showed UNION ALL stacks one query's rows under another's and plain UNION also drops repeated rows, so delivered and not delivered customer ids give 7 rows with UNION ALL and 4 with UNION (Asha's 3 orders collapse to one), both queries need the same number of columns matched by position with names from the first, and Postgres says UNION ALL is usually significantly quicker. the next box is INTERSECT and EXCEPT. earlier baton: 181 showed a view is a query saved under a name that reruns on every read, so a count over delivered_orders went from 5 to 6 when order 106 was updated to delivered without touching the view, and Postgres also has materialized views that store the answer. the next box is UNION and UNION ALL. earlier baton: 180 showed a CTE is an inner query named up front with WITH, so 175's per-customer order counts become per_customer and the main query reads it top to bottom, and the name can be used twice (as a table and inside an average, giving Asha and Bhavin above the 1.75 average), only lasts for one statement, and a name that matches a real table (orders) wins over it. the next box is views, a saved query with a name. earlier baton: 179 showed NOT IN returns nothing at all once the inner list holds a NULL (customers outside every zone but south gives zero rows where Bhavin was expected), because every not-equal test against NULL is unknown and an AND chain can then never be true, while NOT EXISTS gives Bhavin and Esha. the next box is CTEs, naming each step with WITH. earlier baton: 178 showed EXISTS is true when a correlated inner query returns at least one row and NOT EXISTS flips it, so delivered orders keep Asha, Bhavin and Disha once each (a join gives 5 rows) and NOT EXISTS gives Chirag (only a cancelled order) and Esha, and what the inner SELECT lists never matters. the next box is NOT IN and the NULL trap. earlier baton: 177 showed a correlated subquery is a scalar subquery that uses a column of the outer row through a table alias, so it is asked again per row, and price < the average of the products own category (p.category) keeps fafda and jalebi where the shop wide average keeps 4, and dropping the p. makes category = category compare the inner table to itself and silently gives the shop wide average back. the next box is EXISTS and NOT EXISTS, asking whether a matching row exists. earlier baton: 176 showed a scalar subquery is a subquery returning exactly one row and one column, used as a plain value, so price > (SELECT avg(price) FROM products) keeps khandvi and kaju katli (average 6.33), two rows from the inner query is an error, and zero rows gives NULL so the outer query silently returns nothing. the next box is correlated subqueries, an inner query that depends on the outer row. earlier baton: 175 showed a subquery in FROM is an inner SELECT in parentheses with a table alias that the outer query reads as a table, so avg over per-customer order counts (3, 2, 1, 1) gives 1.75 where avg(count(*)) errors, and Esha has no group so she is not in it. the next box is scalar subqueries, an inner query that returns one value. earlier baton: 174 opened the bigger queries section: a subquery in WHERE is an inner SELECT in parentheses that you picture running first and hands IN a list, delivered customer ids 1, 2, 1, 4, 2 keep Asha, Bhavin and Disha once each (a join gives 5 rows), and an inner column that means something else (order_id) returns zero rows with no error. the next box is subquery in FROM, the inner query as a table the outer query reads
last visuals: query and result plus two hidden query and result answers (date spines), query and result plus python block plus two hidden query and result answers (generate_series), text before and after table plus a query and result plus two hidden query and result answers (gaps and islands, one row per streak), python block plus a query and result plus two hidden query and result answers (gaps and islands), query and result plus two hidden query answers (removing duplicates with ROW_NUMBER)
last exits: stops (date spines), forward (generate_series), stops (gaps and islands, one row per streak), stops (gaps and islands), stops (removing duplicates with ROW_NUMBER)
last reactions: i expected the empty days to need a patch afterwards, but the spine just refuses to lose them, i figured every row had to come from a table somewhere, and this one comes out of three values i typed, i found it odd to build a column just to throw it away, i kept looking for a comparison between neighbors, and there isnt one, i hadnt thought of the sort inside OVER as a choice about which copy survives, i assumed top N needed its own feature but its just two ideas stacked, i half expected an error or a 0 at the edge of the table and it quietly gives NULL, i assumed the sorting only decided the order, but here it also shrinks what the function can see, i expected the frame to count days, but it counts rows, i assumed the sorting inside OVER was only for show, but it decides what before means

## NOTES
log of runs that failed the gate, newest last. format: YYYY-MM-DD: concept failed check: one line on why
2026-10-22: repo baseline failed checks/127.py: date_trunc on ordered_at returns datetime.date in duckdb 1.1 to 1.4.5 (the check expects datetime, with 1.2 and 1.1 also failing 114), so the gate fails before any change; needs a fix outside this run
2026-10-23: repo baseline failed checks/127.py again: same date_trunc type assert, no duckdb from 1.0 to 1.4.5 passes the whole gate, still needs a fix outside this run; mermaid render also failed so no diagrams today
2026-10-23: repo baseline failed checks/127.py: same date_trunc type assert on duckdb 1.4.5 (duckdb 2.0.0 also breaks 8 checks on fetchone), mermaid render failed again; no note written, needs a fix outside this run
2026-10-23: repo baseline failed checks/127.py again: same date_trunc type assert on duckdb 1.4.5 (python3 here is 3.11, duckdb 2.0.0 is only installed for 3.13), no note written, needs a fix outside this run
2026-10-23: repo baseline failed gate setup: python3 here is 3.11 with no duckdb (duckdb 2.0.0 sits only under 3.13 and breaks 8 checks on fetchone, a duckdb 1.4.5 install timed out), mermaid render failed again; no note written, needs a fix outside this run
2026-10-23: repo baseline failed checks/127.py: same date_trunc type assert on duckdb 1.4.5 (installed via python3 -m pip), no note written, needs a fix outside this run
2026-10-23: repo baseline failed checks/127.py: same date_trunc type assert on duckdb 1.4.5 (duckdb 2.0.0 breaks 8 checks on fetchone), mermaid render failed again; no note written, needs a fix outside this run
2026-10-24: repo baseline failed checks/008.py and 7 more: pip gives duckdb 2.0.0 for python3 (3.11) and it breaks 8 checks on fetchone (041 also asserts), mermaid render failed again; no note written, needs a fix outside this run
2026-10-24: repo baseline failed checks/008.py and 7 more: pip only gives duckdb 2.0.0 (python3.13) and it breaks 8 checks on fetchone (041 also asserts), no note written, needs a fix outside this run
2026-10-24: repo baseline failed checks/127.py: same date_trunc type assert on duckdb 1.4.5 (pip default is 2.0.0 which breaks 8 checks), mermaid render failed again; no note written, needs a fix outside this run
2026-10-24: repo baseline failed checks/008.py and 7 more: only duckdb 2.0.0 is installed (for python 3.13) and it breaks 8 checks on fetchone (041 also asserts), mermaid render failed again; no note written, needs a fix outside this run
2026-10-24: repo baseline failed checks/011.py and 7 more: python3 is 3.11 with no duckdb, only duckdb 2.0.0 under python3.13 and it breaks 8 checks on fetchone (041 also asserts), no note written, needs a fix outside this run

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
- [ ] session starts: LAG the time gap and flag the click that opens a new session ★
- [ ] session ids: a running sum of the flags numbers each session ★
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
