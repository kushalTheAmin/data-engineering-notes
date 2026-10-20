# 115: IS NULL and IS NOT NULL
builds on: [031 null, a marker for a missing value](./031-null.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [107 comparisons, equal, not equal, bigger, smaller](./107-comparisons-equal-not-equal-bigger-smaller.md), [114 three valued logic, true, false and unknown](./114-three-valued-logic-true-false-and-unknown.md)
section: asking questions with SQL, part 15, ~2 min read

i wrote `WHERE city = NULL` to find the customer with no city and got nothing back, no error. it reads so right.

IS NULL is the test that asks whether a value is missing, and IS NOT NULL asks the opposite. you need them because of [114](./114-three-valued-logic-true-false-and-unknown.md): a test on a [null](./031-null.md) (a missing value) comes out unknown, and [WHERE](./106-where-keeping-only-the-rows-that-match.md) keeps only true. the shop, the imaginary gujarati snack store these notes run on, has 5 customers, and Esha has no city. all three tests side by side:

```sql
SELECT name, city = NULL AS equals_null, city IS NULL AS is_null, city IS NOT NULL AS has_city FROM customers ORDER BY customer_id
```

```result
name | equals_null | is_null | has_city
Asha | NULL | false | true
Bhavin | NULL | false | true
Chirag | NULL | false | true
Disha | NULL | false | true
Esha | NULL | true | false
```

the `= NULL` column is unknown for all 5 rows, Esha included, because "is this equal to something missing" has no answer. so a WHERE on it returns zero rows. `IS NULL` never comes out unknown, only true or false, which makes it the one test that can actually see a null. `WHERE city IS NULL` returns Esha, `WHERE city IS NOT NULL` returns the other 4.

i assumed IS was just a fussy spelling of =, and it turns out to be a different kind of test, one that cant be unknown.

unlike NOT in [110](./110-not-flipping-a-condition.md), these two split the table with nobody lost: 1 row plus 4 rows is the 5 you started with. the Postgres docs say to not write `expression = NULL`, and python is why it tempts you, since `None == None` is True there.

---
prev: [114 three valued logic, true, false and unknown](./114-three-valued-logic-true-false-and-unknown.md) | next: not written yet
