# data engineering notes

learning data engineering from the very bottom, one concept at a time, in public. starts at what a bit is and ends at designing data platforms. every note is a 2 minute read, every note links to the ones it builds on, and every example uses the same small imaginary snack shop so you always know the data.

start here: [001 data is facts written down](./notes/001-data-is-facts-and-numbers.md)

notes so far: 21

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
