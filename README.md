# data engineering notes

learning data engineering from the very bottom, one concept at a time, in public. starts at what a bit is and ends at designing data platforms. every note is a 2 minute read, every note links to the ones it builds on, and every example uses the same small imaginary snack shop so you always know the data.

start here: [001 data is facts written down](./notes/001-data-is-facts-and-numbers.md)

notes so far: 239

the map: [curriculum.md](./curriculum.md) | every term: [glossary.md](./glossary.md) | the shop data: [data/shop.sql](./data/shop.sql) | every fix: [CORRECTIONS.md](./CORRECTIONS.md)

## section 1: data at the atom level
- [001 data is facts written down](./notes/001-data-is-facts-and-numbers.md): one shop order, four answers, every one of them secretly numbers
- [002 bits, everything is a tiny switch](./notes/002-bits.md): one switch, two states, and why every extra one doubles what you can say
- [003 counting in binary](./notes/003-counting-in-binary.md): reading 101 as 5, the same way you already read 345
- [004 bytes, 8 bits and 256 possible values](./notes/004-bytes.md): why ip addresses and colors stop at 255
- [005 hexadecimal, counting with sixteen digits](./notes/005-hexadecimal.md): 16 digits, so 4 switches fit in one character
- [006 one byte, two hex digits](./notes/006-one-byte-two-hex-digits.md): why ff is 255, and why a byte never prints as one character
- [007 text is numbers, one character and one number](./notes/007-text-is-numbers.md): the 2 in a file is really 50, and why text numbers sort wrong
- [008 ascii runs out, 128 spots isnt enough for the world](./notes/008-ascii-runs-out.md): a gujarati letter has no spot, and one byte can mean three different letters
- [009 unicode, one number for every character](./notes/009-unicode.md): one table for every script, but it only picks numbers, not bytes
- [010 utf-8, storing those numbers in 1 to 4 bytes](./notes/010-utf-8.md): why é is one character on screen but two bytes in a file
- [011 why a gujarati letter takes 3 bytes and g takes 1](./notes/011-why-gujarati-takes-3-bytes.md): 12 bits of letter, but some bits in every byte are labels
- [012 combining marks, when one letter on screen is two numbers](./notes/012-combining-marks.md): two é that look identical but are not equal to the database
- [013 negative numbers, the sign bit idea](./notes/013-negative-numbers-sign-bit.md): one bit for the minus, and the odd cost of having two zeros
- [014 twos complement, how computers really store a minus](./notes/014-twos-complement.md): one place gets a minus sign and the two zeros disappear
- [015 integer sizes, 8, 16, 32 and 64 bit numbers](./notes/015-integer-sizes.md): why the shop would break at order 128 with one byte
- [016 overflow, what happens when a count goes past the top](./notes/016-overflow.md): a counter at 127 plus one quietly reads -128
- [017 fractions in binary, halves, quarters, eighths](./notes/017-fractions-in-binary.md): khandvi at 7.50 is 111.1, but 0.30 has no pattern that hits it
- [018 why 0.1 has no exact binary form](./notes/018-why-0-1-has-no-exact-binary-form.md): doubling 0.1 loops 0011 forever, so the computer keeps a close neighbor
- [019 floating point, digits plus where the point sits](./notes/019-floating-point.md): how 8 bytes hold both 0.000001 and a 300 digit number, and why +1 vanishes past 2 to the 53
- [020 why 0.1 + 0.2 is not exactly 0.3](./notes/020-why-0-1-plus-0-2-is-not-0-3.md): both are stored a bit too big, and their sum lands on a different float than 0.3
- [021 storing money as whole cents](./notes/021-storing-money-as-whole-cents.md): ten cents added three times isnt 0.30, so the shop keeps 600 instead of 6.00
- [022 exact decimal types](./notes/022-exact-decimal-types.md): the shop price column passes the 0.1 + 0.2 test on 6 of 6 rows, because it stores digits, not a float
- [023 true and false, the boolean](./notes/023-true-and-false-the-boolean.md): asking if an order is delivered gives back true or false, one bit of information that still costs a byte
- [024 UTC, the worlds reference clock](./notes/024-utc.md): order 101 says 09:15, but 09:15 where? one moment reads 13:15, 09:15 or 18:45 depending on the clock
- [025 unix time, counting seconds from 1970](./notes/025-unix-time.md): one moment, 13:15 UTC on 1 April, is the same number 1775049300 on every clock
- [026 seconds, milliseconds, microseconds: one moment, three numbers](./notes/026-seconds-milliseconds-microseconds.md): the same count times 1000 per row, and reading the wrong unit gives January 1970
- [027 dates without times, and times without dates](./notes/027-dates-and-times-apart.md): asking for orders up to 1 April returns 0, because the date means midnight
- [028 time zones, offsets from UTC](./notes/028-time-zone-offsets.md): 09:15-04:00 and 18:45+05:30 are the same moment, and an offset is still not a time zone
- [029 daylight saving, the hour that happens twice](./notes/029-daylight-saving.md): 01:30 on 1 November 2026 in New York happens twice, an hour apart
- [030 store in UTC, show in local time](./notes/030-store-utc-show-local.md): order 102 is stored once as 22:40 UTC, and reads 18:40 in New York but 2 April in Mumbai
- [031 null, a marker for a missing value](./notes/031-null.md): Eshas city is NULL, and count(city) says 4 while count(*) says 5
- [032 null is not zero and not empty text](./notes/032-null-is-not-zero-or-empty-text.md): storing 0 stars for unrated orders makes the average 2.4 instead of 4.0
- [033 kilobytes to terabytes, how big data gets](./notes/033-kilobytes-to-terabytes.md): one order is a 35 byte line, so a million orders is 35 MB and a trillion is 35 TB
- [034 capstone, one shop order decoded down to bytes](./notes/034-capstone-one-order-decoded-to-bytes.md): order 101 is 35 bytes, and every one of them rests on a note in this section

