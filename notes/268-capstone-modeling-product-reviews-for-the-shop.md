# 268: capstone, modeling product reviews for the shop
builds on: [254 modeling, deciding the tables before writing them](./254-modeling-deciding-the-tables-before-writing-them.md), [255 entities and attributes](./255-entities-and-attributes.md), [256 one to one, when two tables share a key](./256-one-to-one-when-two-tables-share-a-key.md), [257 normal forms, the rules behind splitting tables](./257-normal-forms-the-rules-behind-splitting-tables.md), [258 functional dependency, when one column decides another](./258-functional-dependency-when-one-column-decides-another.md), [259 first normal form, one value per cell](./259-first-normal-form-one-value-per-cell.md), [260 second normal form, nothing about half the key](./260-second-normal-form-nothing-about-half-the-key.md), [261 third normal form, nothing but the key](./261-third-normal-form-nothing-but-the-key.md), [262 denormalization, copying data on purpose](./262-denormalization-copying-data-on-purpose.md), [263 choosing column types by what you do with the value](./263-choosing-column-types-by-what-you-do-with-the-value.md), [264 naming conventions, names people can guess](./264-naming-conventions-names-people-can-guess.md), [265 created_at and updated_at, two timestamps every table carries](./265-created-at-and-updated-at-two-timestamps-every-table-carries.md), [266 soft deletes, marking a row gone instead of removing it](./266-soft-deletes-marking-a-row-gone-instead-of-removing-it.md), [267 schemas as namespaces, folders for tables](./267-schemas-as-namespaces-folders-for-tables.md), [217 CHECK, a rule every value must pass](./217-check-a-rule-every-value-must-pass.md), [218 key constraints, PRIMARY KEY and REFERENCES in CREATE TABLE](./218-key-constraints-primary-key-and-references-in-create-table.md)
section: designing tables, wrap up, ~3 min read

Esha wants to rate the fafda, a crunchy gram flour snack, 1 to 5 stars with a sentence. where does that rating live, and which of the last 14 notes decide it? [267](./267-schemas-as-namespaces-folders-for-tables.md) ended on folders for tables, so this one puts the whole section to work on one feature.

the shop, the imaginary gujarati snack store these notes run on, gets a reviews table. most choices below trace to a note, and none of the reviews are real shop rows, i made them up. a table is a grid of rows, a primary key is the column or columns that name a row, so no two rows share it. if you are landing here cold, read the middle column as the answer and the right one as the note that explains it:

| decision | what i chose | note |
| --- | --- | --- |
| which table | a rating is about a customer and a product together, so the pair gets a table | [254](./254-modeling-deciding-the-tables-before-writing-them.md) |
| entities | customers and products stay entities, rating and body are attributes of the review | [255](./255-entities-and-attributes.md) |
| one to one | no, many reviews per product and per customer, so customer_id alone repeats, only the pair is unique | [256](./256-one-to-one-when-two-tables-share-a-key.md) |
| the key | the pair (customer_id, product_id) decides everything else | [257](./257-normal-forms-the-rules-behind-splitting-tables.md) [258](./258-functional-dependency-when-one-column-decides-another.md) |
| one value, whole key, only the key | one rating per cell, no product name copied in, no city | [259](./259-first-normal-form-one-value-per-cell.md) [260](./260-second-normal-form-nothing-about-half-the-key.md) [261](./261-third-normal-form-nothing-but-the-key.md) |
| copies | no avg_rating stored on products, compute it | [262](./262-denormalization-copying-data-on-purpose.md) |
| types | rating is an INTEGER you average, with a CHECK for 1 to 5 | [263](./263-choosing-column-types-by-what-you-do-with-the-value.md) |
| names | customer_id and product_id, same as everywhere | [264](./264-naming-conventions-names-people-can-guess.md) |
| time | created_at and updated_at | [265](./265-created-at-and-updated-at-two-timestamps-every-table-carries.md) |
| leaving | deleted_at, a soft delete instead of DELETE | [266](./266-soft-deletes-marking-a-row-gone-instead-of-removing-it.md) |
| folder | stays in main, i tried a feedback folder and DuckDB, the database these notes run in, refused foreign keys across folders | [267](./267-schemas-as-namespaces-folders-for-tables.md) |

