# 261: third normal form, nothing but the key
builds on: [260 second normal form, nothing about half the key](./260-second-normal-form-nothing-about-half-the-key.md), [258 functional dependency, when one column decides another](./258-functional-dependency-when-one-column-decides-another.md), [257 normal forms, the rules behind splitting tables](./257-normal-forms-the-rules-behind-splitting-tables.md), [089 update anomalies](./089-update-anomalies.md), [087 primary key](./087-primary-key.md)
section: designing tables, part 8, ~2 min read

[260](./260-second-normal-form-nothing-about-half-the-key.md) said a table with a one column key passes second normal form for free. so is the shops orders table, whose key is just order_id, safe from copied data? not quite.

third normal form is the last rule on the [257](./257-normal-forms-the-rules-behind-splitting-tables.md) checklist: every column is about the key and nothing but the key. a column that is really about another plain column, one outside the key, fails it. here is orders in the shop (the imaginary gujarati snack store) with the customers city copied in, a slice of 4 rows:

```sql
SELECT o.order_id, o.customer_id, c.city FROM orders o JOIN customers c ON c.customer_id = o.customer_id WHERE o.order_id <= 104 ORDER BY o.order_id
```

```result
order_id | customer_id | city
101 | 1 | Jersey City
102 | 2 | Edison
103 | 1 | Jersey City
104 | 3 | Jersey City
```

use the lookup from [258](./258-functional-dependency-when-one-column-decides-another.md). the [primary key](./087-primary-key.md) order_id decides customer_id, and customer_id decides city. so city hangs off the key only through another column. orders 101 and 103 both say Jersey City because both are Ashas.

i expected the one column key to protect it like in 260, but the leak runs sideways through customer_id, not out of the key. if Asha moves to Hoboken, orders 101, 103 and 106 all need fixing, and one you miss is the copy bug from [089](./089-update-anomalies.md). the fix is the cut the shop already made: orders keeps customer_id, and city lives in customers.

one gotcha, it depends on meaning. if the column meant where this order was shipped, it is about the order, and Asha can ship one to Hoboken. same values, different column, no failure.

### check yourself

1. the wide orders table also carries a delivery fee, decided by city. the Jersey City fee changes. predict how many order rows need fixing.
```sql
SELECT count(*) AS orders_to_fix FROM orders o JOIN customers c ON c.customer_id = o.customer_id WHERE c.city = 'Jersey City'
```
<details><summary>answer</summary>

```result
orders_to_fix
4
```

4 rows, Ashas 3 plus Chirags 1. the tempting answer is 3, from thinking only of Asha. the fee depends on city, and city depends on customer_id, a plain column chain.

</details>

2. a products table keyed by product_id alone gets a column category_tax, the same for every product in a category. which level does it fail, second or third?
<details><summary>answer</summary>

the third. the key is one column, so the second passes for free, but the tax is about category, a plain column. the tempting answer is none, since a one column key sounds safe, but 260 only promised that for the second level.

</details>

---
prev: [260 second normal form, nothing about half the key](./260-second-normal-form-nothing-about-half-the-key.md) | next: not written yet
