# 257: normal forms, the rules behind splitting tables
builds on: [256 one to one, when two tables share a key](./256-one-to-one-when-two-tables-share-a-key.md), [091 splitting into tables](./091-splitting-into-tables.md), [089 update anomalies](./089-update-anomalies.md), [090 insert and delete anomalies](./090-insert-and-delete-anomalies.md), [095 composite keys](./095-composite-keys.md), [204 arrays and UNNEST](./204-arrays-and-unnest-lists-inside-a-cell.md)
section: designing tables, part 4, ~2 min read

people say a table is "in third normal form" like its a grade, a B+ for tables. what are they actually grading?

since [256](./256-one-to-one-when-two-tables-share-a-key.md) the notes keep splitting facts into their own tables. a normal form is a named checklist for a table. pass it and one kind of bug from [089](./089-update-anomalies.md) and [090](./090-insert-and-delete-anomalies.md) (a fact in the wrong place, like copied onto many rows) cant happen. they stack, so third includes second includes first, and each gets its own note.

the key is the column or columns that name a row. in the shop, the imaginary gujarati snack store, the first row below is real and the others are imagined:

| level | the check | a row that fails it |
| --- | --- | --- |
| first | one value per cell | product_tags row for dhokla, a steamed savory cake: tags is [steamed, savory] |
| second | every column is about the whole key, not part of it | order_items row (order 101, product 1, quantity 2) with the product name dhokla copied in |
| third | every column is about the key, not about another column | orders row 101 with the city Jersey City copied in |

order_items has a [composite key](./095-composite-keys.md) (a key of two columns), order and product. dhokla is about product 1 alone, so its name would repeat on all 3 order lines holding dhokla. in the third row the city is about the customer, not the order, so it would repeat on every order from Jersey City, 4 of them (Asha 3, Chirag 1). the first row is why [204](./204-arrays-and-unnest-lists-inside-a-cell.md) needed UNNEST (split a list into rows) to count tags.

each fix is a cut like [091](./091-splitting-into-tables.md). i heard "third normal form" as a grade, but its a checklist, and the checks are about what a column means, so you run it by hand. the second only applies when the key has two columns or more.

Edgar Codd defined the first form in 1970, the second and third in 1971.

### check yourself

1. someone copies the city onto every shop order row. Jersey City gets renamed to Jersey City NJ. without running it, how many order rows need fixing, and which level does this table fail?
```sql
SELECT count(*) AS orders_to_fix FROM orders o JOIN customers c ON c.customer_id = o.customer_id WHERE c.city = 'Jersey City'
```
<details><summary>answer</summary>

```result
orders_to_fix
4
```

4 rows, since Asha has 3 orders and Chirag 1, and it fails the third level (city is about the customer, not the order). the tempting answer is 2, counting customers, but the copies live on orders.

</details>

2. a wide order_items table adds a category column (snack, sweet, drink) copied from products. the lowest level it fails is the second or the third?
<details><summary>answer</summary>

the second. a table failing the second also fails the third, so the lowest one counts. category is about the product alone, which is half of the key (order, product). the tempting answer is the third, because it is a fact about another column, but product_id here is part of the key, not a plain column.

</details>

---
prev: [256 one to one, when two tables share a key](./256-one-to-one-when-two-tables-share-a-key.md) | next: not written yet