```sql
CREATE TABLE reviews (
    customer_id INTEGER NOT NULL REFERENCES customers (customer_id),
    product_id  INTEGER NOT NULL REFERENCES products (product_id),
    rating      INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    body        VARCHAR,
    created_at  TIMESTAMP NOT NULL,
    updated_at  TIMESTAMP NOT NULL,
    deleted_at  TIMESTAMP,
    PRIMARY KEY (customer_id, product_id)
);
INSERT INTO reviews VALUES
    (1, 1, 5, 'soft and fresh',  TIMESTAMP '2026-04-12 10:00:00', TIMESTAMP '2026-04-12 10:00:00', NULL),
    (2, 1, 4, 'a bit dry',       TIMESTAMP '2026-04-12 11:00:00', TIMESTAMP '2026-04-12 11:00:00', NULL),
    (3, 1, 2, 'changed my mind', TIMESTAMP '2026-04-13 09:00:00', TIMESTAMP '2026-04-14 09:00:00', TIMESTAMP '2026-04-14 09:00:00'),
    (1, 2, 3, 'ok',              TIMESTAMP '2026-04-13 12:00:00', TIMESTAMP '2026-04-13 12:00:00', NULL);
SELECT p.name, count(*) AS reviews, avg(r.rating) AS avg_rating
FROM reviews r JOIN products p ON p.product_id = r.product_id
WHERE r.deleted_at IS NULL
GROUP BY p.name ORDER BY p.name
```

```result
name | reviews | avg_rating
dhokla | 2 | 4.5
khandvi | 1 | 3.0
```

Chirags soft deleted (marked gone, row kept) dhokla review is still stored, the WHERE hides it. the gotcha is the key. because the pair is the primary key, Chirag cant write a fresh dhokla review later, his old row still holds the pair, same trap as the unique email in 266.

i figured a design this size would be a pile of fresh decisions, but most columns were already decided by the notes above and i was just looking them up. the key was the one i had to think about.

next section is about why some queries on tables like this get slow as the rows pile up.

### check yourself

1. Chirag soft deleted his dhokla review, then later wants to review dhokla again and runs this INSERT. predict what happens, and what he should have done instead.

```sql
-- fails on purpose
INSERT INTO reviews VALUES (3, 1, 4, 'again', TIMESTAMP '2026-04-15 09:00:00', TIMESTAMP '2026-04-15 09:00:00', NULL)
```

<details><summary>answer</summary>

it errors, a duplicate key on (3, 1), because the soft deleted row still holds the pair. the tempting "it works, that review is gone" forgets soft delete keeps the row. he should UPDATE the old row instead: new rating, deleted_at back to NULL, updated_at moved.

</details>

2. a page forgets the deleted_at filter. predict the dhokla review count and average, rounded to 2 places.

```sql
SELECT p.name, count(*) AS reviews, round(avg(r.rating), 2) AS avg_rating
FROM reviews r JOIN products p ON p.product_id = r.product_id
WHERE p.name = 'dhokla'
GROUP BY p.name
```

<details><summary>answer</summary>

```result
name | reviews | avg_rating
dhokla | 3 | 3.67
```

Chirags 2 stars counts, so 5 + 4 + 2 over 3. the tempting 2 and 4.5 are the live numbers, but without the filter every stored row counts.

</details>

---
prev: [267 schemas as namespaces, folders for tables](./267-schemas-as-namespaces-folders-for-tables.md) | next: [269 big O in plain words, how work grows as data grows](./269-big-o-in-plain-words-how-work-grows-as-data-grows.md)