## section 2: memory, disks and files
- [035 the processor, the part that does the work](./notes/035-the-processor.md): adding up order 101 takes 7 tiny steps, and the processor knows nothing about orders
- [036 memory vs disk, one forgets and one remembers](./notes/036-memory-vs-disk.md): order 101 survives a power cut only if it was written to disk
- [037 disk is slow, memory vs SSD vs spinning disk in real numbers](./notes/037-disk-is-slow.md): if memory took 100 seconds, an SSD would take almost two days and a spinning disk almost four months
- [038 1000 or 1024, why your drive looks smaller than the box said](./notes/038-1000-or-1024.md): a 500 GB drive reads 465 on windows, same bytes counted with a different ruler
- [039 a file is a named list of bytes](./notes/039-a-file-is-a-named-list-of-bytes.md): renaming order101.csv to .jpg changes the name and not one byte
- [040 folders and paths](./notes/040-folders-and-paths.md): two files are both called orders.csv, and only the whole path says which one
- [041 text files vs binary files](./notes/041-text-files-vs-binary-files.md): order id 101 takes 3 bytes as text and 4 as a number, and nothing in the file says which it is
- [042 line endings, the invisible characters that break files](./notes/042-line-endings.md): every row says delivered, the filter finds zero, and a hidden carriage return is why
- [043 reading start to end vs jumping to a spot](./notes/043-reading-start-to-end-vs-jumping.md): you want line 6 of a file and a jump of 14 bytes per line lands mid line
- [044 disks read in blocks, never single bytes](./notes/044-disks-read-in-blocks.md): ask for 1 byte and the disk hands over 4096, ask for 2 across a boundary and it hands over 8192
- [045 torn writes, what a half finished write leaves behind](./notes/045-torn-writes.md): a power cut mid save leaves line 6 reading 106,deliveg, new blocks glued to old ones
- [046 writing safely, write a new file then rename it](./notes/046-writing-safely.md): write order 106s update to a tmp file, rename it over the old one, and a power cut can only hit the tmp
- [047 compression, making files smaller by spotting repeats](./notes/047-compression-spotting-repeats.md): the status column stores delivered five times, and storing each run once halves it, until a run of one costs more
- [048 compression trades processor time for disk space](./notes/048-compression-trades-processor-for-space.md): 10 million bytes shrink to 18, but someone still has to build a million lines back
- [049 the terminal, running programs by typing](./notes/049-the-terminal.md): echo masala chai is a program and two arguments, and quotes make it one
- [050 processes, a program while it runs](./notes/050-processes.md): start the same program twice and you get two pids, stop one and the other keeps going
- [051 the operating system, the program that shares the machine out](./notes/051-the-operating-system.md): one processor, two jobs, and the report waits for the loader turns
- [052 the working directory, where the terminal is standing](./notes/052-the-working-directory.md): open orders.csv in python and get the wrong file, because the code never said which folder to stand in
- [053 absolute vs relative paths](./notes/053-absolute-vs-relative-paths.md): the same ../backup/orders.csv finds the right file from one folder and nothing from another
- [054 head and tail, looking at the start and end of a file](./notes/054-head-and-tail.md): a huge csv, and you only want the columns, so read the first lines and stop
- [055 wc, counting lines](./notes/055-wc-counting-lines.md): a file with 7 orders says 8 lines, and with its last row cut short of a final newline says 7
- [056 grep, finding the lines that match](./notes/056-grep-finding-matching-lines.md): grep 1 on the orders file returns all 7 orders, because it matches text anywhere, not a column
- [057 standard input and output, how programs pass text along](./notes/057-standard-input-and-output.md): wc -l with a file name prints it, wc -l < file doesnt, because the program never saw a name
- [058 pipes, chaining small programs together](./notes/058-pipes.md): grep delivered orders.csv | wc -l prints 5 with no file in between, and swapping the order prints nothing
- [059 redirecting output into a file](./notes/059-redirecting-output-into-a-file.md): grep delivered orders.csv > orders.csv leaves orders.csv empty, because the shell empties it first
- [060 capstone, the life of one saved order, memory to disk and back](./notes/060-capstone-the-life-of-one-saved-order.md): one pending order, seven stages from memory to a grep and wc count of 5

## section 3: giving data a shape

