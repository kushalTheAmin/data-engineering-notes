# 113: LIKE, matching text patterns
builds on: [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [107 comparisons, equal, not equal, bigger, smaller](./107-comparisons-equal-not-equal-bigger-smaller.md), [110 NOT, flipping a condition](./110-not-flipping-a-condition.md)
section: asking questions with SQL, part 13, ~2 min read

which products start with k? an equals test needs the whole name, and i only know the first letter.

LIKE keeps a row when its text fits a pattern, where % stands for any run of characters, even none. so `LIKE 'k%'` is pythons `name.startswith("k")`. the shop, the imaginary gujarati snack store these notes run on, has 6 products, and [WHERE](./106-where-keeping-only-the-rows-that-match.md) does the filtering:

```sql
SELECT name FROM products WHERE name LIKE 'k%'
```

```result
name
khandvi
kaju katli
```

khandvi is a chickpea flour snack and kaju katli a cashew sweet. put the % in front and it is endswith, so `LIKE '%a'` gives dhokla and fafda. put one on both sides and it is pythons `in`, so `LIKE '%ch%'` finds masala chai. the other wildcard is _, exactly one character, so `LIKE 'k_a%'` returns only khandvi: kaju also starts with k, but its third letter is j.

now the part that surprised me. you would expect an error if you type a capital K:

```sql
SELECT name FROM products WHERE name LIKE 'K%'
```

```result
name
```

zero rows and no error, because the khandvi in the table is lowercase and LIKE compares letters exactly, in DuckDB and in Postgres. both have ILIKE for a match that ignores case. same trap as the typo in [106](./106-where-keeping-only-the-rows-that-match.md): the query is fine, the answer is just empty.

and NOT LIKE has the [null](./031-null.md) gap from [110](./110-not-flipping-a-condition.md). `city NOT LIKE 'J%'` returns Bhavin and Disha, but not Esha, whose city is missing.

---
prev: [112 BETWEEN, ranges that include both ends](./112-between-ranges-that-include-both-ends.md) | next: [114 three valued logic, true, false and unknown](./114-three-valued-logic-true-false-and-unknown.md)
