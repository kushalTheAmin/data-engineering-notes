# 031: null, a marker for a missing value
builds on: [001 data is facts written down](./001-data-is-facts-and-numbers.md), [023 true and false, the boolean](./023-true-and-false-the-boolean.md), [027 dates without times, and times without dates](./027-dates-and-times-apart.md)
section: data at the atom level, part 31, ~2 min read

[030](./030-store-utc-show-local.md) ended on keeping the customers zone in its own column. so what goes in that column for someone who never told you?

the shop, the imaginary gujarati snack store these notes run on, has the same problem today: Esha never gave a city. the answer is null, a marker meaning "there is no value here". its not a value, its the absence of one. SELECT lists columns and FROM names the table, a table being rows with named columns:

```sql
SELECT customer_id, name, city FROM customers;
```

```result
customer_id | name | city
1 | Asha | Jersey City
2 | Bhavin | Edison
3 | Chirag | Jersey City
4 | Disha | Hoboken
5 | Esha | NULL
```

in python terms each row is a dictionary, and Eshas has "city": None. the database prints that as NULL with no quotes, because its not text. her city is not the word NULL, its nothing.

now count the table two ways. count(*), which counts rows as in [027](./027-dates-and-times-apart.md), and count(city), which counts only rows that have a city:

```sql
SELECT count(*) AS customers, count(city) AS with_city FROM customers;
```

```result
customers | with_city
5 | 4
```

i assumed a missing value would at least be counted as something. it isnt, count(city) skips it on purpose, and Postgres documents it the same way: https://www.postgresql.org/docs/current/functions-aggregate.html

so what: a report that says "4 customers have a city" is right and "5 customers" is also right, depending on which count you wrote. the [boolean](./023-true-and-false-the-boolean.md) note mentioned null as a third answer, unknown, and this is where it comes from.

### check yourself

1. predict both numbers. count(*) counts rows, count(city) counts rows with a city.
```sql
SELECT count(*) AS n, count(city) AS c FROM customers WHERE name IN ('Disha', 'Esha');
```
<details><summary>answer</summary>

```result
n | c
2 | 1
```
both rows are kept, so n is 2, but Esha has no city so c is 1. the tempting answer is 2 and 2, from thinking a blank cell still counts as a value.

</details>

2. orders get an optional delivery_note. you want to count how many orders have one with count(delivery_note). for orders without a note, do you store the text 'none' or leave it null, and why?
<details><summary>answer</summary>

leave it null. count(delivery_note) skips nulls, so it counts only real notes. with 'none' stored, every order has a value and the count equals the number of orders. the tempting answer is 'none', because it looks tidier, but it makes missing data look like data.

</details>

---
prev: [030 store in UTC, show in local time](./030-store-utc-show-local.md) | next: not written yet
