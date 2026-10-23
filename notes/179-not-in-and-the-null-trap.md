# 179: NOT IN and the NULL trap
builds on: [031 null, a marker for a missing value](./031-null.md), [111 IN, matching against a list](./111-in-matching-against-a-list.md), [114 three valued logic, true, false and unknown](./114-three-valued-logic-true-false-and-unknown.md), [166 joining on columns that can be NULL](./166-joining-on-columns-that-can-be-null.md), [174 subquery in WHERE](./174-subquery-in-where.md), [178 EXISTS and NOT EXISTS, asking whether a matching row exists](./178-exists-and-not-exists-asking-whether-a-matching-row-exists.md)
section: bigger queries, part 6, ~2 min read

i widened one filter and the answer went from one customer to none, with no error. NOT IN has a trap, a [NULL](./031-null.md) (a missing value) hiding in the list.

NOT IN keeps a row whose value matches nothing in the list an inner query hands back, the flip of the [subquery in WHERE](./174-subquery-in-where.md). the shop, the imaginary gujarati snack store these notes run on, has delivery_zones from [166](./166-joining-on-columns-that-can-be-null.md): a zone per city, plus a catch-all row with a NULL city.

```sql
SELECT name FROM customers WHERE city NOT IN (SELECT city FROM delivery_zones WHERE zone = 'north') ORDER BY name
```

```result
name
Bhavin
```

Bhavin lives in Edison, outside north. Esha is dropped, her city is NULL so the test is unknown ([114](./114-three-valued-logic-true-false-and-unknown.md)). now ask for every zone except south (<> means not equal), which pulls in the catch-all row:

```sql
SELECT name FROM customers WHERE city NOT IN (SELECT city FROM delivery_zones WHERE zone <> 'south') ORDER BY name
```

```result
name
```

zero rows. the list is now Jersey City, Hoboken, NULL. Bhavin against it:

```text
Edison <> Jersey City   true
Edison <> Hoboken       true
Edison <> NULL          unknown
true AND true AND unknown = unknown, so WHERE drops him
```

[111](./111-in-matching-against-a-list.md) said NOT IN is a chain of not-equal tests joined by AND. a false settles an AND, so anyone in the list gets false, and everyone else gets unknown from the NULL. nobody can get true.

i expected one NULL row to only cost me itself, but it empties the whole result. it rides in from a column you never checked, so a working NOT IN breaks the day one NULL lands there. Postgres (a server database) agrees: null, not true.

[NOT EXISTS](./178-exists-and-not-exists-asking-whether-a-matching-row-exists.md) (true if no row matches) dodges it:

```sql
SELECT name FROM customers c WHERE NOT EXISTS (SELECT 1 FROM delivery_zones z WHERE z.city = c.city AND z.zone <> 'south') ORDER BY name
```

```result
name
Bhavin
Esha
```

a NULL never matches with =, so Esha is back, nothing matched her. filtering the NULL out of the list with `city IS NOT NULL` also works, but Esha stays dropped.

### check yourself

1. predict the rows. who lives somewhere other than Eshas city?

```sql
SELECT name FROM customers WHERE city NOT IN (SELECT city FROM customers WHERE name = 'Esha') ORDER BY name
```
<details><summary>answer</summary>

```result
name
```
nobody. Eshas city is NULL, so the list is just a NULL and every test is unknown. the tempting answer is the other 4 customers.

</details>

2. change it to NOT EXISTS, matching on city. how many of the 5 customers come back, and is Esha one?

```sql
SELECT name FROM customers c WHERE NOT EXISTS (SELECT 1 FROM customers e WHERE e.name = 'Esha' AND e.city = c.city) ORDER BY name
```
<details><summary>answer</summary>

```result
name
Asha
Bhavin
Chirag
Disha
Esha
```
all 5, Esha included. NULL = anything never matches, so no inner row is ever found. the tempting answer is 4, from expecting her to be excluded as herself.

</details>

---
prev: [178 EXISTS and NOT EXISTS, asking whether a matching row exists](./178-exists-and-not-exists-asking-whether-a-matching-row-exists.md) | next: not written yet
