# 259: first normal form, one value per cell
builds on: [258 functional dependency, when one column decides another](./258-functional-dependency-when-one-column-decides-another.md), [257 normal forms, the rules behind splitting tables](./257-normal-forms-the-rules-behind-splitting-tables.md), [204 arrays and UNNEST, lists inside a cell](./204-arrays-and-unnest-lists-inside-a-cell.md), [095 composite keys, a key made of two columns](./095-composite-keys.md)
section: designing tables, part 6, ~2 min read

dhokla, the steamed savory cake in the shop (the imaginary gujarati snack store these notes run on), has the tags steamed and savory. what stops someone saving savory twice in that cell?

first normal form, the first rule of the [257](./257-normal-forms-the-rules-behind-splitting-tables.md) checklist for tables, says every cell (one box in a table) holds exactly one value. the product_tags table from [204](./204-arrays-and-unnest-lists-inside-a-cell.md) breaks it, because a list is several values in one cell. the fix is one row per tag, and the key becomes the pair product_id and tag, a [composite key](./095-composite-keys.md) (a unique id made of two columns). a slice of the list version, then the one value version, where UNNEST turns each list item into its own row:

| product_id | tags |
|---|---|
| 1 | [steamed, savory] |
| 4 | [sweet, festive] |
| 5 | [] |

```sql
SELECT product_id, UNNEST(tags) AS tag FROM product_tags WHERE product_id IN (1, 4, 5) ORDER BY product_id, tag
```

```result
product_id | tag
1 | savory
1 | steamed
4 | festive
4 | sweet
```

i figured a list cell was harmless, but it cant refuse anything. a list can say savory twice, while a table with (product_id, tag) declared as its key rejects the second row (DuckDB, the database these notes run, raises an error, i ran it). and "which products are savory" stops being a hunt inside cells, it is a plain WHERE tag = 'savory' that returns 1, 2 and 6.

masala chai, product 5, ends up with no rows at all. no tags means no rows, you dont need a row saying none.

Lists in cells are legal, and the docs of Postgres, another database, still say that searching for array elements can be a sign of misdesign, and suggest a separate table with a row per element.

### check yourself

1. the 6 shop products are split into one row per tag. predict the row count before running.
```sql
SELECT count(*) AS rows_needed FROM (SELECT UNNEST(tags) AS tag FROM product_tags)
```
<details><summary>answer</summary>

```result
rows_needed
10
```

it is 10. five products have 2 tags each and masala chai has none. the tempting 12 comes from 6 products times 2, but chai gets no row.

</details>

2. in the split table, why is product_id alone a bad key, and what happens when (3, fried) is inserted twice?
<details><summary>answer</summary>

product_id alone allows one row per product, so a product could hold only one tag. the pair is the key, so the second (3, fried) is refused as a repeat. the tempting answer is that the repeat is fine because the first one is a different row, but a key means no two rows share its value.

</details>

---
prev: [258 functional dependency, when one column decides another](./258-functional-dependency-when-one-column-decides-another.md) | next: not written yet
