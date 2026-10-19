# glossary

every term these notes have built, in plain words, with the note that built it. if a note uses a term, its in here first.

| term | plain meaning | built in |
|---|---|---|
| absolute path | a path starting with a slash, always begun at the root | [053](./notes/053-absolute-vs-relative-paths.md) |
| address (network) | a number naming one machine on a network, 4 bytes in IPv4 | [085](./notes/085-addresses-and-ports.md) |
| ambiguous time | a clock reading that happens twice, when clocks go back | [029](./notes/029-daylight-saving.md) |
| argument | a word after the program name, handed to that program | [049](./notes/049-the-terminal.md) |
| ASCII | the old table giving 128 characters a number, English only | [008](./notes/008-ascii-runs-out.md) |
| atomic | happening whole or not at all, never half done | [046](./notes/046-writing-safely.md) |
| binary | counting with only 0 and 1, each place worth double | [003](./notes/003-counting-in-binary.md) |
| binary file | a file whose bytes are not characters, like packed numbers | [041](./notes/041-text-files-vs-binary-files.md) |
| binary fraction | binary carried past the point, places worth a half, quarter, eighth | [017](./notes/017-fractions-in-binary.md) |
| binary point | the dot in a binary number, places to its right halve | [017](./notes/017-fractions-in-binary.md) |
| bit | one tiny switch inside a computer, written as 0 or 1 | [002](./notes/002-bits.md) |
| block | a fixed chunk of bytes, often 4096, a disk reads at once | [044](./notes/044-disks-read-in-blocks.md) |
| boolean | a value with only two states, true or false | [023](./notes/023-true-and-false-the-boolean.md) |
| byte | a group of 8 bits, holding 256 possible values | [004](./notes/004-bytes.md) |
| byte in hex | a byte is always exactly two hex digits, 00 to ff | [006](./notes/006-one-byte-two-hex-digits.md) |
| carriage return | the 0d character, which sent a typewriter carriage back | [042](./notes/042-line-endings.md) |
| character | one letter, digit, space or symbol, stored as one number | [007](./notes/007-text-is-numbers.md) |
| client | a program that sends a request and waits for the answer | [086](./notes/086-client-and-server.md) |
| code point | the number Unicode gives one character, written like U+0AA2 | [009](./notes/009-unicode.md) |
| column | a fixed position in every row, like position 3 for status | [062](./notes/062-csv-rows-and-columns-separated-by-commas.md) |
| column type | one data type chosen for a whole column, every value fits it | [080](./notes/080-every-column-holds-one-type.md) |
| combining mark | a code point with no letter, drawn on the letter before it | [012](./notes/012-combining-marks.md) |
| compression | storing the same information in fewer bytes, rebuildable exactly | [047](./notes/047-compression-spotting-repeats.md) |
| continuation byte | a UTF-8 byte starting 10, continuing the previous characters bytes | [011](./notes/011-why-gujarati-takes-3-bytes.md) |
| core | one full processor inside a chip, most chips hold several | [035](./notes/035-the-processor.md) |
| CRLF | a line ending of two characters, 0d then 0a, common on windows | [042](./notes/042-line-endings.md) |
| CSV | a text file, usually one row per line, values split by commas | [062](./notes/062-csv-rows-and-columns-separated-by-commas.md) |
| data | facts written down so you can ask questions about them later | [001](./notes/001-data-is-facts-and-numbers.md) |
| data type | the kind of value a field allows, like text or number | [076](./notes/076-data-types-in-a-schema.md) |
| database | a program that owns the data files, changing them only on request | [082](./notes/082-a-database-guards-the-data.md) |
| date | a calendar day with no time of day | [027](./notes/027-dates-and-times-apart.md) |
| daylight saving | clocks shifting an hour twice a year in many places | [024](./notes/024-utc.md) |
| decompress | rebuild the original bytes from compressed ones, costing processor work | [048](./notes/048-compression-trades-processor-for-space.md) |
| disk | storage like an SSD or hard drive, keeping bytes without power | [036](./notes/036-memory-vs-disk.md) |
| doubled quote | two quotes in a row inside a quoted value, meaning one quote | [064](./notes/064-quotes-inside-quotes-and-newlines-inside-values.md) |
| embedded newline | a line ending inside a quoted csv value, not ending the row | [064](./notes/064-quotes-inside-quotes-and-newlines-inside-values.md) |
| epoch | the starting line, 1 January 1970 UTC, that unix time counts from | [025](./notes/025-unix-time.md) |
| exact decimal | a type keeping decimal digits exactly, like DECIMAL(6, 2) | [022](./notes/022-exact-decimal-types.md) |
| exact tie | an answer halfway between two floats, rounded to the one ending 0 | [020](./notes/020-why-0-1-plus-0-2-is-not-0-3.md) |
| explode | turning a record holding a list into one row per list item | [071](./notes/071-exploding-lists-into-many-rows.md) |
| field | one fact every row has a spot for, like city | [079](./notes/079-a-table-rows-are-records-columns-are-fields.md) |
| file | a name plus a list of bytes in order, kept on disk | [039](./notes/039-a-file-is-a-named-list-of-bytes.md) |
| file extension | the letters after the dot in a name, just a label | [039](./notes/039-a-file-is-a-named-list-of-bytes.md) |
| flattening | turning inner names into columns, like address_city, one per name | [070](./notes/070-flattening-nested-objects-into-columns.md) |
| float | binary digits plus a count of how far to slide the point | [019](./notes/019-floating-point.md) |
| folder | a named place on disk holding files and other folders | [040](./notes/040-folders-and-paths.md) |
| gibibyte | 1024 x 1024 x 1024 bytes, written GiB | [038](./notes/038-1000-or-1024.md) |
| gigabyte | 1000 megabytes, a billion bytes, written GB | [033](./notes/033-kilobytes-to-terabytes.md) |
| grapheme | one unit as seen on screen, possibly several code points | [012](./notes/012-combining-marks.md) |
| grep | prints every line containing the given pattern, anywhere in the line | [056](./notes/056-grep-finding-matching-lines.md) |
| head | prints the first lines of a file, 10 unless -n says otherwise | [054](./notes/054-head-and-tail.md) |
| header row | the first line of a csv, holding column names instead of data | [065](./notes/065-the-header-row-naming-the-columns.md) |
| hexadecimal | counting with sixteen digits, a to f standing for ten to fifteen | [005](./notes/005-hexadecimal.md) |
| integer size | how many bits a whole number gets, which sets its range | [015](./notes/015-integer-sizes.md) |
| JSON | a text format of records, with a name next to every value | [066](./notes/066-json-records-with-names-on-every-value.md) |
| JSON array | square brackets around values in order, like a python list | [067](./notes/067-json-types.md) |
| JSON lines | a text file with one whole JSON record per line | [069](./notes/069-json-lines.md) |
| JSON object | curly braces around name: value pairs, like a dictionary | [067](./notes/067-json-types.md) |
| JSON types | the six kinds of value: string, number, boolean, null, object, array | [067](./notes/067-json-types.md) |
| jump | asking for a file position directly, called seek in python | [043](./notes/043-reading-start-to-end-vs-jumping.md) |
| kibibyte | 1024 bytes, the unambiguous 1024 based unit, written KiB | [038](./notes/038-1000-or-1024.md) |
| kilobyte | 1000 bytes, written KB | [033](./notes/033-kilobytes-to-terabytes.md) |
| LF | a one character line ending, 0a, common on linux and mac | [042](./notes/042-line-endings.md) |
| line ending | the characters marking where one line stops, the next starts | [042](./notes/042-line-endings.md) |
| lookup | fetching one value from a random spot | [037](./notes/037-disk-is-slow.md) |
| lost update | two saves of one file, the later one erases the earlier change | [081](./notes/081-why-a-shared-spreadsheet-breaks.md) |
| made up id | a number handed out by the database, meaningless outside it | [088](./notes/088-natural-keys-vs-made-up-ids.md) |
| megabyte | 1000 kilobytes, a million bytes, written MB | [033](./notes/033-kilobytes-to-terabytes.md) |
| memory | the computers working space (RAM), emptied when the power goes off | [036](./notes/036-memory-vs-disk.md) |
| microsecond | a millionth of a second | [026](./notes/026-seconds-milliseconds-microseconds.md) |
| millisecond | a thousandth of a second | [026](./notes/026-seconds-milliseconds-microseconds.md) |
| nanosecond | a billionth of a second | [037](./notes/037-disk-is-slow.md) |
| natural key | a real world value that already tells rows apart, like an email | [088](./notes/088-natural-keys-vs-made-up-ids.md) |
| negative zero | a second zero pattern, with the sign bit set | [013](./notes/013-negative-numbers-sign-bit.md) |
| nesting | an object or array sitting inside another one, as deep as needed | [068](./notes/068-nesting.md) |
| network | a way to move bytes from one computer to another | [084](./notes/084-a-network.md) |
| null | a marker meaning there is no value here, not a value | [031](./notes/031-null.md) |
| offset | how far a clock sits ahead of or behind UTC, like +05:30 | [028](./notes/028-time-zone-offsets.md) |
| operating system | the program that starts programs and shares the machine between them | [051](./notes/051-the-operating-system.md) |
| optional field | a field a record may leave out without being rejected | [077](./notes/077-required-vs-optional-fields.md) |
| overflow | a result too big for its bit size, wrapping or erroring | [016](./notes/016-overflow.md) |
| parent folder | the folder holding this one, written .. in a path | [053](./notes/053-absolute-vs-relative-paths.md) |
| path | folder names from the top down to a file, joined by slashes | [040](./notes/040-folders-and-paths.md) |
| pid | the number the system gives one running process, new each run | [050](./notes/050-processes.md) |
| pipe (shell) | joins one programs output to the next programs input | [058](./notes/058-pipes.md) |
| place value | what a digit is worth because of where it sits | [003](./notes/003-counting-in-binary.md) |
| placeholder value | a made up value, like 0, standing in for missing | [032](./notes/032-null-is-not-zero-or-empty-text.md) |
| port | a number picking which program on a machine gets the bytes | [085](./notes/085-addresses-and-ports.md) |
| precision | the most digits a decimal can hold in total | [022](./notes/022-exact-decimal-types.md) |
| primary key | a column that is unique in every row and never NULL | [087](./notes/087-primary-key.md) |
| process | one running copy of a program, loaded into memory | [050](./notes/050-processes.md) |
| processor | the CPU, the part of the computer doing tiny steps on numbers | [035](./notes/035-the-processor.md) |
| program | a file of bytes on disk that can be run | [050](./notes/050-processes.md) |
| quoting (csv) | double quotes around a value so commas inside it stay text | [063](./notes/063-quoting-commas-inside-values.md) |
| reading start to end | taking a files bytes in order from position 0 | [043](./notes/043-reading-start-to-end-vs-jumping.md) |
| record | one row of a table, one thing the data is about | [079](./notes/079-a-table-rows-are-records-columns-are-fields.md) |
| redirect | > sends a programs stdout into a file, emptying it first | [059](./notes/059-redirecting-output-into-a-file.md) |
| register | a tiny holding spot inside the processor, where it works on numbers | [035](./notes/035-the-processor.md) |
| relative path | a path with no leading slash, begun at the working directory | [053](./notes/053-absolute-vs-relative-paths.md) |
| repeating fraction | digits past the point that loop forever, so no exact finite form | [018](./notes/018-why-0-1-has-no-exact-binary-form.md) |
| required field | a field name every record must have, or it is rejected | [077](./notes/077-required-vs-optional-fields.md) |
| root | the top folder holding everything else, written as a single slash | [040](./notes/040-folders-and-paths.md) |
| row | one record of a csv, usually one line, split into values | [062](./notes/062-csv-rows-and-columns-separated-by-commas.md) |
| run | the same value repeated back to back | [047](./notes/047-compression-spotting-repeats.md) |
| run length encoding | storing each run as the value once plus a count | [047](./notes/047-compression-spotting-repeats.md) |
| safe write | write a whole new file beside the old, then rename it over | [046](./notes/046-writing-safely.md) |
| scale | how many of a decimals digits sit after the point | [022](./notes/022-exact-decimal-types.md) |
| schema (file) | a written agreement on which fields every record must have | [075](./notes/075-schema.md) |
| schema on read | storing anything as it arrives, checking shape only when used | [083](./notes/083-schema-on-write-vs-schema-on-read.md) |
| schema on write | checking shape as data goes in, rejecting what doesnt fit | [083](./notes/083-schema-on-write-vs-schema-on-read.md) |
| server | a program that listens on a port and answers requests | [086](./notes/086-client-and-server.md) |
| shell | the program inside a terminal that reads your line and runs it | [049](./notes/049-the-terminal.md) |
| sign bit | the bit saying plus (0) or minus (1) | [013](./notes/013-negative-numbers-sign-bit.md) |
| SSD | a disk made of chips with no moving parts | [037](./notes/037-disk-is-slow.md) |
| standard input | stdin, the channel a process reads from, the keyboard by default | [057](./notes/057-standard-input-and-output.md) |
| standard output | stdout, the channel a process writes to, the screen by default | [057](./notes/057-standard-input-and-output.md) |
| store UTC, show local | keep moments in UTC, convert to local only when displaying | [030](./notes/030-store-utc-show-local.md) |
| stream | bytes handed over in order, like a program reading its stdin | [057](./notes/057-standard-input-and-output.md) |
| structure | an agreement on where each fact sits, so code can find it | [061](./notes/061-structure-why-text-is-hard-to-ask.md) |
| table | a grid of rows, every row holding the same columns | [079](./notes/079-a-table-rows-are-records-columns-are-fields.md) |
| tag | a name in angle brackets, opening or closing an XML value | [072](./notes/072-xml.md) |
| tail | prints the last lines of a file, 10 unless -n says otherwise | [054](./notes/054-head-and-tail.md) |
| terabyte | 1000 gigabytes, a trillion bytes, written TB | [033](./notes/033-kilobytes-to-terabytes.md) |
| terminal | a text window where you type a line and the computer replies | [049](./notes/049-the-terminal.md) |
| text file | a file whose bytes decode as characters, usually with UTF-8 | [041](./notes/041-text-files-vs-binary-files.md) |
| the shop | the imaginary gujarati snack store every example uses | [001](./notes/001-data-is-facts-and-numbers.md) |
| time of day | a clock reading with no day attached | [027](./notes/027-dates-and-times-apart.md) |
| torn write | a write cut off partway, leaving some new blocks and some old | [045](./notes/045-torn-writes.md) |
| twos complement | binary where the leftmost place is negative, so one zero | [014](./notes/014-twos-complement.md) |
| Unicode | one agreed table giving every character in every script a number | [009](./notes/009-unicode.md) |
| unix time | a moment kept as seconds counted since the epoch | [025](./notes/025-unix-time.md) |
| UTC | the one clock everyone measures against, with no daylight saving | [024](./notes/024-utc.md) |
| UTF-8 | a way to store each code point as 1 to 4 bytes | [010](./notes/010-utf-8.md) |
| wc | prints a files counts; wc -l counts its 0a line endings | [055](./notes/055-wc-counting-lines.md) |
| whole cents | money kept as an integer count of cents, price times 100 | [021](./notes/021-storing-money-as-whole-cents.md) |
| working directory | the folder a process stands in, where bare names are looked up | [052](./notes/052-the-working-directory.md) |
| XML | a text format wrapping each value in opening and closing tags | [072](./notes/072-xml.md) |
| YAML | a text format where indentation shows nesting, dashes start list items | [073](./notes/073-yaml.md) |
| YAML trap | a bare word like no read as a boolean, so quote text | [074](./notes/074-yaml-traps.md) |