- [061 structure, why a pile of text is hard to ask questions of](./notes/061-structure-why-text-is-hard-to-ask.md): three messages about dhokla give a total of 3, fixed-position rows give the real 6
- [062 CSV, rows and columns separated by commas](./notes/062-csv-rows-and-columns-separated-by-commas.md): adding two order ids read from a csv gives 101102, because every value arrives as text
- [063 quoting, commas inside values](./notes/063-quoting-commas-inside-values.md): a note with a comma in it splits into 3 values by hand and 2 with a csv reader, because quotes fence it
- [064 quotes inside quotes, and newlines inside values](./notes/064-quotes-inside-quotes-and-newlines-inside-values.md): 3 orders in a csv and wc -l says 4, because one message has a newline inside its quotes
- [065 the header row, naming the columns](./notes/065-the-header-row-naming-the-columns.md): the same 3 orders with status in a different column count 2 delivered by name and 0 by position
- [066 JSON, records with names on every value](./notes/066-json-records-with-names-on-every-value.md): the same order with its names in two different orders reads back as one identical dictionary
- [067 JSON types, strings, numbers, booleans, null, objects and arrays](./notes/067-json-types.md): one order record holds all six JSON kinds, and python reads true as True and null as None
- [068 nesting, records and lists inside records](./notes/068-nesting.md): masala chai sits three steps down in order 103, and items 2 exists for order 105 but not 103
- [069 JSON lines, one record per line](./notes/069-json-lines.md): a save cut off halfway reads 0 of 3 orders as one array and 2 of 3 as one record per line
- [070 flattening nested objects into columns](./notes/070-flattening-nested-objects-into-columns.md): address.city becomes address_city, and a header built from the first record refuses the next one
- [071 exploding lists into many rows](./notes/071-exploding-lists-into-many-rows.md): 2 orders become 4 rows, and order 105 shows up 3 times
- [072 XML, the older cousin you will still meet](./notes/072-xml.md): the same order needs every name written twice, and a list is just the same tag repeated
- [073 YAML, indentation as structure](./notes/073-yaml.md): the same order drops every bracket and closing tag, and a list item ends when a line steps back out
- [074 YAML traps, when no means false](./notes/074-yaml-traps.md): gift_wrap: no comes back as False, and quotes turn it back into text
- [075 schema, the agreement about shape](./notes/075-schema.md): order 104 renamed status to state, the file is still valid JSON, and the schema catches it
- [076 data types in a schema](./notes/076-data-types-in-a-schema.md): a quantity of "3" in quotes passes the names check, and doubling it gives 33
- [077 required vs optional fields](./notes/077-required-vs-optional-fields.md): Esha has no city and is still a valid customer, but a missing name and a null are not the same thing
- [078 capstone, the shop orders as raw text, CSV and JSON side by side](./notes/078-capstone-the-shop-orders-three-ways.md): order 103 as a sentence, 2 csv rows and 1 JSON record, and the fix behind each step

## section 4: tables, keys and relationships
- [079 a table, rows are records, columns are fields](./notes/079-a-table-rows-are-records-columns-are-fields.md): Esha has no city, and a table row still has a city spot, holding NULL
- [080 every column holds one type](./notes/080-every-column-holds-one-type.md): Eshas city is NULL and the column is still text, and a price column refuses the word free
- [081 why a shared spreadsheet breaks when many people use it](./notes/081-why-a-shared-spreadsheet-breaks.md): Asha and Bhavin each fix one row of the same file, both save, and 106 is pending again
- [082 a database, a program that guards your data](./notes/082-a-database-guards-the-data.md): what if nobody could save the file at all, and both Asha and Bhavins fixes survive
- [083 schema on write vs schema on read](./notes/083-schema-on-write-vs-schema-on-read.md): a quantity of "two" is rejected at the door by one and crashes the reader in the other
- [084 a network, computers sending bytes to each other](./notes/084-a-network.md): Asha taps a button and the database is on another machine, so what physically crosses
- [085 addresses and ports, the right program on the right machine](./notes/085-addresses-and-ports.md): the bytes reached the server, but a dozen programs live there, so who gets them
- [086 client and server, you ask, the database answers](./notes/086-client-and-server.md): the server listens first and the client always knocks first, and Ashas phone and Bhavins phone are two clients of one program
- [087 primary key, one unique id per row](./notes/087-primary-key.md): a second Chirag signs up with id 3 and the database just says no
- [088 natural keys vs made up ids](./notes/088-natural-keys-vs-made-up-ids.md): Asha changes her email and 3 orders keyed by it point at nobody, while the id still finds all 3
- [089 update anomalies](./notes/089-update-anomalies.md): Ashas city is fixed on order 101 only, and the shop now says she lives in 2 places
- [090 insert and delete anomalies](./notes/090-insert-and-delete-anomalies.md): cancel Chirags only order and the shop forgets him, while Esha cant be stored at all
- [091 splitting into tables, each fact lives in one place](./notes/091-splitting-into-tables.md): the city is written 7 times in the wide table and 4 times after the split, and Ashas 3 orders just hold a 1
- [092 relationships, one customer, many orders](./notes/092-relationships-one-customer-many-orders.md): Asha has 3 orders and is still 1 customer, and Esha has 0 and still fits the same shape
- [093 foreign key](./notes/093-foreign-key.md): order 104 holds a 3, and the foreign key is what makes that 3 mean Chirag
- [094 what a foreign key stops, rows pointing at nothing](./notes/094-what-a-foreign-key-stops.md): an order for customer 9 is refused, and so is deleting Chirag while order 104 points at him
- [095 composite keys, a key made of two columns](./notes/095-composite-keys.md): order_items has no id column, and the pair of order and product is what must never repeat
- [096 why many to many cant live in either table](./notes/096-why-many-to-many-cant-live-in-either-table.md): order 101 has 2 products and dhokla is on 3 orders, so a pointer column on either side runs out of room
- [097 junction tables, the table in the middle](./notes/097-junction-tables.md): order_items holds one row per order and product pair, with the quantity sitting on the pair
- [098 entity relationship diagrams, boxes and lines](./notes/098-entity-relationship-diagrams.md): one box per table and one line per foreign key, and not a single row of data in the picture
- [099 crows feet, reading one and many on the lines](./notes/099-crows-feet-reading-one-and-many.md): the marks on a line end say how many rows match, and the circle is the zero
- [100 capstone, the whole shop as four connected tables](./notes/100-capstone-the-whole-shop-as-four-connected-tables.md): customers, orders, order_items and products in one picture, 5, 7, 13 and 6 rows, and the fix behind each step

## section 5: asking questions with SQL

