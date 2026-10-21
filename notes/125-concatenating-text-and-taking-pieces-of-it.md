# 125: concatenating text, and taking pieces of it
builds on: [031 null, a marker for a missing value](./031-null.md), [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [116 COALESCE, a fallback when a value is NULL](./116-coalesce-a-fallback-when-a-value-is-null.md), [122 computed columns and AS](./122-computed-columns-and-as.md), [124 text functions, lower, upper, length and trim](./124-text-functions-lower-upper-length-and-trim.md)
section: asking questions with SQL, part 25, ~2 min read

i glued every customers name to their city for a mailing label, and Esha came back as NULL instead of a half label. why does one missing piece wipe out the whole thing?

[124](./124-text-functions-lower-upper-length-and-trim.md) changed text per row, this one joins it and cuts it. `||` glues two pieces of text together, like `+` on python strings, and `substr(text, start, count)` cuts a piece out. both usually sit in a [computed column](./122-computed-columns-and-as.md) (a calculation in the list of returned columns).

the shop, the imaginary gujarati snack store these notes run on, has a customers [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows). all five rows:

```sql
SELECT name || ' from ' || city AS label FROM customers ORDER BY customer_id
```

```result
label
Asha from Jersey City
Bhavin from Edison
Chirag from Jersey City
Disha from Hoboken
NULL
```

Esha has no city, a [null](./031-null.md) (a missing value), and gluing onto a null with `||` gives null. i assumed it would keep her name and skip the city, and it doesnt (python would raise an error, SQL quietly returns null). wrap the city in [COALESCE](./116-coalesce-a-fallback-when-a-value-is-null.md) (a fallback for nulls) and she gets one:

```sql
SELECT name || ' from ' || coalesce(city, '?') AS label FROM customers WHERE name = 'Esha'
```

```result
label
Esha from ?
```

now cutting. dhokla, a steamed savory cake, with every letter numbered:

```text
d h o k l a
1 2 3 4 5 6
substr('dhokla', 2, 3)  ->  start at 2, take 3  ->  hok
```

the gotcha is that SQL counts from 1 (for starts of 1 or more), python counts from 0, so the same cut in python is `"dhokla"[1:4]`. Postgres, a server database, counts from 1 too, its docs have `substring('Thomas' from 2 for 3)` giving hom.

this is how you trim a messy code down to its first few characters. if a label in your report ever shows NULL, look for a null in one of the pieces. the concat function skips nulls instead, in Postgres and DuckDB.

---
prev: [124 text functions, lower, upper, length and trim](./124-text-functions-lower-upper-length-and-trim.md) | next: not written yet
