# 258: functional dependency, when one column decides another
builds on: [257 normal forms, the rules behind splitting tables](./257-normal-forms-the-rules-behind-splitting-tables.md), [087 primary key](./087-primary-key.md), [089 update anomalies](./089-update-anomalies.md)
section: designing tables, part 5, ~2 min read

in [257](./257-normal-forms-the-rules-behind-splitting-tables.md) i kept saying a column is "about the key". about is a feeling. can a loop check it?

a functional dependency is when one column decides another: pick any value of the first, and the second has exactly one possible value. below, the shop (the imaginary gujarati snack store these notes run on) has its customers, a slice of 3 columns. decides() is a dictionary that must never get two answers for one question.

```python
customers = [
    {"id": 1, "name": "Asha",   "city": "Jersey City"},
    {"id": 2, "name": "Bhavin", "city": "Edison"},
    {"id": 3, "name": "Chirag", "city": "Jersey City"},
    {"id": 4, "name": "Disha",  "city": "Hoboken"},
    {"id": 5, "name": "Esha",   "city": None},
]

def decides(rows, a, b):
    seen = {}
    for row in rows:
        if seen.setdefault(row[a], row[b]) != row[b]:
            return False
    return True

print("id decides city:", decides(customers, "id", "city"))
print("city decides id:", decides(customers, "city", "id"))
print("name decides city:", decides(customers, "name", "city"))
```

```output
id decides city: True
city decides id: False
name decides city: True
```

it only goes one way. Jersey City comes back with ids 1 and 3, so city cant decide id. i assumed "about the key" was a vague feeling, but its a lookup that must never have two answers. a primary key ([087](./087-primary-key.md), a column unique in every row) decides every other column, and thats the whole point of it.

the third line is the trap. name decides city is True, but only because 5 names happen to differ. data can kill a guess, never prove one. whether it holds is a rule about what the column means: add a second Asha in Hoboken and it breaks. a city copied onto orders is the copy bug from [089](./089-update-anomalies.md): it depends on the customer, not the order.

Postgres uses this: group by a tables primary key and it lets you select that tables other columns without grouping them.

the next one is the simplest rule, one value per cell.

### check yourself

1. does category decide price in products? predict before running.
```sql
SELECT category, count(DISTINCT price) AS prices FROM products GROUP BY category ORDER BY category
```
<details><summary>answer</summary>

```result
category | prices
drink | 1
snack | 3
sweet | 2
```

no. snack has 3 prices (6.00, 7.50, 4.50), so one category gives several answers. the tempting yes comes from drink, which has one product and so one price by luck.

</details>

2. a second customer named Asha joins from Hoboken. which of "name decides city" and "id decides city" still hold?
<details><summary>answer</summary>

only id. Asha now maps to Jersey City and Hoboken. the tempting answer is that both hold because they held before, but the old rows only showed what was true so far.

</details>

---
prev: [257 normal forms, the rules behind splitting tables](./257-normal-forms-the-rules-behind-splitting-tables.md) | next: [259 first normal form, one value per cell](./259-first-normal-form-one-value-per-cell.md)
