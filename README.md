# data engineering notes

learning data engineering from the very bottom, one concept at a time, in public. starts at what a bit is and ends at designing data platforms. every note is a 2 minute read, every note links to the ones it builds on, and every example uses the same small imaginary snack shop so you always know the data.

start here: [001 data is facts written down](./notes/001-data-is-facts-and-numbers.md)

notes so far: 119

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
