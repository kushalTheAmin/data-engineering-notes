# 262: denormalization, copying data on purpose
builds on: [261 third normal form, nothing but the key](./261-third-normal-form-nothing-but-the-key.md), [257 normal forms, the rules behind splitting tables](./257-normal-forms-the-rules-behind-splitting-tables.md), [089 update anomalies](./089-update-anomalies.md), [155 why joins](./155-why-joins-the-answer-lives-in-more-than-one-table.md), [254 modeling, deciding the tables before writing them](./254-modeling-deciding-the-tables-before-writing-them.md)
section: designing tables, part 9, ~2 min read

the shop (the imaginary gujarati snack store these notes run on) wants a page listing its 7 orders with each customers city. the cities live in a customers table and each order only points at its customer, so you do 7 lookups into customers. copy the city onto each order row and reads need none.

denormalization is copying a fact into a second place on purpose, so reads skip the lookup. [261](./261-third-normal-form-nothing-but-the-key.md) showed that copied city breaking third normal form, one rule on the table checklist from [257](./257-normal-forms-the-rules-behind-splitting-tables.md), and it does. here the break is a choice. in sql the lookup is a [join](./155-why-joins-the-answer-lives-in-more-than-one-table.md) (pairing rows of two tables by a shared id), the python below uses a dictionary.

```python
cities = {1: "Jersey City", 2: "Edison", 3: "Jersey City", 4: "Hoboken", 5: None}
orders = [(101, 1), (102, 2), (103, 1), (104, 3), (105, 4), (106, 1), (107, 2)]
wide = [{"order_id": o, "customer_id": c, "city": cities[c]} for o, c in orders]

print(wide[0])
cities[1] = "Hoboken"
print([w["city"] for w in wide if w["customer_id"] == 1])
wide = [{"order_id": o, "customer_id": c, "city": cities[c]} for o, c in orders]
print([w["city"] for w in wide if w["customer_id"] == 1])
```

```output
{'order_id': 101, 'customer_id': 1, 'city': 'Jersey City'}
['Jersey City', 'Jersey City', 'Jersey City']
['Hoboken', 'Hoboken', 'Hoboken']
```

row 101 carries its city, so reading it needs no lookup. then Asha moves to Hoboken and i fix customers only, the one true home. her 3 order rows still say Jersey City, the stale copy bug from [089](./089-update-anomalies.md), one fact in many rows with only some fixed. the last two lines rebuild the copy from customers.

i assumed breaking the rules meant sloppy design, but the careful version is knowing exactly which copy is the true one and never editing the other by hand.

BigQuery, Googles database for big analysis queries, recommends a close cousin, nested fields, to cut joins, and its docs say it doesnt always help.

one gotcha: a copy meant to freeze, like the price on a receipt from [254](./254-modeling-deciding-the-tables-before-writing-them.md), isnt stale. its a different fact.

### check yourself

1. imagine orders carried a copied city. Jersey City is renamed Jersey City NJ, and someone fixes only customers. predict how many order rows now disagree with it.
```sql
SELECT count(*) AS stale_rows FROM orders o JOIN customers c ON c.customer_id = o.customer_id WHERE c.city = 'Jersey City'
```
<details><summary>answer</summary>

```result
stale_rows
4
```

4 rows, Ashas 3 plus Chirags 1. the tempting answer is 2, the two customers rows, but the copies live on orders.

</details>

2. you may copy one onto every order row: the customers city, or the customers count of open orders. which, and why?
<details><summary>answer</summary>

the city. it changes rarely, so rebuilding the copy is rare. the count changes with every new order, so its copy is wrong until rewritten, again and again. the tempting answer is both, since both are handy, but a copy that goes stale every minute costs more care than it saves.

</details>

---
prev: [261 third normal form, nothing but the key](./261-third-normal-form-nothing-but-the-key.md) | next: not written yet
