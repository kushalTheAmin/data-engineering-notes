# glossary

every term these notes have built, in plain words, with the note that built it. if a note uses a term, its in here first.

| term | plain meaning | built in |
|---|---|---|
| 401 | status code meaning the request lacks valid credentials, caller unknown | [314](./notes/314-api-keys-a-password-for-programs.md) |
| absolute path | a path starting with a slash, always begun at the root | [053](./notes/053-absolute-vs-relative-paths.md) |
| ACCESS EXCLUSIVE | the strongest table lock, blocks every other query on the table | [245](./notes/245-changing-a-column-type-the-table-rewrite-and-the-lock.md) |
| access token | short lived string a program sends instead of a key | [315](./notes/315-tokens-that-expire-a-key-with-a-shelf-life.md) |
| ACID | four promises of a database: atomicity, consistency, isolation, durability | [229](./notes/229-acid-four-promises-a-database-makes.md) |
| add column | a new column added to a table that already has rows | [225](./notes/225-alter-table-adding-a-column-to-a-table-with-rows.md) |
| address (network) | a number naming one machine on a network, 4 bytes in IPv4 | [085](./notes/085-addresses-and-ports.md) |
| aggregate function | reads many rows, returns one value, like count, sum or max | [137](./notes/137-aggregate-functions-many-rows-in-one-value-out.md) |
| aggregates skip nulls | sum, avg and count(column) ignore null rows entirely | [141](./notes/141-what-nulls-do-to-sum-and-avg.md) |
| alias | a name you give a result column with AS | [122](./notes/122-computed-columns-and-as.md) |
| ambiguous time | a clock reading that happens twice, when clocks go back | [029](./notes/029-daylight-saving.md) |
| ANALYZE | Postgres command that samples a table and saves its statistics | [297](./notes/297-statistics-how-the-planner-guesses-row-counts.md) |
| AND | joins two tests, keeping a row only if both are true | [108](./notes/108-and-or-combining-two-tests.md) |
| anti join | keeps left rows with no match: a left join, then IS NULL | [167](./notes/167-anti-join-rows-with-no-match.md) |
| API | the requests a server promises to answer for other programs | [312](./notes/312-apis-a-door-built-for-programs.md) |
| API key | secret string a program sends so the API knows who asks | [314](./notes/314-api-keys-a-password-for-programs.md) |
| argument | a word after the program name, handed to that program | [049](./notes/049-the-terminal.md) |
| array (SQL) | several values kept in one cell, written in square brackets | [204](./notes/204-arrays-and-unnest-lists-inside-a-cell.md) |
| ASCII | the old table giving 128 characters a number, English only | [008](./notes/008-ascii-runs-out.md) |
| asymmetric encryption | two different keys: one locks, only the other unlocks | [318](./notes/318-public-and-private-keys-locking-without-sharing-a-secret.md) |
| atomic | happening whole or not at all, never half done | [046](./notes/046-writing-safely.md) |
| atomicity | the ACID promise: all of a transaction happens, or none of it | [229](./notes/229-acid-four-promises-a-database-makes.md) |
| attribute (data model) | one fact about one entity, stored as a column | [255](./notes/255-entities-and-attributes.md) |
| attribute (python) | a value stored on an object, like o105.status | [336](./notes/336-classes-in-one-picture-data-and-functions-together.md) |
| authorization code flow | OAuth steps: login at the shop, one time code, swap for token | [316](./notes/316-oauth-in-one-picture-a-token-without-the-password.md) |
| autovacuum | background Postgres job that runs VACUUM and ANALYZE for you | [304](./notes/304-vacuum-how-postgres-cleans-up-old-row-versions.md) |
| avg | the average of a column, its sum divided by how many values | [140](./notes/140-sum-and-avg-adding-up-and-averaging.md) |
| B tree | a tree whose nodes are whole pages, each holding many sorted values | [287](./notes/287-b-tree-pages-that-point-to-pages.md) |
| backfill | fills a new column for rows that already exist, in small batches | [246](./notes/246-add-a-new-column-and-backfill-it-in-batches.md) |
| backup | a copy of your data, kept elsewhere, that you can restore from | [251](./notes/251-backups-a-copy-you-can-restore-from.md) |
| balanced tree | a tree that keeps its depth as small as its size allows | [281](./notes/281-balanced-trees-why-the-depth-stays-small.md) |
| bandwidth | how many bytes a connection moves per second | [323](./notes/323-latency-and-bandwidth-slow-vs-narrow.md) |
| bare column | the column alone in a WHERE, with no function around it | [295](./notes/295-functions-on-a-column-why-the-index-gets-skipped.md) |
| batch | a small slice of rows handled by one statement | [246](./notes/246-add-a-new-column-and-backfill-it-in-batches.md) |
| BEGIN | the command that opens a transaction | [228](./notes/228-commit-and-rollback-keeping-or-undoing-a-transaction.md) |
| BETWEEN | a test keeping values from a low to a high end, inclusive | [112](./notes/112-between-ranges-that-include-both-ends.md) |
| big O | how a codes step count grows as the data grows | [269](./notes/269-big-o-in-plain-words-how-work-grows-as-data-grows.md) |
| binary | counting with only 0 and 1, each place worth double | [003](./notes/003-counting-in-binary.md) |
| binary file | a file whose bytes are not characters, like packed numbers | [041](./notes/041-text-files-vs-binary-files.md) |
| binary fraction | binary carried past the point, places worth a half, quarter, eighth | [017](./notes/017-fractions-in-binary.md) |
| binary point | the dot in a binary number, places to its right halve | [017](./notes/017-fractions-in-binary.md) |
| binary search | on sorted data, look at the middle and drop the wrong half | [273](./notes/273-binary-search-finding-one-item-in-sorted-data-by-halving.md) |
| bit | one tiny switch inside a computer, written as 0 or 1 | [002](./notes/002-bits.md) |
| block | a fixed chunk of bytes, often 4096, a disk reads at once | [044](./notes/044-disks-read-in-blocks.md) |
| boolean | a value with only two states, true or false | [023](./notes/023-true-and-false-the-boolean.md) |
| branch (git) | a name pointing at one commit, moved forward by new commits | [330](./notes/330-git-branches-trying-something-without-breaking-main.md) |
| buffer hit | a page found already in memory, so no disk trip | [303](./notes/303-the-buffer-pool-keeping-hot-pages-in-memory.md) |
| buffer pool | memory where Postgres keeps copies of pages it already read | [303](./notes/303-the-buffer-pool-keeping-hot-pages-in-memory.md) |
| build (hash join) | loading the inner side into a hash table, once | [299](./notes/299-hash-join-build-a-hash-table-then-look-up-each-row.md) |
| byte | a group of 8 bits, holding 256 possible values | [004](./notes/004-bytes.md) |
| byte in hex | a byte is always exactly two hex digits, 00 to ff | [006](./notes/006-one-byte-two-hex-digits.md) |
| carriage return | the 0d character, which sent a typewriter carriage back | [042](./notes/042-line-endings.md) |
| CASE WHEN | an if, elif, else per row, the first true test wins | [123](./notes/123-case-when-if-and-else-inside-a-query.md) |
| CAST | converts a value to another type, written CAST(x AS type) | [132](./notes/132-cast-changing-a-values-type.md) |
| certificate | a signed document: this public key belongs to this name | [321](./notes/321-certificates-proving-whose-public-key-it-is.md) |
| certificate authority | a trusted organization that signs certificates, a CA | [321](./notes/321-certificates-proving-whose-public-key-it-is.md) |
| chaining | each slot holds a small list, so shared slots still fit | [279](./notes/279-collisions-when-two-keys-land-in-the-same-spot.md) |
| character | one letter, digit, space or symbol, stored as one number | [007](./notes/007-text-is-numbers.md) |
| CHECK | a column rule: refuse any row where its test is false | [217](./notes/217-check-a-rule-every-value-must-pass.md) |
| class | a blueprint bundling data with the functions that use it | [336](./notes/336-classes-in-one-picture-data-and-functions-together.md) |
| client | a program that sends a request and waits for the answer | [086](./notes/086-client-and-server.md) |
| clone (git) | copies a whole remote repository to your machine, with its history | [331](./notes/331-pushing-and-pulling-sharing-code-through-a-remote.md) |
| closure | a function that keeps the outer variables it was built with | [338](./notes/338-returning-a-function-building-a-function-inside-a-function.md) |
| COALESCE | returns the first value in its list that is not null | [116](./notes/116-coalesce-a-fallback-when-a-value-is-null.md) |
| code point | the number Unicode gives one character, written like U+0AA2 | [009](./notes/009-unicode.md) |
| cohort | customers who first showed up in the same month | [201](./notes/201-cohorts-the-month-each-customer-first-showed-up.md) |
| collision | two different keys getting the same slot | [279](./notes/279-collisions-when-two-keys-land-in-the-same-spot.md) |
| column | a fixed position in every row, like position 3 for status | [062](./notes/062-csv-rows-and-columns-separated-by-commas.md) |
| column type | one data type chosen for a whole column, every value fits it | [080](./notes/080-every-column-holds-one-type.md) |
| combining mark | a code point with no letter, drawn on the letter before it | [012](./notes/012-combining-marks.md) |
| COMMIT | ends a transaction and keeps every change made inside it | [228](./notes/228-commit-and-rollback-keeping-or-undoing-a-transaction.md) |
| commit (git) | one saved snapshot of the project, with a message and an id | [329](./notes/329-git-commits-as-snapshots-of-your-code.md) |
| comparison | a column, a test like >= and a value, true or false | [107](./notes/107-comparisons-equal-not-equal-bigger-smaller.md) |
| composite index | an index sorted by one column, then a second inside ties | [290](./notes/290-composite-indexes-sorted-by-the-first-column-then-the-second.md) |
| composite key | a primary key of two columns, only the pair is unique | [095](./notes/095-composite-keys.md) |
| compression | storing the same information in fewer bytes, rebuildable exactly | [047](./notes/047-compression-spotting-repeats.md) |
| computed column | an expression in SELECT, worked out fresh for each row | [122](./notes/122-computed-columns-and-as.md) |
| concatenate | glue two pieces of text into one, written with two bars | [125](./notes/125-concatenating-text-and-taking-pieces-of-it.md) |
| conditional aggregation | a CASE inside an aggregate, so each row counts toward chosen totals | [148](./notes/148-conditional-aggregation-counting-several-things-in-one-pass.md) |
| conflict markers | the <<<<<<<, ======= and >>>>>>> lines git writes into a conflicted file | [332](./notes/332-merge-conflicts-when-git-cant-combine-two-edits.md) |
| connection | an open line from your program to a database | [102](./notes/102-a-database-in-one-file.md) |
| consistency (ACID) | the ACID promise: declared rules still hold after every change | [229](./notes/229-acid-four-promises-a-database-makes.md) |
| container | a program running in a walled-off box with all it needs | [208](./notes/208-containers-a-program-packed-with-everything-it-needs.md) |
| Content-Type | header naming the format of the body, like application/json | [313](./notes/313-json-over-http-the-answer-is-text-until-you-parse-it.md) |
| continuation byte | a UTF-8 byte starting 10, continuing the previous characters bytes | [011](./notes/011-why-gujarati-takes-3-bytes.md) |
| core | one full processor inside a chip, most chips hold several | [035](./notes/035-the-processor.md) |
| correlated subquery | a scalar subquery that uses the outer row, asked again per row | [177](./notes/177-correlated-subqueries-a-query-that-depends-on-the-outer-row.md) |
| cost (planner) | a made up score Postgres gives each plan, lower wins | [296](./notes/296-the-query-planner-picking-the-cheapest-plan.md) |
| count(*) | counts every row, nulls or not | [138](./notes/138-count-star-vs-count-of-a-column.md) |
| count(column) | counts the rows where that column is not null | [138](./notes/138-count-star-vs-count-of-a-column.md) |
| count(DISTINCT column) | counts how many different non-null values a column has | [139](./notes/139-count-distinct-counting-different-values.md) |
| covering index | an index holding every column a query needs, so no table trips | [292](./notes/292-covering-index-when-the-index-alone-has-the-answer.md) |
| crash | anything that wipes memory, like a power cut or the server dying | [232](./notes/232-durability-surviving-a-crash.md) |
| CREATE TABLE | makes a new empty table from a name and typed columns | [213](./notes/213-create-table-naming-a-table-and-its-columns.md) |
| CREATE TABLE IF NOT EXISTS | skips if the name is taken, never checking the columns match | [213](./notes/213-create-table-naming-a-table-and-its-columns.md) |
| created_at | a column holding when the row was inserted, set once, never changed | [265](./notes/265-created-at-and-updated-at-two-timestamps-every-table-carries.md) |
| CRLF | a line ending of two characters, 0d then 0a, common on windows | [042](./notes/042-line-endings.md) |
| cross join | a join with no test, pairing every row with every row | [169](./notes/169-cross-join-every-row-with-every-row.md) |
| crows feet | line end marks on an ERD showing how many rows match | [099](./notes/099-crows-feet-reading-one-and-many.md) |
| cryptographic hash | a hash with a fixed-size output, no undoing, any change scrambles it | [319](./notes/319-cryptographic-hashes-a-fingerprint-you-cant-reverse.md) |
| CSV | a text file, usually one row per line, values split by commas | [062](./notes/062-csv-rows-and-columns-separated-by-commas.md) |
| csv reader | walks a csv file forward, handing out one row per step | [340](./notes/340-reading-a-csv-in-python-row-by-row.md) |
| CTE | a named inner query written first with WITH, alive for one statement | [180](./notes/180-ctes-naming-each-step-with-with.md) |
| ctid | a rows address in Postgres: page number, then slot | [284](./notes/284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md) |
| curving up (growth) | 10 times the data costs 100 times the steps | [271](./notes/271-curving-up-when-10-times-the-data-means-100-times-the-steps.md) |
| data | facts written down so you can ask questions about them later | [001](./notes/001-data-is-facts-and-numbers.md) |
| data type | the kind of value a field allows, like text or number | [076](./notes/076-data-types-in-a-schema.md) |
| database | a program that owns the data files, changing them only on request | [082](./notes/082-a-database-guards-the-data.md) |
| database server | a database that runs as its own program and answers clients | [211](./notes/211-a-database-server-postgres-where-most-app-data-lives.md) |
| dataframe | a table held in memory: rows, named columns, one type per column | [345](./notes/345-a-dataframe-a-table-in-memory.md) |
| date | a calendar day with no time of day | [027](./notes/027-dates-and-times-apart.md) |
| date part | one piece of a date, like its year, as a number | [126](./notes/126-date-parts-pulling-out-the-year-month-and-day.md) |
| date spine | every day you want as rows, with the data left joined on | [198](./notes/198-date-spines-a-left-join-that-keeps-the-empty-days.md) |
| date_diff | counts the day or month boundaries crossed between two moments | [129](./notes/129-the-difference-between-two-dates.md) |
| date_trunc | chops a timestamp down to the start of its day or month | [127](./notes/127-truncating-timestamps-to-a-day-or-a-month.md) |
| daylight saving | clocks shifting an hour twice a year in many places | [024](./notes/024-utc.md) |
| dead row version | an ended version no open snapshot can still need | [304](./notes/304-vacuum-how-postgres-cleans-up-old-row-versions.md) |
| deadlock | two transactions each waiting for a lock the other holds | [244](./notes/244-deadlocks-two-transactions-waiting-on-each-other.md) |
| decompress | rebuild the original bytes from compressed ones, costing processor work | [048](./notes/048-compression-trades-processor-for-space.md) |
| decorator | a function that takes a function and returns a new one | [339](./notes/339-decorators-the-at-shorthand-for-wrapping-a-function.md) |
| deduplicate | keep one row per thing when the data holds several | [194](./notes/194-removing-duplicates-with-row-number.md) |
| DEFAULT | the value filled in when an insert leaves that column out | [215](./notes/215-not-null-and-default-required-columns-and-fallback-values.md) |
| default frame | with ORDER BY in OVER, the first row through this one | [191](./notes/191-the-default-frame-trap.md) |
| DELETE | removes the rows that match its WHERE, whole rows at once | [223](./notes/223-delete-removing-rows-and-what-still-points-at-them.md) |
| delete anomaly | removing one fact also removes another that lived only in that row | [090](./notes/090-insert-and-delete-anomalies.md) |
| DELETE without WHERE | removes every row in the table, leaving it empty | [223](./notes/223-delete-removing-rows-and-what-still-points-at-them.md) |
| denormalization | copying a fact on purpose so reads skip a lookup | [262](./notes/262-denormalization-copying-data-on-purpose.md) |
| DENSE_RANK | like RANK, but the row after a tie gets the next number | [188](./notes/188-rank-vs-dense-rank-what-ties-do.md) |
| depth | the number of levels in a tree, from the root down | [281](./notes/281-balanced-trees-why-the-depth-stays-small.md) |
| DESC | sort direction: biggest first, instead of the default smallest first | [117](./notes/117-order-by-sorting-by-one-or-more-columns.md) |
| dialect | one databases own version of SQL, with its own spellings and rules | [135](./notes/135-one-language-many-dialects.md) |
| DictReader | csv reader making each row a dictionary keyed by the header | [340](./notes/340-reading-a-csv-in-python-row-by-row.md) |
| diff | the lines a change removed (-) and added (+) | [333](./notes/333-pull-requests-asking-for-a-review-before-merging.md) |
| digital signature | a fingerprint locked with the private key, checkable with the public one | [320](./notes/320-digital-signatures-proof-a-message-came-from-the-key-holder.md) |
| dirty read | reading another transactions change before it is committed | [236](./notes/236-dirty-reads.md) |
| disk | storage like an SSD or hard drive, keeping bytes without power | [036](./notes/036-memory-vs-disk.md) |
| DISTINCT | keeps one copy of each repeated row in a query result | [121](./notes/121-distinct-removing-duplicate-rows.md) |
| DNS | a lookup service: send a name, get back an address | [306](./notes/306-dns-turning-names-into-addresses.md) |
| double counting | a sum repeating a value because a fan out copied its row | [165](./notes/165-double-counting-why-sums-after-a-fan-out-lie.md) |
| doubled quote | two quotes in a row inside a quoted value, meaning one quote | [064](./notes/064-quotes-inside-quotes-and-newlines-inside-values.md) |
| DROP TABLE | removes a table itself, its rows and its columns | [226](./notes/226-drop-and-truncate-emptying-a-table-vs-removing-it.md) |
| DuckDB | a database that runs inside your program, keeping data in one file | [102](./notes/102-a-database-in-one-file.md) |
| durability | the ACID promise: once COMMIT says done, a crash cant undo it | [229](./notes/229-acid-four-promises-a-database-makes.md) |
| embedded newline | a line ending inside a quoted csv value, not ending the row | [064](./notes/064-quotes-inside-quotes-and-newlines-inside-values.md) |
| encryption | turning bytes into other bytes, only the key turns them back | [317](./notes/317-encryption-locking-data-so-only-a-key-opens-it.md) |
| encryption key (not a database key) | a secret number the lock uses to scramble and unscramble | [317](./notes/317-encryption-locking-data-so-only-a-key-opens-it.md) |
| entity | a kind of thing you keep facts about, drawn as one table | [098](./notes/098-entity-relationship-diagrams.md) |
| entity relationship diagram | a picture of boxes for tables and lines for foreign keys | [098](./notes/098-entity-relationship-diagrams.md) |
| environment variable | a named piece of text handed to a program when it starts | [342](./notes/342-environment-variables-settings-that-live-outside-the-code.md) |
| epoch | the starting line, 1 January 1970 UTC, that unix time counts from | [025](./notes/025-unix-time.md) |
| exact decimal | a type keeping decimal digits exactly, like DECIMAL(6, 2) | [022](./notes/022-exact-decimal-types.md) |
| exact tie | an answer halfway between two floats, rounded to the one ending 0 | [020](./notes/020-why-0-1-plus-0-2-is-not-0-3.md) |
| EXCEPT | keeps first query rows missing from the second, order matters | [183](./notes/183-intersect-and-except.md) |
| exception | python stopping a line it cant do, unless a try catches it | [334](./notes/334-errors-in-scripts-catching-them-without-hiding-them.md) |
| EXCLUDED | in an upsert, the row you tried to insert | [224](./notes/224-upsert-insert-or-update-in-one-statement.md) |
| EXISTS | true when the inner query returns at least one row | [178](./notes/178-exists-and-not-exists-asking-whether-a-matching-row-exists.md) |
| EXPLAIN | Postgres command that shows the plan it would use for a query | [285](./notes/285-full-table-scan-reading-every-page.md) |
| EXPLAIN ANALYZE | EXPLAIN that runs the query and prints real rows and times too | [302](./notes/302-explain-analyze-the-planners-guesses-vs-what-really-happened.md) |
| explode | turning a record holding a list into one row per list item | [071](./notes/071-exploding-lists-into-many-rows.md) |
| expression index | an index built on a functions result, like lower(name) | [295](./notes/295-functions-on-a-column-why-the-index-gets-skipped.md) |
| fan out | a join keeping a left row once per matching right row | [164](./notes/164-fan-out-when-a-join-multiplies-rows.md) |
| field | one fact every row has a spot for, like city | [079](./notes/079-a-table-rows-are-records-columns-are-fields.md) |
| file | a name plus a list of bytes in order, kept on disk | [039](./notes/039-a-file-is-a-named-list-of-bytes.md) |
| file extension | the letters after the dot in a name, just a label | [039](./notes/039-a-file-is-a-named-list-of-bytes.md) |
| fingerprint | the fixed-size output of a cryptographic hash | [319](./notes/319-cryptographic-hashes-a-fingerprint-you-cant-reverse.md) |
| first normal form | every cell holds exactly one value, never a list | [259](./notes/259-first-normal-form-one-value-per-cell.md) |
| flat (growth) | steps stay the same however big the data gets | [270](./notes/270-flat-and-straight-line-the-two-shapes-of-growth.md) |
| flattening | turning inner names into columns, like address_city, one per name | [070](./notes/070-flattening-nested-objects-into-columns.md) |
| float | binary digits plus a count of how far to slide the point | [019](./notes/019-floating-point.md) |
| flush | force waiting data onto disk before moving on | [232](./notes/232-durability-surviving-a-crash.md) |
| folder | a named place on disk holding files and other folders | [040](./notes/040-folders-and-paths.md) |
| foreign key | a column holding another tables primary key values, a pointer | [093](./notes/093-foreign-key.md) |
| FROM | the clause naming the table a query reads from | [104](./notes/104-select-and-from-picking-columns.md) |
| full join | a join keeping unmatched rows from both tables, nulls fill the gaps | [162](./notes/162-right-and-full-outer-joins.md) |
| full run order (of a query) | FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY, LIMIT | [153](./notes/153-the-full-run-order-with-group-by-and-having.md) |
| full table scan | reading every page of a table and testing every row | [285](./notes/285-full-table-scan-reading-every-page.md) |
| function | SQL that takes a value and returns a new one | [124](./notes/124-text-functions-lower-upper-length-and-trim.md) |
| function (python) | a value you can store, pass to other functions, or call | [337](./notes/337-functions-as-values-handing-a-function-to-another-function.md) |
| functional dependency | one column decides another: each value gives exactly one value | [258](./notes/258-functional-dependency-when-one-column-decides-another.md) |
| gap (between islands) | the empty days between two runs of days with orders | [195](./notes/195-gaps-and-islands-date-minus-row-number.md) |
| generate_series | a function in FROM making one row per step, stop included | [197](./notes/197-generate-series-a-column-of-consecutive-days.md) |
| GET | HTTP method meaning give me this, changing nothing | [309](./notes/309-http-methods-get-asks-post-sends.md) |
| gibibyte | 1024 x 1024 x 1024 bytes, written GiB | [038](./notes/038-1000-or-1024.md) |
| gigabyte | 1000 megabytes, a billion bytes, written GB | [033](./notes/033-kilobytes-to-terabytes.md) |
| git | a tool that saves snapshots of a project folder | [329](./notes/329-git-commits-as-snapshots-of-your-code.md) |
| git add | picks which files go into the next snapshot | [329](./notes/329-git-commits-as-snapshots-of-your-code.md) |
| grand total | the one row that sums up every row of the result | [152](./notes/152-rollup-subtotals-and-grand-totals.md) |
| grapheme | one unit as seen on screen, possibly several code points | [012](./notes/012-combining-marks.md) |
| grep | prints every line containing the given pattern, anywhere in the line | [056](./notes/056-grep-finding-matching-lines.md) |
| group (GROUP BY) | all rows sharing one value of the grouped column, aggregated together | [143](./notes/143-group-by-one-group-per-value.md) |
| GROUP BY | makes one group per different value, then one aggregate row each | [143](./notes/143-group-by-one-group-per-value.md) |
| GROUP BY rule | every SELECT column must be grouped or inside an aggregate | [145](./notes/145-the-group-by-rule-every-column-is-grouped-or-aggregated.md) |
| grouping by several columns | one group per different combination of the values, only combinations that exist | [144](./notes/144-grouping-by-more-than-one-column.md) |
| grouping() | gives 1 on a made-up total row, 0 on a real group | [152](./notes/152-rollup-subtotals-and-grand-totals.md) |
| handshake (TLS) | the opening exchange where browser and server agree a secret key | [322](./notes/322-encryption-in-transit-tls-and-https.md) |
| hard delete | a real DELETE: the row is physically removed | [266](./notes/266-soft-deletes-marking-a-row-gone-instead-of-removing-it.md) |
| hash function | turns any input into a number, same input always same number | [277](./notes/277-hash-functions-turning-anything-into-a-number-in-a-fixed-range.md) |
| hash join | join: hash one side into a table, look up the other | [299](./notes/299-hash-join-build-a-hash-table-then-look-up-each-row.md) |
| hash table | slots where a keys hash picks the one place to look | [278](./notes/278-hash-tables-how-a-dictionary-finds-a-key-without-searching.md) |
| HAVING | a filter on groups, run after GROUP BY, testing an aggregate | [146](./notes/146-having-filtering-whole-groups.md) |
| head | prints the first lines of a file, 10 unless -n says otherwise | [054](./notes/054-head-and-tail.md) |
| header row | the first line of a csv, holding column names instead of data | [065](./notes/065-the-header-row-naming-the-columns.md) |
| hexadecimal | counting with sixteen digits, a to f standing for ten to fifteen | [005](./notes/005-hexadecimal.md) |
| Host header | the request line naming which site, since the address has no name | [310](./notes/310-http-headers-notes-attached-to-a-request.md) |
| host name | a text name for one machine, like shop.example | [306](./notes/306-dns-turning-names-into-addresses.md) |
| HTTP | rules the web uses: a text request, then a text response | [308](./notes/308-request-and-response-one-message-out-one-message-back.md) |
| HTTP header | one Name: value line between a messages first line and blank line | [310](./notes/310-http-headers-notes-attached-to-a-request.md) |
| HTTP method | the first word of a request, saying what kind of action | [309](./notes/309-http-methods-get-asks-post-sends.md) |
| HTTPError | error python raises when a response has a 4xx or 5xx status | [343](./notes/343-calling-an-api-from-python-status-first-then-parse.md) |
| HTTPS | HTTP sent through a TLS lock, the wire shows locked bytes | [322](./notes/322-encryption-in-transit-tls-and-https.md) |
| ILIKE | LIKE that ignores upper and lower case | [113](./notes/113-like-matching-text-patterns.md) |
| image | the frozen packed box a container starts from, never changes | [209](./notes/209-images-and-containers-the-packed-box-and-the-running-copy.md) |
| import | runs a module file once and hands your code its names | [325](./notes/325-modules-and-imports-using-code-from-other-files.md) |
| IN | keeps a row if its value equals any item in a list | [111](./notes/111-in-matching-against-a-list.md) |
| index (database) | a separate sorted list of values, each with its rows address | [286](./notes/286-index-a-sorted-shortcut-to-rows.md) |
| index (pandas) | the row labels down a dataframes left side, not a shortcut | [345](./notes/345-a-dataframe-a-table-in-memory.md) |
| index lookup | walk from root page down, one child per page, to the row | [288](./notes/288-one-lookup-traced-through-a-b-tree.md) |
| index overhead | what each index adds: disk pages, plus one entry per insert | [293](./notes/293-what-indexes-cost-slower-writes-and-more-disk.md) |
| index-only scan | Postgres answering a query from the index without visiting the table | [292](./notes/292-covering-index-when-the-index-alone-has-the-answer.md) |
| inner join | a join keeping only pairs where the match holds, dropping the rest | [156](./notes/156-inner-join-traced-by-hand.md) |
| inner side | the table a join searches once for every outer row | [298](./notes/298-nested-loop-join-for-each-outer-row-search-the-inner-side.md) |
| INSERT | adds new rows to a table, matching values to columns | [220](./notes/220-insert-adding-rows-and-matching-values-to-columns.md) |
| insert anomaly | a fact cant be stored until an unrelated fact exists | [090](./notes/090-insert-and-delete-anomalies.md) |
| INSERT from a SELECT | adds the rows a query returns, matched to columns by position | [221](./notes/221-insert-from-a-select-copying-rows-from-a-query.md) |
| integer division | dividing whole numbers and keeping only the whole part | [131](./notes/131-integer-division-when-7-divided-by-2-gives-3.md) |
| integer size | how many bits a whole number gets, which sets its range | [015](./notes/015-integer-sizes.md) |
| INTERSECT | keeps only rows that appear in both queries | [183](./notes/183-intersect-and-except.md) |
| interval | a length of time, like 2 days, you add to a date | [128](./notes/128-adding-and-subtracting-intervals.md) |
| IS NOT DISTINCT FROM | an equals that counts two nulls as the same, so they match | [166](./notes/166-joining-on-columns-that-can-be-null.md) |
| IS NOT NULL | the test that is true when a value is present, never unknown | [115](./notes/115-is-null-and-is-not-null.md) |
| IS NULL | the test that is true when a value is missing, never unknown | [115](./notes/115-is-null-and-is-not-null.md) |
| island | a run of consecutive days, rows with no break between them | [195](./notes/195-gaps-and-islands-date-minus-row-number.md) |
| isolation | the ACID promise: simultaneous users dont see half done work | [229](./notes/229-acid-four-promises-a-database-makes.md) |
| isolation level | the setting for how much of others work a transaction sees | [239](./notes/239-isolation-levels-read-committed.md) |
| join | pairing rows of two tables where a foreign key equals the id | [155](./notes/155-why-joins-the-answer-lives-in-more-than-one-table.md) |
| join chain | joins in a row, each pairing the last result with a table | [163](./notes/163-joining-three-tables.md) |
| join filter placement | a right side test in WHERE runs after the join, dropping NULLs | [161](./notes/161-a-where-that-quietly-turns-a-left-join-into-an-inner-join.md) |
| join null | a null a left join fills in for a missing partner | [160](./notes/160-the-nulls-a-left-join-creates.md) |
| JSON | a text format of records, with a name next to every value | [066](./notes/066-json-records-with-names-on-every-value.md) |
| JSON array | square brackets around values in order, like a python list | [067](./notes/067-json-types.md) |
| JSON lines | a text file with one whole JSON record per line | [069](./notes/069-json-lines.md) |
| JSON object | curly braces around name: value pairs, like a dictionary | [067](./notes/067-json-types.md) |
| JSON path | a $.name address telling a query which value to pull out | [205](./notes/205-querying-json-inside-a-column.md) |
| JSON types | the six kinds of value: string, number, boolean, null, object, array | [067](./notes/067-json-types.md) |
| json.load | reads a whole JSON file into python values in one go | [341](./notes/341-reading-json-in-python-the-whole-file-at-once.md) |
| jump | asking for a file position directly, called seek in python | [043](./notes/043-reading-start-to-end-vs-jumping.md) |
| junction table | a table with one row per pair, pointing at both sides | [097](./notes/097-junction-tables.md) |
| kernel | the core of the operating system, shared by containers | [208](./notes/208-containers-a-program-packed-with-everything-it-needs.md) |
| key constraint | a key rule declared in CREATE TABLE, enforced on every insert | [218](./notes/218-key-constraints-primary-key-and-references-in-create-table.md) |
| key function | a function sorted calls once per item to get its sort value | [337](./notes/337-functions-as-values-handing-a-function-to-another-function.md) |
| key pair | a public key and a private key made together | [318](./notes/318-public-and-private-keys-locking-without-sharing-a-secret.md) |
| kibibyte | 1024 bytes, the unambiguous 1024 based unit, written KiB | [038](./notes/038-1000-or-1024.md) |
| kilobyte | 1000 bytes, written KB | [033](./notes/033-kilobytes-to-terabytes.md) |
| LAG | a window function that returns a value from an earlier row | [192](./notes/192-lag-and-lead-looking-at-the-row-before.md) |
| latency | the wait for a request to go out and back | [323](./notes/323-latency-and-bandwidth-slow-vs-narrow.md) |
| LEAD | a window function that returns a value from a later row | [192](./notes/192-lag-and-lead-looking-at-the-row-before.md) |
| leading zero | a front 0 that numbers drop and text keeps | [263](./notes/263-choosing-column-types-by-what-you-do-with-the-value.md) |
| leaf | a tree node with no children under it | [280](./notes/280-trees-data-that-branches.md) |
| left join | inner join plus every unmatched left row, with null on the right | [159](./notes/159-left-join-keep-every-row-from-the-left-table.md) |
| left table | the table written before the word JOIN in the query | [159](./notes/159-left-join-keep-every-row-from-the-left-table.md) |
| leftmost prefix rule | an index only jumps for questions starting at its first column | [291](./notes/291-the-leftmost-prefix-rule-which-questions-a-composite-index-can-answer.md) |
| length | how many characters a text has, spaces included, not bytes | [124](./notes/124-text-functions-lower-upper-length-and-trim.md) |
| LF | a one character line ending, 0a, common on linux and mac | [042](./notes/042-line-endings.md) |
| library | code other people wrote that your program calls | [208](./notes/208-containers-a-program-packed-with-everything-it-needs.md) |
| LIKE | keeps text matching a pattern, % any run, _ one character | [113](./notes/113-like-matching-text-patterns.md) |
| LIMIT | keeps only the first n rows of the result | [120](./notes/120-limit-and-offset-paging-through-rows.md) |
| line ending | the characters marking where one line stops, the next starts | [042](./notes/042-line-endings.md) |
| localhost | the name for this same machine, address 127.0.0.1 | [306](./notes/306-dns-turning-names-into-addresses.md) |
| lock | a mark a transaction puts on data so others must wait | [242](./notes/242-row-locks-and-table-locks.md) |
| lock_timeout | a setting: give up if a lock wait lasts longer than this | [248](./notes/248-the-swap-renaming-two-columns-in-one-transaction.md) |
| logical order (of a query) | the fixed clause order: FROM, WHERE, SELECT, ORDER BY, LIMIT | [134](./notes/134-the-order-sql-really-runs-in.md) |
| long and wide | long: many rows per thing. wide: one row, many columns | [151](./notes/151-pivoting-turning-rows-into-columns.md) |
| lookup | fetching one value from a random spot | [037](./notes/037-disk-is-slow.md) |
| lost update (database) | two transactions use one old value, the later write erases the earlier | [235](./notes/235-lost-updates.md) |
| lost update (files) | two saves of one file, the later one erases the earlier change | [081](./notes/081-why-a-shared-spreadsheet-breaks.md) |
| lower | a function turning every letter to lower case | [124](./notes/124-text-functions-lower-upper-length-and-trim.md) |
| made up id | a number handed out by the database, meaningless outside it | [088](./notes/088-natural-keys-vs-made-up-ids.md) |
| many to many | rows on each side can match many rows on the other | [096](./notes/096-why-many-to-many-cant-live-in-either-table.md) |
| materialized view | a view that stores its answer instead of rerunning the query | [181](./notes/181-views-a-saved-query-with-a-name.md) |
| max | returns the biggest non-null value in a column, or the latest date | [142](./notes/142-min-and-max-the-smallest-and-biggest-value.md) |
| median | the middle value once sorted, or the average of the two middles | [149](./notes/149-median-the-middle-value-after-sorting.md) |
| megabyte | 1000 kilobytes, a million bytes, written MB | [033](./notes/033-kilobytes-to-terabytes.md) |
| memory | the computers working space (RAM), emptied when the power goes off | [036](./notes/036-memory-vs-disk.md) |
| merge | combining two sorted lists into one by taking the smaller front | [274](./notes/274-merging-two-sorted-lists-into-one.md) |
| merge commit | a commit with two parents, joining two lines of work | [332](./notes/332-merge-conflicts-when-git-cant-combine-two-edits.md) |
| merge conflict (git) | both branches changed the same lines, so git asks you to choose | [332](./notes/332-merge-conflicts-when-git-cant-combine-two-edits.md) |
| merge join | Postgres join: sort both sides, walk them side by side once | [300](./notes/300-merge-join-walk-two-sorted-lists-side-by-side.md) |
| merge sort | treat items as lists of one, merge pairs, repeat until one list | [275](./notes/275-merge-sort-split-down-to-single-items-then-merge-back-up.md) |
| method | a function stored on a class, called on one of its objects | [336](./notes/336-classes-in-one-picture-data-and-functions-together.md) |
| microsecond | a millionth of a second | [026](./notes/026-seconds-milliseconds-microseconds.md) |
| millisecond | a thousandth of a second | [026](./notes/026-seconds-milliseconds-microseconds.md) |
| min | returns the smallest non-null value in a column, or the earliest date | [142](./notes/142-min-and-max-the-smallest-and-biggest-value.md) |
| modeling | deciding the tables, and which table each fact belongs in, before SQL | [254](./notes/254-modeling-deciding-the-tables-before-writing-them.md) |
| module | a python file whose names other files can import | [325](./notes/325-modules-and-imports-using-code-from-other-files.md) |
| most common values | the values a column holds most, saved with their shares | [297](./notes/297-statistics-how-the-planner-guesses-row-counts.md) |
| MVCC | Postgres never overwrites a row, an UPDATE writes a new version | [249](./notes/249-mvcc-an-update-writes-a-new-row-version.md) |
| naming convention | habits for naming tables and columns so others can guess them | [264](./notes/264-naming-conventions-names-people-can-guess.md) |
| nan | not a number, what 0 / 0 gives in DuckDB | [130](./notes/130-nullif-and-dividing-by-zero.md) |
| nanosecond | a billionth of a second | [037](./notes/037-disk-is-slow.md) |
| natural key | a real world value that already tells rows apart, like an email | [088](./notes/088-natural-keys-vs-made-up-ids.md) |
| negative zero | a second zero pattern, with the sign bit set | [013](./notes/013-negative-numbers-sign-bit.md) |
| nested loop | a loop inside a loop, steps are outer length times inner length | [272](./notes/272-a-loop-inside-a-loop-the-steps-are-one-list-times-the-other.md) |
| nested loop join | Postgres join: for each outer row, search the inner side | [298](./notes/298-nested-loop-join-for-each-outer-row-search-the-inner-side.md) |
| nesting | an object or array sitting inside another one, as deep as needed | [068](./notes/068-nesting.md) |
| network | a way to move bytes from one computer to another | [084](./notes/084-a-network.md) |
| nextval | the call that hands out a sequences next number | [219](./notes/219-sequences-where-made-up-ids-come-from.md) |
| no promised order | without ORDER BY, rows may come back in any order | [118](./notes/118-no-order-by-no-promised-order.md) |
| node | a box in a tree holding one value, pointing to its children | [280](./notes/280-trees-data-that-branches.md) |
| non repeatable read | reading one row twice in a transaction and getting different values | [237](./notes/237-non-repeatable-reads.md) |
| normal form | a named checklist a table passes to avoid a copy bug | [257](./notes/257-normal-forms-the-rules-behind-splitting-tables.md) |
| NOT | flips a test, but a null stays unknown and is dropped | [110](./notes/110-not-flipping-a-condition.md) |
| NOT EXISTS | true when the inner query returns no rows at all | [178](./notes/178-exists-and-not-exists-asking-whether-a-matching-row-exists.md) |
| NOT IN | keeps non-matches, but one NULL in the list empties the result | [179](./notes/179-not-in-and-the-null-trap.md) |
| NOT NULL | a column rule: the database refuses any row where it is null | [215](./notes/215-not-null-and-default-required-columns-and-fallback-values.md) |
| null | a marker meaning there is no value here, not a value | [031](./notes/031-null.md) |
| NULLIF | hands back null when two values are equal, else the first | [130](./notes/130-nullif-and-dividing-by-zero.md) |
| NULLS FIRST | the ORDER BY option that puts missing values at the start | [119](./notes/119-where-nulls-land-when-you-sort.md) |
| NULLS LAST | the ORDER BY option that puts missing values at the end | [119](./notes/119-where-nulls-land-when-you-sort.md) |
| OAuth | how an app gets a token for someone without their password | [316](./notes/316-oauth-in-one-picture-a-token-without-the-password.md) |
| object (python) | one thing built from a class, holding its own data | [336](./notes/336-classes-in-one-picture-data-and-functions-together.md) |
| OFFSET (rows) | skips this many result rows before returning any | [120](./notes/120-limit-and-offset-paging-through-rows.md) |
| offset (time zones) | how far a clock sits ahead of or behind UTC, like +05:30 | [028](./notes/028-time-zone-offsets.md) |
| ON | the join test that decides which pairs of rows are kept | [157](./notes/157-on-how-a-join-decides-which-rows-match.md) |
| one to many | one row on one side matches many rows on the other | [092](./notes/092-relationships-one-customer-many-orders.md) |
| one to one | each row matches at most one row in the other table | [256](./notes/256-one-to-one-when-two-tables-share-a-key.md) |
| operating system | the program that starts programs and shares the machine between them | [051](./notes/051-the-operating-system.md) |
| optional field | a field a record may leave out without being rejected | [077](./notes/077-required-vs-optional-fields.md) |
| OR | joins two tests, keeping a row if either is true | [108](./notes/108-and-or-combining-two-tests.md) |
| ORDER BY | sorts the returned rows by a column, later columns only break ties | [117](./notes/117-order-by-sorting-by-one-or-more-columns.md) |
| origin | the usual nickname git gives the remote you cloned from | [331](./notes/331-pushing-and-pulling-sharing-code-through-a-remote.md) |
| orphan row | a row whose foreign key matches no row in the other table | [094](./notes/094-what-a-foreign-key-stops.md) |
| os.environ | pythons dictionary-like view of its environment variables, values all text | [342](./notes/342-environment-variables-settings-that-live-outside-the-code.md) |
| outer side | the table a join reads once, row by row | [298](./notes/298-nested-loop-join-for-each-outer-row-search-the-inner-side.md) |
| overflow | a result too big for its bit size, wrapping or erroring | [016](./notes/016-overflow.md) |
| package | a bundle of python modules other people wrote and shared | [327](./notes/327-packages-and-pip-installing-code-other-people-wrote.md) |
| page (Postgres) | a fixed 8192 byte chunk of a table file, packed with rows | [284](./notes/284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md) |
| page split | a full page divides in two and its parent gains a signpost | [289](./notes/289-how-a-b-tree-stays-balanced-as-rows-arrive.md) |
| pandas | a python package that gives you dataframes | [345](./notes/345-a-dataframe-a-table-in-memory.md) |
| parent folder | the folder holding this one, written .. in a path | [053](./notes/053-absolute-vs-relative-paths.md) |
| partial dependency | a column decided by only part of a two column key | [260](./notes/260-second-normal-form-nothing-about-half-the-key.md) |
| partition (window functions) | one group of rows sharing a value, inside a window | [186](./notes/186-partition-by-a-separate-window-per-group.md) |
| PARTITION BY | inside OVER, cuts the window into one group per value | [186](./notes/186-partition-by-a-separate-window-per-group.md) |
| path | folder names from the top down to a file, joined by slashes | [040](./notes/040-folders-and-paths.md) |
| path (URL) | the part after the host saying which thing on that server | [307](./notes/307-urls-and-query-parameters.md) |
| percentile | the value some fraction of the way through the sorted column | [150](./notes/150-percentiles-the-medians-cousins.md) |
| phantom read | a re-run query in one transaction returns a different set of rows | [238](./notes/238-phantoms.md) |
| pid | the number the system gives one running process, new each run | [050](./notes/050-processes.md) |
| pip | the program that downloads a package from PyPI and installs it | [327](./notes/327-packages-and-pip-installing-code-other-people-wrote.md) |
| pipe (shell) | joins one programs output to the next programs input | [058](./notes/058-pipes.md) |
| PITR | short for point in time recovery | [252](./notes/252-point-in-time-recovery-a-backup-plus-the-replayed-log.md) |
| pivot | turning the values of one column into columns of their own | [151](./notes/151-pivoting-turning-rows-into-columns.md) |
| place value | what a digit is worth because of where it sits | [003](./notes/003-counting-in-binary.md) |
| placeholder value | a made up value, like 0, standing in for missing | [032](./notes/032-null-is-not-zero-or-empty-text.md) |
| plan | the steps Postgres picks to run a query | [296](./notes/296-the-query-planner-picking-the-cheapest-plan.md) |
| plan tree | a plan drawn as nodes, with rows moving up to the root | [301](./notes/301-reading-explain-the-plan-as-a-tree.md) |
| point in time recovery | restore a backup, replay the log, stop at a time you pick | [252](./notes/252-point-in-time-recovery-a-backup-plus-the-replayed-log.md) |
| port | a number picking which program on a machine gets the bytes | [085](./notes/085-addresses-and-ports.md) |
| port mapping | the -p flag: laptop port forwards to a port inside the container | [210](./notes/210-running-postgres-in-a-container-on-your-laptop.md) |
| positional insert | an INSERT with no column list, values fill columns in table order | [220](./notes/220-insert-adding-rows-and-matching-values-to-columns.md) |
| POST | HTTP method meaning here is data, act on it | [309](./notes/309-http-methods-get-asks-post-sends.md) |
| Postgres | a popular database server | [211](./notes/211-a-database-server-postgres-where-most-app-data-lives.md) |
| precedence | which operator runs first when a test mixes several, AND before OR | [109](./notes/109-parentheses-and-runs-before-or.md) |
| precision | the most digits a decimal can hold in total | [022](./notes/022-exact-decimal-types.md) |
| primary key | a column that is unique in every row and never NULL | [087](./notes/087-primary-key.md) |
| private key | the half of a key pair you never share | [318](./notes/318-public-and-private-keys-locking-without-sharing-a-secret.md) |
| probe (hash join) | reading the outer side, one hash table look per row | [299](./notes/299-hash-join-build-a-hash-table-then-look-up-each-row.md) |
| process | one running copy of a program, loaded into memory | [050](./notes/050-processes.md) |
| processor | the CPU, the part of the computer doing tiny steps on numbers | [035](./notes/035-the-processor.md) |
| program | a file of bytes on disk that can be run | [050](./notes/050-processes.md) |
| public key | the half of a key pair you hand to anyone | [318](./notes/318-public-and-private-keys-locking-without-sharing-a-secret.md) |
| pull (git) | download new commits from the remote and combine them with yours | [331](./notes/331-pushing-and-pulling-sharing-code-through-a-remote.md) |
| pull request | a proposal on the remote to merge a branch, open for review | [333](./notes/333-pull-requests-asking-for-a-review-before-merging.md) |
| push (git) | upload your new commits to the remote | [331](./notes/331-pushing-and-pulling-sharing-code-through-a-remote.md) |
| PyPI | the public shelf of python packages, the Python Package Index | [327](./notes/327-packages-and-pip-installing-code-other-people-wrote.md) |
| query | one request sent to a database, naming the result you want | [101](./notes/101-sql-you-describe-the-result.md) |
| query parameter | a key=value filter after the ? in a URL | [307](./notes/307-urls-and-query-parameters.md) |
| query planner | the part of Postgres that prices the ways to run a query | [296](./notes/296-the-query-planner-picking-the-cheapest-plan.md) |
| quoting (csv) | double quotes around a value so commas inside it stay text | [063](./notes/063-quoting-commas-inside-values.md) |
| range join | a join whose ON is a BETWEEN, matching values to periods | [170](./notes/170-joining-on-a-range-matching-a-date-to-a-period.md) |
| RANK | window function giving tied rows one number, then skipping past the tie | [188](./notes/188-rank-vs-dense-rank-what-ties-do.md) |
| read committed | default Postgres level: each query sees only data committed before it began | [231](./notes/231-isolation-two-people-at-the-same-time.md) |
| reading start to end | taking a files bytes in order from position 0 | [043](./notes/043-reading-start-to-end-vs-jumping.md) |
| record | one row of a table, one thing the data is about | [079](./notes/079-a-table-rows-are-records-columns-are-fields.md) |
| recursive CTE | a CTE that reads its own rows, repeating until none are found | [203](./notes/203-recursive-ctes-following-a-chain-of-rows.md) |
| redirect | > sends a programs stdout into a file, emptying it first | [059](./notes/059-redirecting-output-into-a-file.md) |
| refresh token | long lived string that is only swapped for a new access token | [315](./notes/315-tokens-that-expire-a-key-with-a-shelf-life.md) |
| register | a tiny holding spot inside the processor, where it works on numbers | [035](./notes/035-the-processor.md) |
| relationship | how rows in one table connect to rows in another | [092](./notes/092-relationships-one-customer-many-orders.md) |
| relative path | a path with no leading slash, begun at the working directory | [053](./notes/053-absolute-vs-relative-paths.md) |
| remainder | what is left after dividing, written % | [277](./notes/277-hash-functions-turning-anything-into-a-number-in-a-fixed-range.md) |
| remote | a copy of the repository on a server others can reach | [331](./notes/331-pushing-and-pulling-sharing-code-through-a-remote.md) |
| repeatable read | Postgres level: one picture, taken at the first query, kept all transaction | [240](./notes/240-repeatable-read-rows-dont-change-under-you-mid-transaction.md) |
| repeating fraction | digits past the point that loop forever, so no exact finite form | [018](./notes/018-why-0-1-has-no-exact-binary-form.md) |
| replay | reading the log forward and redoing changes the table files lack | [234](./notes/234-replaying-the-log-after-a-crash.md) |
| request (HTTP) | the text a client sends: what it wants, extra lines, optional body | [308](./notes/308-request-and-response-one-message-out-one-message-back.md) |
| required field | a field name every record must have, or it is rejected | [077](./notes/077-required-vs-optional-fields.md) |
| response (HTTP) | the text a server sends back: how it went, extra lines, body | [308](./notes/308-request-and-response-one-message-out-one-message-back.md) |
| restore | load a backup back, returning data to the moment of the copy | [251](./notes/251-backups-a-copy-you-can-restore-from.md) |
| retention | how many of a cohort logged in again in a later month | [202](./notes/202-retention-who-came-back-the-month-after.md) |
| revenue | quantity times price, added up over the order rows you choose | [171](./notes/171-joins-plus-group-by-revenue-per-customer.md) |
| right join | a left join with the tables swapped, keeps every right row | [162](./notes/162-right-and-full-outer-joins.md) |
| ROLLBACK | ends a transaction and throws away every change made inside it | [228](./notes/228-commit-and-rollback-keeping-or-undoing-a-transaction.md) |
| ROLLUP | a GROUP BY that adds subtotal rows and a grand total | [152](./notes/152-rollup-subtotals-and-grand-totals.md) |
| root | the top folder holding everything else, written as a single slash | [040](./notes/040-folders-and-paths.md) |
| root (tree) | the top node of a tree (root as top folder: see root) | [280](./notes/280-trees-data-that-branches.md) |
| rounds (merge sort) | how many times the lists get paired up and merged, halving backwards | [276](./notes/276-why-sorting-costs-more-than-one-pass-over-the-data.md) |
| row | one record of a csv, usually one line, split into values | [062](./notes/062-csv-rows-and-columns-separated-by-commas.md) |
| row lock | a mark on one row, so others changing it wait | [242](./notes/242-row-locks-and-table-locks.md) |
| row version | one stored copy of a row, an UPDATE makes a new one | [249](./notes/249-mvcc-an-update-writes-a-new-row-version.md) |
| ROW_NUMBER | window function that numbers rows 1, 2, 3 in the OVER ordering | [187](./notes/187-row-number-numbering-rows-in-order.md) |
| ROWS BETWEEN | sets a frame by counting rows before and after the current one | [190](./notes/190-window-frames-rows-between.md) |
| run | the same value repeated back to back | [047](./notes/047-compression-spotting-repeats.md) |
| run length encoding | storing each run as the value once plus a count | [047](./notes/047-compression-spotting-repeats.md) |
| running total | a sum where each row adds itself and every row before it | [189](./notes/189-running-totals.md) |
| safe write | write a whole new file beside the old, then rename it over | [046](./notes/046-writing-safely.md) |
| scalar subquery | a subquery returning one row and one column, used as a value | [176](./notes/176-scalar-subqueries-one-value-inside-a-query.md) |
| scale | how many of a decimals digits sit after the point | [022](./notes/022-exact-decimal-types.md) |
| schema (database) | a named folder of tables inside a database, written schema.table | [267](./notes/267-schemas-as-namespaces-folders-for-tables.md) |
| schema (file) | a written agreement on which fields every record must have | [075](./notes/075-schema.md) |
| schema on read | storing anything as it arrives, checking shape only when used | [083](./notes/083-schema-on-write-vs-schema-on-read.md) |
| schema on write | checking shape as data goes in, rejecting what doesnt fit | [083](./notes/083-schema-on-write-vs-schema-on-read.md) |
| scheme | the start of a URL, like http, naming the rules for talking | [307](./notes/307-urls-and-query-parameters.md) |
| scope (token) | the list of things a token is allowed to do | [316](./notes/316-oauth-in-one-picture-a-token-without-the-password.md) |
| script | a python file you run directly, not one you import | [326](./notes/326-running-a-python-script-from-the-terminal.md) |
| search path | the folders Postgres checks in order to find a bare table name | [267](./notes/267-schemas-as-namespaces-folders-for-tables.md) |
| second normal form | every column depends on the whole key, not half of it | [260](./notes/260-second-normal-form-nothing-about-half-the-key.md) |
| SELECT | the clause naming which columns to keep, in the order written | [104](./notes/104-select-and-from-picking-columns.md) |
| SELECT FOR UPDATE | a read that also locks the rows it returns until commit | [243](./notes/243-select-for-update-locking-on-purpose.md) |
| SELECT star | the shortcut for every column, in the tables order | [105](./notes/105-select-star-every-column.md) |
| selectivity | share of a tables rows that a condition keeps | [294](./notes/294-selectivity-when-an-index-doesnt-help.md) |
| self | a methods first parameter: the object it was called on | [336](./notes/336-classes-in-one-picture-data-and-functions-together.md) |
| self join | a table joined to a second copy of itself under another alias | [168](./notes/168-self-join-a-table-joined-to-itself.md) |
| semi join | keeps left rows that have a match, once each, never copies | [178](./notes/178-exists-and-not-exists-asking-whether-a-matching-row-exists.md) |
| Seq Scan | Postgres name for a full table scan in a plan | [285](./notes/285-full-table-scan-reading-every-page.md) |
| sequence | a counter the database keeps outside any table, only moving forward | [219](./notes/219-sequences-where-made-up-ids-come-from.md) |
| serializable | strictest level: results match some one-at-a-time order of transactions | [241](./notes/241-serializable-as-if-one-at-a-time-and-retrying-the-failures.md) |
| serialization failure | error 40001: Postgres refuses a transaction so the app must retry it | [241](./notes/241-serializable-as-if-one-at-a-time-and-retrying-the-failures.md) |
| server | a program that listens on a port and answers requests | [086](./notes/086-client-and-server.md) |
| session (clicks) | a run of one persons clicks, a long silence starts the next | [199](./notes/199-session-starts-flag-the-click-after-a-long-gap.md) |
| session (database) | one connections conversation with the database, with its own settings | [212](./notes/212-connections-and-sessions-one-conversation-with-the-database.md) |
| session id | the running sum of start flags, one number per session | [200](./notes/200-session-ids-a-running-sum-of-the-flags.md) |
| session key | the secret key picked in the handshake, locking everything after | [322](./notes/322-encryption-in-transit-tls-and-https.md) |
| shared_buffers | the setting that sizes the buffer pool, 128MB by default | [303](./notes/303-the-buffer-pool-keeping-hot-pages-in-memory.md) |
| shell | the program inside a terminal that reads your line and runs it | [049](./notes/049-the-terminal.md) |
| sign bit | the bit saying plus (0) or minus (1) | [013](./notes/013-negative-numbers-sign-bit.md) |
| signpost (B tree) | a value in a non-leaf page splitting which child to follow | [287](./notes/287-b-tree-pages-that-point-to-pages.md) |
| slot (hash table) | one numbered place in a hash table, holding a key and value | [278](./notes/278-hash-tables-how-a-dictionary-finds-a-key-without-searching.md) |
| slot (page) | a numbered seat for one row version on a Postgres page | [284](./notes/284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md) |
| snake_case | lowercase words joined by underscores, like ordered_at | [264](./notes/264-naming-conventions-names-people-can-guess.md) |
| snapshot (git) | the whole project folder as it was at one commit | [329](./notes/329-git-commits-as-snapshots-of-your-code.md) |
| snapshot (Postgres) | a note of which transactions had finished when a query began | [250](./notes/250-transaction-snapshots-what-your-transaction-is-allowed-to-see.md) |
| soft delete | marking a row gone with a deleted_at time instead of removing it | [266](./notes/266-soft-deletes-marking-a-row-gone-instead-of-removing-it.md) |
| splitting into tables | one table per kind of thing, other tables keep only its id | [091](./notes/091-splitting-into-tables.md) |
| SQL | the language you send a database to ask for rows | [101](./notes/101-sql-you-describe-the-result.md) |
| SQL dump | a text file of SQL commands that rebuilds a database when run | [103](./notes/103-your-first-query-against-the-shop.md) |
| SSD | a disk made of chips with no moving parts | [037](./notes/037-disk-is-slow.md) |
| standard input | stdin, the channel a process reads from, the keyboard by default | [057](./notes/057-standard-input-and-output.md) |
| standard output | stdout, the channel a process writes to, the screen by default | [057](./notes/057-standard-input-and-output.md) |
| statistics (planner) | per column summary Postgres saves to guess row counts | [297](./notes/297-statistics-how-the-planner-guesses-row-counts.md) |
| status code | 3 digit number on a responses first line, saying how it went | [311](./notes/311-status-codes-what-200-404-and-500-mean.md) |
| store UTC, show local | keep moments in UTC, convert to local only when displaying | [030](./notes/030-store-utc-show-local.md) |
| straight line (growth) | steps grow as fast as the data does | [270](./notes/270-flat-and-straight-line-the-two-shapes-of-growth.md) |
| streak row | one output row per island: first day, last day, length | [196](./notes/196-gaps-and-islands-one-row-per-streak.md) |
| stream | bytes handed over in order, like a program reading its stdin | [057](./notes/057-standard-input-and-output.md) |
| structure | an agreement on where each fact sits, so code can find it | [061](./notes/061-structure-why-text-is-hard-to-ask.md) |
| subquery | a SELECT in parentheses inside another query, run first | [174](./notes/174-subquery-in-where.md) |
| subquery in FROM | an inner SELECT the outer query reads like a table | [175](./notes/175-subquery-in-from.md) |
| substr | cuts a piece of text by start and count, counting from 1 | [125](./notes/125-concatenating-text-and-taking-pieces-of-it.md) |
| subtotal | the total for one group, shown as an extra row | [152](./notes/152-rollup-subtotals-and-grand-totals.md) |
| sum | adds up all the values in a column into one value | [140](./notes/140-sum-and-avg-adding-up-and-averaging.md) |
| swap (column type) | renaming the new column to the old name in one transaction | [248](./notes/248-the-swap-renaming-two-columns-in-one-transaction.md) |
| symmetric encryption | one key both locks and unlocks the data | [317](./notes/317-encryption-locking-data-so-only-a-key-opens-it.md) |
| sys.argv | the list of words typed after python3, script name first, all text | [326](./notes/326-running-a-python-script-from-the-terminal.md) |
| table | a grid of rows, every row holding the same columns | [079](./notes/079-a-table-rows-are-records-columns-are-fields.md) |
| table alias | a short name for a table, valid for one query only | [158](./notes/158-table-aliases-short-nicknames-for-tables.md) |
| table lock | a mark on a whole table, the strongest also blocks plain reads | [242](./notes/242-row-locks-and-table-locks.md) |
| table rewrite | storing every row again in a fresh copy of the table | [245](./notes/245-changing-a-column-type-the-table-rewrite-and-the-lock.md) |
| tag | a name in angle brackets, opening or closing an XML value | [072](./notes/072-xml.md) |
| tail | prints the last lines of a file, 10 unless -n says otherwise | [054](./notes/054-head-and-tail.md) |
| temporary table | a table dropped when its session ends, visible only there | [214](./notes/214-temporary-tables.md) |
| terabyte | 1000 gigabytes, a trillion bytes, written TB | [033](./notes/033-kilobytes-to-terabytes.md) |
| terminal | a text window where you type a line and the computer replies | [049](./notes/049-the-terminal.md) |
| text file | a file whose bytes decode as characters, usually with UTF-8 | [041](./notes/041-text-files-vs-binary-files.md) |
| the shop | the imaginary gujarati snack store every example uses | [001](./notes/001-data-is-facts-and-numbers.md) |
| third normal form | every column is about the key and nothing but the key | [261](./notes/261-third-normal-form-nothing-but-the-key.md) |
| three valued logic | a test is true, false or unknown, and a null gives unknown | [114](./notes/114-three-valued-logic-true-false-and-unknown.md) |
| time of day | a clock reading with no day attached | [027](./notes/027-dates-and-times-apart.md) |
| timeout | seconds a program waits for a reply before giving up | [343](./notes/343-calling-an-api-from-python-status-first-then-parse.md) |
| TLS | the protocol that does a handshake, then locks all traffic | [322](./notes/322-encryption-in-transit-tls-and-https.md) |
| token | key string the server hands out, often with an expiry | [315](./notes/315-tokens-that-expire-a-key-with-a-shelf-life.md) |
| top N per group | keep the first N rows of each group: number inside, filter outside | [193](./notes/193-top-n-per-group.md) |
| torn write | a write cut off partway, leaving some new blocks and some old | [045](./notes/045-torn-writes.md) |
| traceback | the trail of lines python prints when an exception stops a script | [334](./notes/334-errors-in-scripts-catching-them-without-hiding-them.md) |
| trade off | anything speeding up reads must be kept up on every write | [282](./notes/282-the-trade-off-faster-reads-usually-mean-slower-writes.md) |
| transaction | a group of changes that all happen or none do | [227](./notes/227-transactions-all-or-nothing.md) |
| tree | nodes linked parent to children, a lookup follows one path down | [280](./notes/280-trees-data-that-branches.md) |
| trigger | a rule the database runs by itself on every write | [247](./notes/247-keeping-the-new-column-in-sync-with-a-trigger.md) |
| trim | a function cutting spaces off both ends of text | [124](./notes/124-text-functions-lower-upper-length-and-trim.md) |
| TRUNCATE | removes every row at once and keeps the empty table | [226](./notes/226-drop-and-truncate-emptying-a-table-vs-removing-it.md) |
| try/except | python code that catches one named kind of exception and carries on | [334](./notes/334-errors-in-scripts-catching-them-without-hiding-them.md) |
| TRY_CAST | CAST that gives null instead of an error when conversion fails | [133](./notes/133-casts-that-fail-and-try-cast.md) |
| tuple (python) | a fixed list of values, safe to use as a dictionary key | [344](./notes/344-practice-dedupe-and-count-orders-in-plain-python.md) |
| twos complement | binary where the leftmost place is negative, so one zero | [014](./notes/014-twos-complement.md) |
| type by use | choose a type by what you do with the value | [263](./notes/263-choosing-column-types-by-what-you-do-with-the-value.md) |
| UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING | frame option meaning every row of the window, no limit either way | [191](./notes/191-the-default-frame-trap.md) |
| Unicode | one agreed table giving every character in every script a number | [009](./notes/009-unicode.md) |
| UNION | stacks two queries rows, then drops repeated rows | [182](./notes/182-union-and-union-all.md) |
| UNION ALL | stacks two queries rows and keeps every repeat | [182](./notes/182-union-and-union-all.md) |
| UNIQUE | a column rule: the database refuses a value already in the column | [216](./notes/216-unique-no-two-rows-may-share-a-value.md) |
| unix time | a moment kept as seconds counted since the epoch | [025](./notes/025-unix-time.md) |
| unknown | the third test result, from a null, that WHERE drops | [114](./notes/114-three-valued-logic-true-false-and-unknown.md) |
| UNNEST | turns each item of a list cell into its own row | [204](./notes/204-arrays-and-unnest-lists-inside-a-cell.md) |
| UPDATE | changes values in rows that already exist | [222](./notes/222-update-changing-rows-and-why-the-where-matters.md) |
| update anomaly | one fact stored in many rows, an update changing only some | [089](./notes/089-update-anomalies.md) |
| UPDATE without WHERE | changes every row in the table, with no warning | [222](./notes/222-update-changing-rows-and-why-the-where-matters.md) |
| updated_at | a column holding when the row last changed, moved by every update | [265](./notes/265-created-at-and-updated-at-two-timestamps-every-table-carries.md) |
| upper | a function turning every letter to upper case | [124](./notes/124-text-functions-lower-upper-length-and-trim.md) |
| upsert | an INSERT that updates the row instead if its key exists | [224](./notes/224-upsert-insert-or-update-in-one-statement.md) |
| URL | one text string holding scheme, host, port, path and query | [307](./notes/307-urls-and-query-parameters.md) |
| urlopen | python function that sends a request and returns the response | [343](./notes/343-calling-an-api-from-python-status-first-then-parse.md) |
| UTC | the one clock everyone measures against, with no daylight saving | [024](./notes/024-utc.md) |
| UTF-8 | a way to store each code point as 1 to 4 bytes | [010](./notes/010-utf-8.md) |
| VACUUM | Postgres command that frees dead row versions for reuse | [304](./notes/304-vacuum-how-postgres-cleans-up-old-row-versions.md) |
| valid state | every declared rule true at once, before and after a transaction | [230](./notes/230-acid-consistency-the-rules-still-hold-after-every-change.md) |
| venv | a folder with its own python and its own installed packages | [328](./notes/328-venvs-one-set-of-installed-packages-per-project.md) |
| view | a query saved under a name, rerun on every read | [181](./notes/181-views-a-saved-query-with-a-name.md) |
| WAL | short for write ahead log | [233](./notes/233-the-write-ahead-log-write-down-the-plan-before-the-change.md) |
| wc | prints a files counts; wc -l counts its 0a line endings | [055](./notes/055-wc-counting-lines.md) |
| WHERE | the clause keeping only rows whose condition is true, checked before SELECT | [106](./notes/106-where-keeping-only-the-rows-that-match.md) |
| WHERE vs HAVING | WHERE tests single rows before grouping, HAVING tests groups after | [147](./notes/147-where-vs-having-before-grouping-or-after.md) |
| whole cents | money kept as an integer count of cents, price times 100 | [021](./notes/021-storing-money-as-whole-cents.md) |
| wildcard | a pattern character standing in for other characters | [113](./notes/113-like-matching-text-patterns.md) |
| window | the rows a window function sees while working on one row | [185](./notes/185-over-the-window-a-function-looks-through.md) |
| window frame | the slice of the window a function uses for one row | [190](./notes/190-window-frames-rows-between.md) |
| window function | a calculation across rows that keeps every row, like sum with OVER | [184](./notes/184-window-functions-a-total-next-to-every-row.md) |
| with | opens something, runs a block, then closes it even after an error | [335](./notes/335-with-opening-and-closing-things-safely.md) |
| working directory | the folder a process stands in, where bare names are looked up | [052](./notes/052-the-working-directory.md) |
| worst case | the unluckiest input, like the wanted item sitting last | [269](./notes/269-big-o-in-plain-words-how-work-grows-as-data-grows.md) |
| wrapper | the function a decorator returns, which calls the original inside | [339](./notes/339-decorators-the-at-shorthand-for-wrapping-a-function.md) |
| write | any change to stored data, like an INSERT adding a row | [282](./notes/282-the-trade-off-faster-reads-usually-mean-slower-writes.md) |
| write ahead log | the databases own list of changes, flushed before table files change | [233](./notes/233-the-write-ahead-log-write-down-the-plan-before-the-change.md) |
| write buffer | memory where python parks small writes until the file closes | [335](./notes/335-with-opening-and-closing-things-safely.md) |
| xmax | stamp on a row version: the transaction that ended it | [249](./notes/249-mvcc-an-update-writes-a-new-row-version.md) |
| xmin | stamp on a row version: the transaction that created it | [249](./notes/249-mvcc-an-update-writes-a-new-row-version.md) |
| XML | a text format wrapping each value in opening and closing tags | [072](./notes/072-xml.md) |
| YAML | a text format where indentation shows nesting, dashes start list items | [073](./notes/073-yaml.md) |
| YAML trap | a bare word like no read as a boolean, so quote text | [074](./notes/074-yaml-traps.md) |

