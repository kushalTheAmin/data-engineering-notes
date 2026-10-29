# 257: normal forms, the rules behind splitting tables
builds on: [256 one to one, when two tables share a key](./256-one-to-one-when-two-tables-share-a-key.md), [255 entities and attributes](./255-entities-and-attributes.md), [089 update anomalies](./089-update-anomalies.md), [087 primary key, one unique id per row](./087-primary-key.md), [097 junction tables, the table in the middle](./097-junction-tables.md)
section: designing tables, part 4, ~2 min read

[255](./255-entities-and-attributes.md) and [256](./256-one-to-one-when-two-tables-share-a-key.md) both cut tables apart by feel. is there a checklist, so you know a table needs cutting before it bites?

there is. a normal form is a numbered rule a table either passes or fails, and each one bans one way of copying a fact. that copying is what caused the [update anomalies](./089-update-anomalies.md) (one fact in many rows, an update missing some). the first three forms, each with a table the shop (the imaginary snack store) must never build:

| normal form | a table fails when | a shop table that would fail |
| --- | --- | --- |
| first | one cell holds a list | orders with items = "dhokla, masala chai" on order 101 |
| second | a column is about only half a two-column key | order_items with the product name beside product_id |
| third | a column is about another column, not the row | customers with a delivery fee beside city |

take the second row. order_items is a [junction table](./097-junction-tables.md) (one row per pair of things), so its [primary key](./087-primary-key.md) (the columns unique per row) is the pair order_id plus product_id. a column is about something when that thing alone settles its value. a product name is about the product alone, half of that pair, so dhokla would be copied into 3 rows, one per order that holds it. third row: the fee is about the city, so Jersey City would repeat on Asha and Chirag.

i read these as three separate checklists, but they stack. a table in third form passes first and second too. the shop, as built, passes all three, which is why none of those tables exist in it.

nothing checks this for you. a database enforces keys and column types, but whether a column is really about the key is a design call you make on paper. forms go past third, and third is the one often called normalized.

### check yourself

1. a teammate adds a product_name column to order_items, then renames dhokla to dhokla fresh by updating one row. how many rows still say the old name, and which rung broke? this counts the rows that held dhokla:

```sql
SELECT count(*) AS rows_with_dhokla FROM order_items WHERE product_id = 1
```

<details><summary>answer</summary>

```result
rows_with_dhokla
3
```

so 2 rows still say dhokla, since only 1 of the 3 was updated. the name is about the product alone, half the key, so second form broke. the tempting answer is third, because a name sits beside an id, but third is about a column that is about another non-key column.

</details>

2. customers gets a phones cell holding 555-0101, 555-0199 for Asha. which form fails, and can the table still pass third form?

<details><summary>answer</summary>

first form fails, one cell holds a list. and no, it cant pass third, since the forms stack and passing third includes passing first. the tempting yes treats third as only about city-style copying.

</details>

---
prev: [256 one to one, when two tables share a key](./256-one-to-one-when-two-tables-share-a-key.md) | next: not written yet
