# 260: second normal form, nothing about half the key
builds on: [259 first normal form, one value per cell](./259-first-normal-form-one-value-per-cell.md), [258 functional dependency, when one column decides another](./258-functional-dependency-when-one-column-decides-another.md), [257 normal forms, the rules behind splitting tables](./257-normal-forms-the-rules-behind-splitting-tables.md), [095 composite keys, a key made of two columns](./095-composite-keys.md), [089 update anomalies](./089-update-anomalies.md)
section: designing tables, part 7, ~2 min read

the shop (the imaginary gujarati snack store these notes run on) sells dhokla, a steamed savory cake, on 3 order lines. if every line also carried the word dhokla, how many places do you fix when the name changes?

second normal form is the next rule on the [257](./257-normal-forms-the-rules-behind-splitting-tables.md) checklist for tables: every column must depend on the whole key, never on just part of it. the order_items key is a [composite key](./095-composite-keys.md) (two columns, the pair is unique), order_id and product_id. here is that table with the name copied in, a slice of 3 lines:

```sql
SELECT oi.order_id, oi.product_id, p.name, oi.quantity FROM order_items oi JOIN products p ON p.product_id = oi.product_id WHERE oi.product_id = 1 ORDER BY oi.order_id
```

```result
order_id | product_id | name | quantity
101 | 1 | dhokla | 2
104 | 1 | dhokla | 3
107 | 1 | dhokla | 1
```

use the idea from [258](./258-functional-dependency-when-one-column-decides-another.md), where one column decides another (one value in, one value out). product_id alone decides name, so the name hangs off half the key. quantity is different: product 1 alone gives 2, 3 or 1, and only the pair (order, product) gives one answer. thats the test, ask whether the whole pair is needed.

rename dhokla and 3 lines need fixing, the copy bug from [089](./089-update-anomalies.md). the fix is the cut the shop already made: name lives in products, order_items keeps only quantity.

i assumed a rule this strict would bite everywhere, but a table whose key is one column passes for free, since one column has no half to depend on. so this check only ever fires on composite keys.

### check yourself

1. someone renames kaju katli, product 4, in a wide order_items table that has the name copied onto every line. predict how many lines need fixing.
```sql
SELECT count(*) AS lines_to_fix FROM order_items WHERE product_id = 4
```
<details><summary>answer</summary>

```result
lines_to_fix
2
```

2 lines, orders 102 and 105. the tempting answer is 1, since it is one product, but the copies live on the lines.

</details>

2. ordered_at is copied onto every order_items line. does that break second normal form, and if order 105 gets a corrected time, how many lines change?
```sql
SELECT count(*) AS lines_to_fix FROM order_items WHERE order_id = 105
```
<details><summary>answer</summary>

```result
lines_to_fix
3
```

yes, it breaks it. the time is decided by order_id alone, half of the key, and order 105 has 3 lines. the tempting answer is that it passes because order_id is in the key, but being in the key is not the test, depending on the whole key is.

</details>

---
prev: [259 first normal form, one value per cell](./259-first-normal-form-one-value-per-cell.md) | next: [261 third normal form, nothing but the key](./261-third-normal-form-nothing-but-the-key.md)
