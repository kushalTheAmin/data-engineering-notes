# 116: COALESCE, a fallback when a value is NULL
builds on: [031 null, a marker for a missing value](./031-null.md), [032 null is not zero and not empty text](./032-null-is-not-zero-or-empty-text.md), [104 SELECT and FROM, picking columns](./104-select-and-from-picking-columns.md), [115 IS NULL and IS NOT NULL](./115-is-null-and-is-not-null.md)
section: asking questions with SQL, part 16, ~2 min read

a report lists the 5 customers and prints None next to Esha, because she has no city. how do you show "unknown" instead, without touching the data?

COALESCE hands back the first value in its list that isnt a [null](./031-null.md) (a missing value), and null only if every value is null. [115](./115-is-null-and-is-not-null.md) found the nulls, this one replaces them on the way out. here it is as a python loop, on the cities of the shop, the imaginary gujarati snack store these notes run on:

```python
def coalesce(*values):
    for v in values:
        if v is not None:
            return v
    return None

cities = ["Jersey City", "Edison", "Jersey City", "Hoboken", None]
for c in cities:
    print(c, "->", coalesce(c, "unknown"))
```

```output
Jersey City -> Jersey City
Edison -> Edison
Jersey City -> Jersey City
Hoboken -> Hoboken
None -> unknown
```

in SQL thats `COALESCE(city, 'unknown')`, and you can list more fallbacks, so `COALESCE(a, b, c)` tries a, then b, then c. the stored row stays null, only what comes out changes.

but the fallback is a real value now, and whatever runs after it counts it. back to the ratings from [032](./032-null-is-not-zero-or-empty-text.md), where 2 of 5 orders are unrated. in a SELECT (the part that [picks what comes out](./104-select-and-from-picking-columns.md)):

```sql
SELECT avg(stars) AS skips_nulls, avg(COALESCE(stars, 0)) AS filled_with_0 FROM order_ratings
```

```result
skips_nulls | filled_with_0
4.0 | 2.4
```

i figured COALESCE was a cosmetic wrapper, and it quietly changed what avg, the average, divides by: 12 over 3 ratings is 4.0, 12 over 5 is 2.4. thats the same wrecked average as the zero filled column in 032, made at query time instead.

COALESCE is in the SQL standard, so Postgres has it too, meant for defaults at display time. use it on the last step, not before you count or average. the next one is sorting.

---
prev: [115 IS NULL and IS NOT NULL](./115-is-null-and-is-not-null.md) | next: [117 ORDER BY, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md)
