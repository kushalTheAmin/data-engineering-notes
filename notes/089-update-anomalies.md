# 089: update anomalies
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [081 why a shared spreadsheet breaks when many people use it](./081-why-a-shared-spreadsheet-breaks.md), [088 natural keys vs made up ids](./088-natural-keys-vs-made-up-ids.md)
section: tables, keys and relationships, part 11, ~2 min read

Asha moves to Hoboken, someone fixes her city on one order, and now the shop says she lives in two places. nothing in the data says which is right. i assumed this bug needed two people saving at once like in [081](./081-why-a-shared-spreadsheet-breaks.md), and one careful person alone can cause it.

an update anomaly is what you get when the same fact is stored in several rows and an update changes only some of them. in [088](./088-natural-keys-vs-made-up-ids.md) i copied the email into every order, and here its the city. pretend the shop, the imaginary gujarati snack store, kept one wide [table](./079-a-table-rows-are-records-columns-are-fields.md) with the customers city copied onto each order row. a slice, from the real shop rows:

| order_id | customer | city (before) | city (after fixing order 101) |
|---|---|---|---|
| 101 | Asha | Jersey City | Hoboken |
| 103 | Asha | Jersey City | Jersey City |
| 106 | Asha | Jersey City | Jersey City |
| 102 | Bhavin | Edison | Edison |

the person edited the row in front of them, 101. rows 103 and 106 never knew. every row is fine alone, so no rule on a single column can catch it, the problem lives between rows.

```python
rows = [{"order_id": 101, "customer": "Asha", "city": "Jersey City"},
        {"order_id": 103, "customer": "Asha", "city": "Jersey City"},
        {"order_id": 106, "customer": "Asha", "city": "Jersey City"}]
rows[0]["city"] = "Hoboken"
# {...} is a set, it keeps each city once; sorted puts them in order
print(sorted({r["city"] for r in rows if r["customer"] == "Asha"}))
```

```output
['Hoboken', 'Jersey City']
```

one customer, two cities. in the real shop Asha has one row in customers with her city written once, so one update fixes it for all 3 orders. wide copied-everywhere tables are easy to build and this is the price. Wikipedia describes database normalization, the habit of storing each fact once, as a way to reduce redundancy and improve integrity.

the next one is the mirror problem, losing facts you meant to keep.

### check yourself

1. the flat table above is only a slice. the full table also holds Dishas order 105 (Hoboken), and Asha has her 3 rows. someone runs an update that sets city to Hoboken for Ashas orders below 105. how many rows now say Hoboken, and how many of Ashas rows still say Jersey City?
<details><summary>answer</summary>

3 rows say Hoboken (101 and 103 from the update, plus Dishas 105), and 1 of Ashas rows still says Jersey City, order 106. the tempting answers are 2 Hoboken, forgetting Dishas row, and 0 Jersey City left, from reading the update as all of Asha.

</details>

2. a dev says "i fixed it for good, my UPDATE changes every row where customer is Asha". one order was typed with the customer as "asha " with a trailing space. what happens, and why is a careful UPDATE still not enough?
<details><summary>answer</summary>

that row doesnt match in most databases (some MySQL collations ignore case and trailing spaces), so it keeps the old city. the update only reaches copies it can find, and a fact copied many times will eventually have one it cant. storing the city once leaves nothing to miss.

</details>

---
prev: [088 natural keys vs made up ids](./088-natural-keys-vs-made-up-ids.md) | next: [090 insert and delete anomalies](./090-insert-and-delete-anomalies.md)
