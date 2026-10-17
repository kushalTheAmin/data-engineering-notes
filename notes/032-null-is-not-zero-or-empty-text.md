# 032: null is not zero and not empty text
builds on: [031 null, a marker for a missing value](./031-null.md)
section: data at the atom level, part 32, ~2 min read

orders 103 and 107 were delivered but nobody rated them. do you store 0 stars for them, or nothing? it wrecks the average.

[031](./031-null.md) said null is a marker for "no value here", like Eshas missing city (python calls it None). people often reach for a made up placeholder like 0 or '' instead. the shop, the imaginary gujarati snack store these notes run on, now keeps ratings both ways. this is the whole table, 5 rows with named columns. SELECT lists the columns you want and FROM names the table:

```sql
SELECT order_id, stars, stars_zero_filled FROM order_ratings;
```

```result
order_id | stars | stars_zero_filled
101 | 5 | 5
102 | 4 | 4
103 | NULL | 0
105 | 3 | 3
107 | NULL | 0
```

now ask for the average of each column. avg adds the values up and divides by how many it counted:

```sql
SELECT avg(stars) AS real_avg, avg(stars_zero_filled) AS zero_avg FROM order_ratings;
```

```result
real_avg | zero_avg
4.0 | 2.4
```

i kept reading 0 as "no rating", but 0 is a real rating, so the database counts it. avg skips the nulls, so it divides 12 by 3 orders and gets 4.0. with zeros it divides 12 by 5 and gets 2.4. same orders, a rating that looks like an apology. Postgres docs say avg takes the average of the non-null values: https://www.postgresql.org/docs/current/functions-aggregate.html

empty text has the same trap. '' is real text that happens to have no characters, so count(city) counts it (Oracle is the odd one out and turns '' into null). if you used '' for "no city", a report would say the customer has one.

so what: when the fake value is a real one, a dashboard cant tell "unknown" from "zero". null is annoying but honest, and 0 is only right when the answer really is zero.

### check yourself

1. five customers: one city is Edison, two are '' (empty text), two are null. predict both numbers. count(*) counts rows, count(city) counts rows with a city, and VALUES just writes the five rows inline.
```sql
SELECT count(*) AS n, count(city) AS c FROM (VALUES ('Edison'), (''), (''), (NULL), (NULL)) AS t(city);
```
<details><summary>answer</summary>

```result
n | c
5 | 3
```
the empty strings are real values, so they count: Edison plus two '' is 3. the tempting answer is 1, from reading a blank as missing. it only looks missing.

</details>

2. the owner says: just add WHERE stars_zero_filled > 0, which keeps only rows where the stars are above 0, to hide the zeros. predict the average of stars_zero_filled now. does it match avg(stars)?
```sql
SELECT avg(stars_zero_filled) AS avg_filtered FROM order_ratings WHERE stars_zero_filled > 0;
```
<details><summary>answer</summary>

```result
avg_filtered
4.0
```
the 0 rows are dropped, so it divides 12 by 3 and matches avg(stars). but that filter is just rebuilding null by hand, and it breaks if a customer can really give 0 stars. the tempting answer is still 2.4, from forgetting the filter removes rows before averaging.

</details>

---
prev: [031 null, a marker for a missing value](./031-null.md) | next: [033 kilobytes to terabytes, how big data gets](./033-kilobytes-to-terabytes.md)