- [101 SQL, you describe the result, the database figures out how](./notes/101-sql-you-describe-the-result.md): the python loop says how to find Jersey City customers, the SQL only says which, and the database picks the steps
- [102 a database in one file, setting up DuckDB](./notes/102-a-database-in-one-file.md): DuckDB runs inside your program and keeps everything in a single file you connect to by path
- [103 your first query against the shop](./notes/103-your-first-query-against-the-shop.md): the shop loads into a DuckDB file by running its SQL text, and SELECT name, price FROM products returns six rows
- [104 SELECT and FROM, picking columns](./notes/104-select-and-from-picking-columns.md): FROM names the table, SELECT picks columns in the order you write them, and rows never drop, so SELECT category repeats snack three times
- [105 SELECT star, every column, and why you rarely want it](./notes/105-select-star-every-column.md): a label that printed snack one day and 6.00 the next, with no error, because of one star
- [106 WHERE, keeping only the rows that match](./notes/106-where-keeping-only-the-rows-that-match.md): you can filter on a column you never select, and a capital D typo returns zero rows with no error
- [107 comparisons, equal, not equal, bigger, smaller](./notes/107-comparisons-equal-not-equal-bigger-smaller.md): price >= 6 keeps dhokla at exactly 6.00 and price > 6 drops it, with no error
- [108 AND and OR, combining two tests](./notes/108-and-or-combining-two-tests.md): asking for snacks and sweets with AND returns zero rows, because one row has one category and english and means OR
- [109 parentheses, and AND runs before OR](./notes/109-parentheses-and-runs-before-or.md): asking for snacks or sweets under 6 returns khandvi at 7.50, because AND goes first and parentheses fix it
- [110 NOT, flipping a condition](./notes/110-not-flipping-a-condition.md): NOT city = 'Jersey City' returns 2 customers not 3, because Eshas null city makes the test unknown and NOT unknown is still unknown
- [111 IN, matching against a list](./notes/111-in-matching-against-a-list.md): IN is the OR chain written once, and NOT IN with a NULL in the list returns zero rows
- [112 BETWEEN, ranges that include both ends](./notes/112-between-ranges-that-include-both-ends.md): BETWEEN keeps both ends so dhokla at 6.00 and fafda at 4.50 are in, and a date as the high end of a timestamp range drops the last day
- [113 LIKE, matching text patterns](./notes/113-like-matching-text-patterns.md): LIKE 'k%' finds khandvi and kaju katli, and a capital K returns zero rows with no error
- [114 three valued logic, true, false and unknown](./notes/114-three-valued-logic-true-false-and-unknown.md): Esha has no city, so a test on it is unknown, and a false settles an AND while a true settles an OR
- [115 IS NULL and IS NOT NULL](./notes/115-is-null-and-is-not-null.md): city = NULL returns zero rows even for Esha, while IS NULL finds her and IS NOT NULL returns the other 4
- [116 COALESCE, a fallback when a value is NULL](./notes/116-coalesce-a-fallback-when-a-value-is-null.md): COALESCE returns the first non-null value so Eshas city shows unknown, and filling stars with 0 drops the average from 4.0 to 2.4
- [117 ORDER BY, sorting by one or more columns](./notes/117-order-by-sorting-by-one-or-more-columns.md): ORDER BY category, price DESC groups the menu by category and puts the priciest first only inside each, so kaju katli at 12.00 sits fifth
- [118 no ORDER BY, no promised order](./notes/118-no-order-by-no-promised-order.md): a query with no ORDER BY may return rows in any order, and rows tied on the sort column have no promised order either
- [119 where NULLs land when you sort](./notes/119-where-nulls-land-when-you-sort.md): DuckDB puts nulls last even on DESC, Postgres treats null as biggest so DESC puts them first, and NULLS FIRST or NULLS LAST settles it
- [120 LIMIT and OFFSET, paging through rows](./notes/120-limit-and-offset-paging-through-rows.md): LIMIT 2 OFFSET 2 on the menu by price gives page 2, dhokla and jalebi, and it only means something with ORDER BY
- [121 DISTINCT, removing duplicate rows](./notes/121-distinct-removing-duplicate-rows.md): SELECT DISTINCT category turns 6 rows into 3, and DISTINCT on customer and status turns 7 rows into 5 because it compares the whole row
- [122 computed columns and AS](./notes/122-computed-columns-and-as.md): SELECT name, price - 1 AS sale_price builds a new column per row without touching the table, and DuckDB lets WHERE use it where Postgres doesnt
- [123 CASE WHEN, if and else inside a query](./notes/123-case-when-if-and-else-inside-a-query.md): CASE WHEN price < 5 THEN 'cheap' labels each product per row, the first true test wins, and with no ELSE a row that matches nothing gets null
- [124 text functions, lower, upper, length and trim](./notes/124-text-functions-lower-upper-length-and-trim.md): a trailing space makes WHERE typed_name = 'CHIRAG' find nothing, length shows it, and lower(trim(...)) cleans it in the result
- [125 concatenating text, and taking pieces of it](./notes/125-concatenating-text-and-taking-pieces-of-it.md): gluing name and city gives NULL for Esha because one null piece nulls the whole label, and substr counts from 1 where python counts from 0
- [126 date parts, pulling out the year, month and day](./notes/126-date-parts-pulling-out-the-year-month-and-day.md): extract(month FROM ordered_at) gives the number 4 not April, WHERE can filter on it, and month alone forgets the year
- [127 truncating timestamps to a day or a month](./notes/127-truncating-timestamps-to-a-day-or-a-month.md): date_trunc('month', x) chops a timestamp to the first of its month and keeps the year, but the result is still a timestamp, so a plain date only matches at midnight
- [128 adding and subtracting intervals](./notes/128-adding-and-subtracting-intervals.md): ordered_at + INTERVAL 2 DAY moves a timestamp and keeps the clock, and 1 month is not 30 days, so Jan 31 plus 1 month lands on Feb 28
- [129 the difference between two dates](./notes/129-the-difference-between-two-dates.md): 102 to 103 is 1 day and 17 hours apart, and date_diff still says 2
- [130 NULLIF and dividing by zero](./notes/130-nullif-and-dividing-by-zero.md): NULLIF(placed, 0) turns a zero into NULL so a rate comes out NULL, while a raw 0 / 0 gives nan in DuckDB and one nan wrecks avg
- [131 integer division, when 7 / 2 gives 3](./notes/131-integer-division-when-7-divided-by-2-gives-3.md): DuckDB / gives 3.5 and // gives 3, while Postgres makes / on two integers drop the fraction
- [132 CAST, changing a values type](./notes/132-cast-changing-a-values-type.md): CAST(7.50 AS INTEGER) gives 8 in DuckDB, not pythons 7, and the text '9' sorts after '10' until you cast it
- [133 casts that fail, and TRY_CAST](./notes/133-casts-that-fail-and-try-cast.md): CAST on n/a kills the whole query, TRY_CAST returns null instead, and 12,00 with a comma quietly becomes null too
- [134 the order SQL really runs in](./notes/134-the-order-sql-really-runs-in.md): a query runs FROM, WHERE, SELECT, ORDER BY, LIMIT, so an AS name works in ORDER BY but not in a Postgres WHERE
- [135 one language, many dialects](./notes/135-one-language-many-dialects.md): the first 2 rows is FETCH FIRST in the standard, LIMIT in Postgres and DuckDB, TOP in SQL Server
- [136 capstone, one query traced clause by clause](./notes/136-capstone-one-query-traced-clause-by-clause.md): one query with 5 clauses, and the rows left after each one, with every note of the section on the map

