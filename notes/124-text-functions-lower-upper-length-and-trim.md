# 124: text functions, lower, upper, length and trim
builds on: [007 text is numbers, one character and one number](./007-text-is-numbers.md), [011 why a gujarati letter takes 3 bytes and g takes 1](./011-why-gujarati-takes-3-bytes.md), [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [107 comparisons, equal, not equal, bigger, smaller](./107-comparisons-equal-not-equal-bigger-smaller.md), [122 computed columns and AS](./122-computed-columns-and-as.md), [123 CASE WHEN, if and else inside a query](./123-case-when-if-and-else-inside-a-query.md)
section: asking questions with SQL, part 24, ~2 min read

Chirag is sitting right there in the table, so why does `WHERE typed_name = 'CHIRAG'` return nothing?

[123](./123-case-when-if-and-else-inside-a-query.md) made a decision per row, text functions change the words per row. a function takes a value and hands back a new one, usually inside a [computed column](./122-computed-columns-and-as.md) (an expression in SELECT). lower and upper change case, length counts [characters](./007-text-is-numbers.md) (letters, digits, spaces), trim cuts spaces off both ends. in python: `s.lower()`, `s.upper()`, `len(s)`, `s.strip()`.

the shop, the imaginary gujarati snack store these notes run on, has a new [table](./079-a-table-rows-are-records-columns-are-fields.md), signups, with names exactly as typed into a form. all four rows, first the length before and after trim:

```sql
SELECT signup_id, length(typed_name) AS len, length(trim(typed_name)) AS trimmed_len FROM signups ORDER BY signup_id
```

```result
signup_id | len | trimmed_len
1 | 4 | 4
2 | 7 | 6
3 | 7 | 6
4 | 5 | 5
```

i assumed you would see a stray space when you look at the rows, and you dont, only the lengths give it away. bhavin and CHIRAG are 6 letters but 7 characters, each with a space on the end. the [equals test](./107-comparisons-equal-not-equal-bigger-smaller.md) compares every character, so 'CHIRAG ' is not 'CHIRAG', and that is the empty result. functions nest inside out, so trim first, then change the case:

```sql
SELECT signup_id, lower(trim(typed_name)) AS lowered, upper(trim(typed_name)) AS uppered FROM signups ORDER BY signup_id
```

```result
signup_id | lowered | uppered
1 | asha | ASHA
2 | bhavin | BHAVIN
3 | chirag | CHIRAG
4 | disha | DISHA
```

now `WHERE lower(trim(typed_name)) = 'chirag'` finds row 3. the stored rows are untouched, the cleaning only exists in the result.

two gotchas. trim removes spaces and nothing else by default (the docs of Postgres, a server database, say so, and in DuckDB, the database these notes run in, a tab survives too). and length counts characters, not bytes: `length('ગ')` is 1 though [UTF-8](./011-why-gujarati-takes-3-bytes.md) stores it in 3 bytes. strlen gives the 3.

---
prev: [123 CASE WHEN, if and else inside a query](./123-case-when-if-and-else-inside-a-query.md) | next: [125 concatenating text, and taking pieces of it](./125-concatenating-text-and-taking-pieces-of-it.md)
