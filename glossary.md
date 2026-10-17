# glossary

every term these notes have built, in plain words, with the note that built it. if a note uses a term, its in here first.

| term | plain meaning | built in |
|---|---|---|
| ambiguous time | a clock reading that happens twice, when clocks go back | [029](./notes/029-daylight-saving.md) |
| ASCII | the old table giving 128 characters a number, English only | [008](./notes/008-ascii-runs-out.md) |
| binary | counting with only 0 and 1, each place worth double | [003](./notes/003-counting-in-binary.md) |
| binary fraction | binary carried past the point, places worth a half, quarter, eighth | [017](./notes/017-fractions-in-binary.md) |
| binary point | the dot in a binary number, places to its right halve | [017](./notes/017-fractions-in-binary.md) |
| bit | one tiny switch inside a computer, written as 0 or 1 | [002](./notes/002-bits.md) |
| boolean | a value with only two states, true or false | [023](./notes/023-true-and-false-the-boolean.md) |
| byte | a group of 8 bits, holding 256 possible values | [004](./notes/004-bytes.md) |
| byte in hex | a byte is always exactly two hex digits, 00 to ff | [006](./notes/006-one-byte-two-hex-digits.md) |
| character | one letter, digit, space or symbol, stored as one number | [007](./notes/007-text-is-numbers.md) |
| code point | the number Unicode gives one character, written like U+0AA2 | [009](./notes/009-unicode.md) |
| combining mark | a code point with no letter, drawn on the letter before it | [012](./notes/012-combining-marks.md) |
| continuation byte | a UTF-8 byte starting 10, continuing the previous characters bytes | [011](./notes/011-why-gujarati-takes-3-bytes.md) |
| core | one full processor inside a chip, most chips hold several | [035](./notes/035-the-processor.md) |
| data | facts written down so you can ask questions about them later | [001](./notes/001-data-is-facts-and-numbers.md) |
| date | a calendar day with no time of day | [027](./notes/027-dates-and-times-apart.md) |
| daylight saving | clocks shifting an hour twice a year in many places | [024](./notes/024-utc.md) |
| disk | storage like an SSD or hard drive, keeping bytes without power | [036](./notes/036-memory-vs-disk.md) |
| epoch | the starting line, 1 January 1970 UTC, that unix time counts from | [025](./notes/025-unix-time.md) |
| exact decimal | a type keeping decimal digits exactly, like DECIMAL(6, 2) | [022](./notes/022-exact-decimal-types.md) |
| exact tie | an answer halfway between two floats, rounded to the one ending 0 | [020](./notes/020-why-0-1-plus-0-2-is-not-0-3.md) |
| file | a name plus a list of bytes in order, kept on disk | [039](./notes/039-a-file-is-a-named-list-of-bytes.md) |
| file extension | the letters after the dot in a name, just a label | [039](./notes/039-a-file-is-a-named-list-of-bytes.md) |
| float | binary digits plus a count of how far to slide the point | [019](./notes/019-floating-point.md) |
| gibibyte | 1024 x 1024 x 1024 bytes, written GiB | [038](./notes/038-1000-or-1024.md) |
| gigabyte | 1000 megabytes, a billion bytes, written GB | [033](./notes/033-kilobytes-to-terabytes.md) |
| grapheme | one unit as seen on screen, possibly several code points | [012](./notes/012-combining-marks.md) |
| hexadecimal | counting with sixteen digits, a to f standing for ten to fifteen | [005](./notes/005-hexadecimal.md) |
| integer size | how many bits a whole number gets, which sets its range | [015](./notes/015-integer-sizes.md) |
| kibibyte | 1024 bytes, the unambiguous 1024 based unit, written KiB | [038](./notes/038-1000-or-1024.md) |
| kilobyte | 1000 bytes, written KB | [033](./notes/033-kilobytes-to-terabytes.md) |
| lookup | fetching one value from a random spot | [037](./notes/037-disk-is-slow.md) |
| megabyte | 1000 kilobytes, a million bytes, written MB | [033](./notes/033-kilobytes-to-terabytes.md) |
| memory | the computers working space (RAM), emptied when the power goes off | [036](./notes/036-memory-vs-disk.md) |
| microsecond | a millionth of a second | [026](./notes/026-seconds-milliseconds-microseconds.md) |
| millisecond | a thousandth of a second | [026](./notes/026-seconds-milliseconds-microseconds.md) |
| nanosecond | a billionth of a second | [037](./notes/037-disk-is-slow.md) |
| negative zero | a second zero pattern, with the sign bit set | [013](./notes/013-negative-numbers-sign-bit.md) |
| null | a marker meaning there is no value here, not a value | [031](./notes/031-null.md) |
| offset | how far a clock sits ahead of or behind UTC, like +05:30 | [028](./notes/028-time-zone-offsets.md) |
| overflow | a result too big for its bit size, wrapping or erroring | [016](./notes/016-overflow.md) |
| place value | what a digit is worth because of where it sits | [003](./notes/003-counting-in-binary.md) |
| placeholder value | a made up value, like 0, standing in for missing | [032](./notes/032-null-is-not-zero-or-empty-text.md) |
| precision | the most digits a decimal can hold in total | [022](./notes/022-exact-decimal-types.md) |
| processor | the CPU, the part of the computer doing tiny steps on numbers | [035](./notes/035-the-processor.md) |
| register | a tiny holding spot inside the processor, where it works on numbers | [035](./notes/035-the-processor.md) |
| repeating fraction | digits past the point that loop forever, so no exact finite form | [018](./notes/018-why-0-1-has-no-exact-binary-form.md) |
| scale | how many of a decimals digits sit after the point | [022](./notes/022-exact-decimal-types.md) |
| sign bit | the bit saying plus (0) or minus (1) | [013](./notes/013-negative-numbers-sign-bit.md) |
| SSD | a disk made of chips with no moving parts | [037](./notes/037-disk-is-slow.md) |
| store UTC, show local | keep moments in UTC, convert to local only when displaying | [030](./notes/030-store-utc-show-local.md) |
| terabyte | 1000 gigabytes, a trillion bytes, written TB | [033](./notes/033-kilobytes-to-terabytes.md) |
| the shop | the imaginary gujarati snack store every example uses | [001](./notes/001-data-is-facts-and-numbers.md) |
| time of day | a clock reading with no day attached | [027](./notes/027-dates-and-times-apart.md) |
| twos complement | binary where the leftmost place is negative, so one zero | [014](./notes/014-twos-complement.md) |
| Unicode | one agreed table giving every character in every script a number | [009](./notes/009-unicode.md) |
| unix time | a moment kept as seconds counted since the epoch | [025](./notes/025-unix-time.md) |
| UTC | the one clock everyone measures against, with no daylight saving | [024](./notes/024-utc.md) |
| UTF-8 | a way to store each code point as 1 to 4 bytes | [010](./notes/010-utf-8.md) |
| whole cents | money kept as an integer count of cents, price times 100 | [021](./notes/021-storing-money-as-whole-cents.md) |