## section 6: summarizing data

- [137 aggregate functions, many rows in, one value out](./notes/137-aggregate-functions-many-rows-in-one-value-out.md): count, sum and max turn 13 order_items rows into one row, and summing zero rows gives NULL, not 0
- [138 COUNT star vs COUNT of a column](./notes/138-count-star-vs-count-of-a-column.md): count(*) counts rows, count(stars) skips the nulls, so the same 5 ratings give 5 or 3
- [139 COUNT DISTINCT, counting different values](./notes/139-count-distinct-counting-different-values.md): 7 orders but count(DISTINCT customer_id) is 4, and unlike SELECT DISTINCT it skips nulls
- [140 SUM and AVG, adding up and averaging](./notes/140-sum-and-avg-adding-up-and-averaging.md): the 6 product prices sum to 38.00 and average 6.33, a price no product has, because avg is just sum over count
- [141 what NULLs do to SUM and AVG](./notes/141-what-nulls-do-to-sum-and-avg.md): sum and avg skip null rows, so avg divides by 3 not 5, and all null gives NULL
- [142 MIN and MAX, the smallest and biggest value](./notes/142-min-and-max-the-smallest-and-biggest-value.md): max(price) returns 12.00 but not the product, for that you sort and take one row
- [143 GROUP BY, one group per value](./notes/143-group-by-one-group-per-value.md): 6 products become 3 rows, one per category, and a null city gets its own group
- [144 grouping by more than one column](./notes/144-grouping-by-more-than-one-column.md): 7 orders become 5 groups by customer and status, and combinations that dont exist get no row, not a zero
- [145 the GROUP BY rule, every column is grouped or aggregated](./notes/145-the-group-by-rule-every-column-is-grouped-or-aggregated.md): selecting status while grouping by customer errors because Ashas group holds three statuses, so every SELECT column must be grouped or aggregated
- [146 HAVING, filtering whole groups](./notes/146-having-filtering-whole-groups.md): HAVING count(*) >= 2 keeps customers 1 and 2 of the 4 groups, and it can test an aggregate you never SELECT
- [147 WHERE vs HAVING, before grouping or after](./notes/147-where-vs-having-before-grouping-or-after.md): WHERE count(*) errors because no count exists before grouping, and WHERE status = 'delivered' makes Asha count 2, not 3
- [148 conditional aggregation, counting several things in one pass](./notes/148-conditional-aggregation-counting-several-things-in-one-pass.md): sum(CASE WHEN ...) gives total, delivered and pending per customer in one query, and count(CASE ... ELSE 0) wrongly counts all 7 rows
- [149 median, the middle value after sorting](./notes/149-median-the-middle-value-after-sorting.md): the 6 prices have median 5.50 against an avg of 6.33, because an even count averages the two middles
- [150 percentiles, the medians cousins](./notes/150-percentiles-the-medians-cousins.md): the 90th percentile of the 6 prices is 9.75, halfway between 7.50 and 12.00, a position and not 90% of the max
- [151 pivoting, turning rows into columns](./notes/151-pivoting-turning-rows-into-columns.md): one sum(CASE ...) per status turns 5 long rows into one row per customer, and a status you forget to type silently disappears
- [152 ROLLUP, subtotals and grand totals](./notes/152-rollup-subtotals-and-grand-totals.md): ROLLUP (customer_id, status) turns 5 groups into 10 rows, with Asha at 3 and the shop at 7 as NULL rows
- [153 the full run order with GROUP BY and HAVING](./notes/153-the-full-run-order-with-group-by-and-having.md): WHERE, GROUP BY, HAVING, then SELECT, ORDER BY and LIMIT, so LIMIT counts groups
- [154 capstone, orders per customer traced from rows to groups](./notes/154-capstone-orders-per-customer-traced-from-rows-to-groups.md): 7 orders become 4 customer lines, and Esha gets none because a group is built from rows

## section 7: combining tables with joins

