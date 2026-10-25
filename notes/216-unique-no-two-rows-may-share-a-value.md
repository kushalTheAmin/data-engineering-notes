# 216: UNIQUE, no two rows may share a value
builds on: [031 null, a marker meaning there is no value](./031-null.md), [087 primary key](./087-primary-key.md), [213 CREATE TABLE, naming a table and its columns](./213-create-table-naming-a-table-and-its-columns.md), [215 NOT NULL and DEFAULT, required columns and fallback values](./215-not-null-and-default-required-columns-and-fallback-values.md)
section: changing data safely, part 9, ~2 min read

two shoppers sign up with the same email. the table already has a primary key, so which rule stops the second one?

not the key, the key is for customer_id. UNIQUE is a rule you put on any other column: the database refuses a row whose value is already in that column. you write it inside [CREATE TABLE](./213-create-table-naming-a-table-and-its-columns.md) (the command that makes a table), next to rules like [NOT NULL](./215-not-null-and-default-required-columns-and-fallback-values.md) (refuse a missing value). the shop, the imaginary gujarati snack store these notes run on, gets a login table, in DuckDB. INSERT INTO adds rows:

```sql
CREATE TABLE login (customer_id INTEGER NOT NULL, email VARCHAR UNIQUE);
INSERT INTO login VALUES (1, 'asha@example.com'), (2, 'bhavin@example.com');
SELECT * FROM login ORDER BY customer_id
```

```result
customer_id | email
1 | asha@example.com
2 | bhavin@example.com
```

now Chirag tries ashas email:

```sql
-- fails on purpose
INSERT INTO login VALUES (3, 'asha@example.com')
```

DuckDB says duplicate key, violates unique constraint, and the row never lands. a [primary key](./087-primary-key.md) (a column unique in every row and never missing) is this same rule plus no NULL, and a table gets only one primary key but can have many UNIQUE columns.

the part i didnt expect is [NULL](./031-null.md) (no value). in DuckDB two missing emails dont count as the same value, so both get in (count(email) counts only rows that have one):

```sql
INSERT INTO login VALUES (4, NULL), (5, NULL);
SELECT count(*) AS rows_now, count(email) AS with_email FROM login
```

```result
rows_now | with_email
4 | 2
```

i assumed one NULL would be the limit. Postgres does the same by default, though SQL Server allows only one, and its docs say you can add NULLS NOT DISTINCT to change that. so if you need every row to have a value, UNIQUE alone is not enough, pair it with NOT NULL.

### check yourself

1. a coupon table has `code VARCHAR UNIQUE`. coupon DIWALI is saved for Asha (customer 1), then diwali for Bhavin (customer 2). is the second row accepted? how many rows come back?
```sql
CREATE TABLE coupon (code VARCHAR UNIQUE, customer_id INTEGER);
INSERT INTO coupon VALUES ('DIWALI', 1), ('diwali', 2);
SELECT count(*) AS coupons FROM coupon
```
<details><summary>answer</summary>

```result
coupons
2
```
accepted. in DuckDB, UNIQUE compares the text exactly, so DIWALI and diwali are different values (MySQL ignores case by default and would refuse). the tempting answer is refused, because they look the same to a person.

</details>

2. the shop sets city UNIQUE in a new table and saves five cities: Jersey City, Edison, Hoboken, and two customers with no city, like Esha. do all five go in, and what do count(*) and count(city) give?
```sql
CREATE TABLE hub (city VARCHAR UNIQUE);
INSERT INTO hub VALUES ('Jersey City'), ('Edison'), ('Hoboken'), (NULL), (NULL);
SELECT count(*) AS all_rows, count(city) AS named FROM hub
```
<details><summary>answer</summary>

```result
all_rows | named
5 | 3
```
all five go in, since DuckDB never clashes NULLs, and count(city) skips them. the tempting answer is 4 rows, one NULL allowed.

</details>

---
prev: [215 NOT NULL and DEFAULT, required columns and fallback values](./215-not-null-and-default-required-columns-and-fallback-values.md) | next: [217 CHECK, a rule every value must pass](./217-check-a-rule-every-value-must-pass.md)