- [155 why joins, the answer lives in more than one table](./notes/155-why-joins-the-answer-lives-in-more-than-one-table.md): the city of order 104 lives in customers, and a join is a loop inside a loop that pairs 7 orders with their 7 customers
- [156 inner join traced by hand](./notes/156-inner-join-traced-by-hand.md): 7 orders and 5 customers make 35 pairs, only 7 survive, and Esha never shows up
- [157 ON, how a join decides which rows match](./notes/157-on-how-a-join-decides-which-rows-match.md): the same join keeps 7 pairs on an id match, 4 with a city test added, and all 35 when ON is true
- [158 table aliases, short nicknames for tables](./notes/158-table-aliases-short-nicknames-for-tables.md): a nickname like o for orders shrinks the ON line, and the full name stops working in that query
- [159 left join, keep every row from the left table](./notes/159-left-join-keep-every-row-from-the-left-table.md): a left join keeps Esha with a NULL order, 8 rows where the inner join gave 7
- [160 the nulls a left join creates](./notes/160-the-nulls-a-left-join-creates.md): count(*) says Esha placed 1 order, count(o.order_id) says 0
- [161 a WHERE that quietly turns a left join into an inner join](./notes/161-a-where-that-quietly-turns-a-left-join-into-an-inner-join.md): a WHERE on the orders side drops Esha and Chirag, 5 rows, while the same test in ON keeps all 7
- [162 right and full outer joins](./notes/162-right-and-full-outer-joins.md): a full join of customers and signups gives 7 rows, 5 plus 4 minus 2 matches, and the stray spaces leave Bhavin and Chirag alone on both sides
- [163 joining three tables](./notes/163-joining-three-tables.md): orders, order_items and products chain as two joins in a row, each ON only sees tables written above it, and the chain gives 13 rows
- [164 fan out, when a join multiplies rows](./notes/164-fan-out-when-a-join-multiplies-rows.md): joining 7 orders to their items gives 13 rows, because an order with 3 items is kept 3 times
- [165 double counting, why sums after a fan out lie](./notes/165-double-counting-why-sums-after-a-fan-out-lie.md): 7 delivery fees add to 15.00, but summed after joining to order_items they give 31.00, and sum(DISTINCT) gives 5.00
- [166 joining on columns that can be NULL](./notes/166-joining-on-columns-that-can-be-null.md): NULL never matches NULL in a join, so Esha drops out of an inner join on city (4 rows), and IS NOT DISTINCT FROM brings her back (5 rows)
- [167 anti join, rows with no match](./notes/167-anti-join-rows-with-no-match.md): a left join plus WHERE the right primary key IS NULL finds Esha, the only customer with no orders, and fafda, the only product never ordered
- [168 self join, a table joined to itself](./notes/168-self-join-a-table-joined-to-itself.md): joining customers to customers on city gives 6 pairs, 4 of them a person with herself, and a.customer_id < b.customer_id leaves Asha and Chirag
- [169 cross join, every row with every row](./notes/169-cross-join-every-row-with-every-row.md): 5 customers crossed with 6 products give 30 pairs, the loop inside a loop with no if, and only 10 of those pairs were ever ordered
- [170 joining on a range, matching a date to a period](./notes/170-joining-on-a-range-matching-a-date-to-a-period.md): a BETWEEN join drops order 103 because a timestamp at noon is after a date end at midnight, and a CAST to date fixes it
- [171 joins plus GROUP BY, revenue per customer](./notes/171-joins-plus-group-by-revenue-per-customer.md): the joins run first and GROUP BY sums quantity times price, Asha is 43.50, Esha drops out, and Chirag still shows 18.00 for a cancelled order until a WHERE removes it
- [172 practice, five join questions on the shop, checking row counts](./notes/172-practice-five-join-questions-on-the-shop-checking-row-counts.md): five tasks on predicting the row count of a join before running it, from 14 rows for two left joins to 5 sweet items bought by only 2 customers
- [173 capstone, the shop revenue report from four tables](./notes/173-capstone-the-shop-revenue-report-from-four-tables.md): four left joins and a GROUP BY put all 5 customers on one report with 93.50 delivered revenue, and the 33.00 gap to 126.50 is cancelled and pending orders

## section 8: bigger queries

- [174 subquery in WHERE](./notes/174-subquery-in-where.md): the inner SELECT runs first and hands IN a list, delivered customer ids 1, 2, 1, 4, 2 keep Asha, Bhavin and Disha once each, where a join gives 5 rows
- [175 subquery in FROM](./notes/175-subquery-in-from.md): avg(count(*)) errors, but grouping in an inner query first gives 4 rows and an average of 1.75, and Esha has no group so she is left out
- [176 scalar subqueries, one value inside a query](./notes/176-scalar-subqueries-one-value-inside-a-query.md): a subquery that returns one row and one column works like a number, so price > (SELECT avg(price) ...) keeps khandvi and kaju katli, and zero inner rows quietly gives an empty result
- [177 correlated subqueries, a query that depends on the outer row](./notes/177-correlated-subqueries-a-query-that-depends-on-the-outer-row.md): the inner query uses a column of the outer row, so cheaper than its own category average keeps 2 products where the shop wide average keeps 4
- [178 EXISTS and NOT EXISTS, asking whether a matching row exists](./notes/178-exists-and-not-exists-asking-whether-a-matching-row-exists.md): EXISTS only asks whether the inner query found a row, so Asha with 2 delivered orders shows once, and NOT EXISTS gives Chirag (cancelled only) and Esha
- [179 NOT IN and the NULL trap](./notes/179-not-in-and-the-null-trap.md): city NOT IN a list that includes a NULL returns zero rows, while NOT EXISTS gives Bhavin and Esha
- [180 CTEs, naming each step with WITH](./notes/180-ctes-naming-each-step-with-with.md): the 175 inner query moved to the top and named per_customer, so it is used twice, as a table and inside an average, and gives Asha and Bhavin
- [181 views, a saved query with a name](./notes/181-views-a-saved-query-with-a-name.md): a view stores the query, not rows, so the delivered count went 5 to 6 after one order update without touching the view
- [182 UNION and UNION ALL](./notes/182-union-and-union-all.md): stacking delivered and not delivered customer ids gives 7 rows with UNION ALL and 4 with UNION
- [183 INTERSECT and EXCEPT](./notes/183-intersect-and-except.md): delivered ids against the rest give Asha for INTERSECT, Bhavin and Disha for EXCEPT, and Chirag when the sides swap
- [184 window functions, a total next to every row](./notes/184-window-functions-a-total-next-to-every-row.md): every product keeps its row and gets the 38.00 total beside it
- [185 OVER, the window a function looks through](./notes/185-over-the-window-a-function-looks-through.md): every product gets its own window, so price minus the average gives dhokla -0.33 and kaju katli 5.67
- [186 PARTITION BY, a separate window per group](./notes/186-partition-by-a-separate-window-per-group.md): average price per category gives snacks 6.00, sweets 8.50 and masala chai its own 3.00, with all 6 rows kept
- [187 ROW_NUMBER, numbering rows in order](./notes/187-row-number-numbering-rows-in-order.md): products numbered by price come out as kaju katli 1 and dhokla 3 while the rows stay in id order
- [188 RANK vs DENSE_RANK, what ties do](./notes/188-rank-vs-dense-rank-what-ties-do.md): two tied rows both get 1, then RANK jumps to 3 and DENSE_RANK goes to 2
- [189 running totals](./notes/189-running-totals.md): daily orders placed 2, 0, 1, 1, 0, 1, 0, 1, 1 add up to a running 2, 2, 3, 4, 4, 5, 5, 6, 7
- [190 window frames, ROWS BETWEEN](./notes/190-window-frames-rows-between.md): one day of orders is jumpy, so add up just the last 3 rows on every row
- [191 the default frame trap](./notes/191-the-default-frame-trap.md): add an ORDER BY inside OVER and max quietly becomes a running max
- [192 LAG and LEAD, looking at the row before](./notes/192-lag-and-lead-looking-at-the-row-before.md): the day before's orders pushed down one row, with NULL on the first day
- [193 top N per group](./notes/193-top-n-per-group.md): the 2 priciest products per category, 5 rows, with masala chai alone in drinks
- [194 removing duplicates with ROW_NUMBER](./notes/194-removing-duplicates-with-row-number.md): DISTINCT leaves Asha twice in the city feed, so number each customers rows newest first and keep number 1
- [195 gaps and islands, date minus row number](./notes/195-gaps-and-islands-date-minus-row-number.md): which days in a row got an order, found by subtracting a counter from the date
- [196 gaps and islands, one row per streak](./notes/196-gaps-and-islands-one-row-per-streak.md): turning 6 labeled days into 4 streak rows with GROUP BY
- [197 generate_series, a column of consecutive days](./notes/197-generate-series-a-column-of-consecutive-days.md): orders has no row for april 2, 5 or 7, so make the 9 days from nothing
- [198 date spines, a left join that keeps the empty days](./notes/198-date-spines-a-left-join-that-keeps-the-empty-days.md): grouping orders by day gives 6 rows, so left join them onto 9 generated days and the empty ones read 0
- [199 session starts, flagging the click after a long gap](./notes/199-session-starts-flag-the-click-after-a-long-gap.md): a click list has no sessions in it, so flag the click that comes after a 30 minute silence
- [200 session ids, a running sum of the flags](./notes/200-session-ids-a-running-sum-of-the-flags.md): add the 0 and 1 start flags as you go and every click gets its session number
- [201 cohorts, the month each customer first showed up](./notes/201-cohorts-the-month-each-customer-first-showed-up.md): Asha logged in three months running, so her cohort is her earliest one, and counting per month without min makes 5 people add up to 7
- [202 retention, who came back the month after](./notes/202-retention-who-came-back-the-month-after.md): Asha came back the month after joining and Bhavin never did, so left join active months onto cohorts and count who matched
- [203 recursive CTEs, following a chain of rows](./notes/203-recursive-ctes-following-a-chain-of-rows.md): Asha told Bhavin, Bhavin told Disha, Disha told Esha, so a query that reads its own rows walks the whole chain round by round
- [204 arrays and UNNEST, lists inside a cell](./notes/204-arrays-and-unnest-lists-inside-a-cell.md): count the savory products when each keeps its tags in one cell, and watch the empty list vanish
- [205 querying JSON inside a column](./notes/205-querying-json-inside-a-column.md): the app logs clicks as JSON strings in one column, so ->> pulls the customer out, and a missing name quietly gives NULL
- [206 practice, ten interview style SQL questions on the shop](./notes/206-practice-ten-interview-style-sql-questions-on-the-shop.md): the shop sells 6 products but a units query shows 5, and nine more questions where the words tell you which tool to reach for
- [207 capstone, each customers first order and the days between orders](./notes/207-capstone-each-customers-first-order-and-the-days-between-orders.md): Asha ordered on april 1, 3 and 8, so one window per customer numbers each order and LAG gives the days since the one before

## section 9: changing data safely

- [208 containers, a program packed with everything it needs](./notes/208-containers-a-program-packed-with-everything-it-needs.md): a script that runs on a laptop and dies on a server needs its python and libraries packed in a box, and the one thing it still borrows is the kernel
- [209 images and containers, the packed box and the running copy](./notes/209-images-and-containers-the-packed-box-and-the-running-copy.md): edit a file in one of two containers started from the same image and the other never sees it, because the image itself never changes
- [210 running Postgres in a container on your laptop](./notes/210-running-postgres-in-a-container-on-your-laptop.md): the container says running but the app gets connection refused, because without -p nothing on the laptop is wired to the box
- [211 a database server, Postgres where most app data lives](./notes/211-a-database-server-postgres-where-most-app-data-lives.md): DuckDB lets one program write to its file, so a shop with many shoppers needs a server that alone opens the files and answers every client
- [212 connections and sessions, one conversation with the database](./notes/212-connections-and-sessions-one-conversation-with-the-database.md): Asha sets her time zone and Bhavin on the same server still sees UTC, because a setting belongs to one connection's session
- [213 CREATE TABLE, naming a table and its columns](./notes/213-create-table-naming-a-table-and-its-columns.md): CREATE TABLE IF NOT EXISTS on products raises no error and adds no column, because it only checks that the name is taken
- [214 temporary tables, a table that lives as long as your session](./notes/214-temporary-tables.md): a temp table named products hides the real one, so the shop suddenly has 3 products and nothing was deleted
- [215 NOT NULL and DEFAULT, required columns and fallback values](./notes/215-not-null-and-default-required-columns-and-fallback-values.md): Esha has no city but nobody has no name, and a default fills a column you leave out but never rescues a NULL you type
- [216 UNIQUE, no two rows may share a value](./notes/216-unique-no-two-rows-may-share-a-value.md): the second asha@example.com is refused, but two NULL emails both get in, because a missing value never equals another
- [217 CHECK, a rule every value must pass](./notes/217-check-a-rule-every-value-must-pass.md): a price of -7.50 passes NOT NULL, and a NULL price even passes CHECK (price > 0), because unknown is not false
- [218 key constraints, PRIMARY KEY and REFERENCES in CREATE TABLE](./notes/218-key-constraints-primary-key-and-references-in-create-table.md): a column called order_id is just a label, the database refuses an orphan or a repeated id only once the key rule is written down
- [219 sequences, where made up ids come from](./notes/219-sequences-where-made-up-ids-come-from.md): a failed insert still burns an id, so Chirag gets ticket 4 and ticket 3 never exists
- [220 INSERT, adding rows and matching values to columns](./notes/220-insert-adding-rows-and-matching-values-to-columns.md): swap two whole numbers in an INSERT and Disha ends up wanting jalebi, because the database only checks types, never what you meant
- [221 INSERT from a SELECT, copying rows from a query](./notes/221-insert-from-a-select-copying-rows-from-a-query.md): run the copy of delivered orders twice and 5 orders become 10 rows, because nothing remembers the first run
- [222 UPDATE, changing rows and why the WHERE matters](./notes/222-update-changing-rows-and-why-the-where-matters.md): forget one WHERE on an UPDATE and all 7 orders say cancelled, with no error and no warning
- [223 DELETE, removing rows and what still points at them](./notes/223-delete-removing-rows-and-what-still-points-at-them.md): a cancelled order wont delete while its item row still points at it, so the pointing row goes first
- [224 upsert, insert or update in one statement](./notes/224-upsert-insert-or-update-in-one-statement.md): a price list has jalebi changed and imarti new, and one INSERT with ON CONFLICT updates the first and adds the second
- [225 ALTER TABLE, adding a column to a table with rows](./notes/225-alter-table-adding-a-column-to-a-table-with-rows.md): the shop adds a vegan flag to a menu that already has rows, and every old row quietly reads NULL
- [226 DROP and TRUNCATE, emptying a table vs removing it](./notes/226-drop-and-truncate-emptying-a-table-vs-removing-it.md): DELETE, TRUNCATE and DROP all get rid of the menu rows, but only DROP takes the table with them
- [227 transactions, all or nothing](./notes/227-transactions-all-or-nothing.md): an order row goes in, its item row breaks a foreign key, and the shop is left with an order holding nothing
- [228 COMMIT and ROLLBACK, keeping or undoing a transaction](./notes/228-commit-and-rollback-keeping-or-undoing-a-transaction.md): insert an order, count it, type ROLLBACK, and both rows are gone together
- [229 ACID, four promises a database makes](./notes/229-acid-four-promises-a-database-makes.md): a power cut, two shoppers at once, a price of -5 and a crash after saving each break a different promise
- [230 ACID consistency, the rules still hold after every change](./notes/230-acid-consistency-the-rules-still-hold-after-every-change.md): one good price change and one bad one share a transaction and both vanish, while an order with no items sails through
- [231 isolation, two people at the same time](./notes/231-isolation-two-people-at-the-same-time.md): Esha is mid order and Asha counts at that moment, she sees the last finished picture and nobody waits
- [232 durability, surviving a crash](./notes/232-durability-surviving-a-crash.md): Esha is told her order is saved and the power dies, so what the database did before saying saved decides if 108 survives
- [233 the write ahead log, write down the plan before the change](./notes/233-the-write-ahead-log-write-down-the-plan-before-the-change.md): Esha is told done while the table file on disk still lacks 108, and thats on purpose
- [234 replaying the log after a crash](./notes/234-replaying-the-log-after-a-crash.md): the server restarts with the table file behind, and redoing the whole log would put order 108 in twice
- [235 lost updates](./notes/235-lost-updates.md): 10 dhokla left, two buyers each take one, and the stock says 9 with no error
- [236 dirty reads](./notes/236-dirty-reads.md): Esha rolls back a typo price, but Asha already read it, a price that never existed
- [237 non repeatable reads](./notes/237-non-repeatable-reads.md): Asha reads dhokla twice in one transaction and gets 6.00 then 7.00, and nothing was rolled back
- [238 phantoms](./notes/238-phantoms.md): Asha lists the pending orders twice in one transaction and gets one row, then two, and none of the rows she read changed
- [239 isolation levels, read committed](./notes/239-isolation-levels-read-committed.md): Asha types BEGIN and Esha commits 108 right after, so does ashas first query see it
