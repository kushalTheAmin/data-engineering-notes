# 344: practice, dedupe and count orders in plain python
builds on: [341 reading JSON in python, the whole file at once](./341-reading-json-in-python-the-whole-file-at-once.md), [340 reading a csv in python, row by row](./340-reading-a-csv-in-python-row-by-row.md), [194 removing duplicates with ROW_NUMBER](./194-removing-duplicates-with-row-number.md)
section: python for data work, part 20, ~2 min read

a retry sends orders 101 and 102 to the shop twice. how many orders did it get, 9 or 7? any count you run before deduping says 9, and thats the bug.

to [deduplicate](./194-removing-duplicates-with-row-number.md) is to keep one row per thing when the data holds several. 194 did it in SQL, this is practice for plain python, five tasks on the shop (the imaginary gujarati snack store these notes run on). the tools are a [csv reader](./340-reading-a-csv-in-python-row-by-row.md), which hands out a csv file one row at a time, [json.load](./341-reading-json-in-python-the-whole-file-at-once.md), which turns JSON into python values (json.loads does the same for text in a variable), and a dictionary used as buckets.

this is the city_feed slice from 194 (all 5 rows), with what two dedupe rules keep:

| row | customer_id | city | changed_at | exact copies dropped | latest per customer |
|---|---|---|---|---|---|
| 1 | 1 | Jersey City | 2026-04-10 09:00:00 | keep | drop |
| 2 | 2 | Edison | 2026-04-10 09:05:00 | keep | keep |
| 3 | 1 | Hoboken | 2026-04-12 18:30:00 | keep | keep |
| 4 | 4 | Hoboken | 2026-04-11 07:45:00 | keep | keep |
| 5 | 2 | Edison | 2026-04-10 09:05:00 | drop | drop |

same 5 rows, 4 left or 3 left, depending on the rule. i assumed dedupe was one operation, but you have to pick which row survives first. worked example, the exact-copies column, in python:

```python
import csv, os, tempfile

path = os.path.join(tempfile.mkdtemp(), "city_feed.csv")
with open(path, "w", newline="") as f:
    f.write("customer_id,city,changed_at\n1,Jersey City,2026-04-10 09:00:00\n2,Edison,2026-04-10 09:05:00\n1,Hoboken,2026-04-12 18:30:00\n4,Hoboken,2026-04-11 07:45:00\n2,Edison,2026-04-10 09:05:00\n")
with open(path, newline="") as f:
    feed = list(csv.DictReader(f))

seen = {}
try:
    seen[feed[0]] = 1
except TypeError as e:
    print(e)
for row in feed:
    key = tuple(row.values())  # a tuple, a fixed list, can be a key
    if key not in seen:
        seen[key] = row
print(len(feed), len(seen))
```

```output
unhashable type: 'dict'
5 4
```

a dictionary cant be a key, because its contents can change ([python docs](https://docs.python.org/3/glossary.html) say mutable containers like dictionaries are not hashable). so the row becomes a tuple first. a retry after a timeout is how real duplicates show up, since the first call may have worked and only the reply got lost.

### check yourself

1. the 7 shop orders are 101 to 107, with 104 cancelled, 106 pending and the rest delivered, as JSON text. count them by status with a dictionary of buckets. what prints?
<details><summary>answer</summary>

```python
import json
raw = '[{"order_id": 101, "status": "delivered"}, {"order_id": 102, "status": "delivered"}, {"order_id": 103, "status": "delivered"}, {"order_id": 104, "status": "cancelled"}, {"order_id": 105, "status": "delivered"}, {"order_id": 106, "status": "pending"}, {"order_id": 107, "status": "delivered"}]'
counts = {}
for o in json.loads(raw):
    if o["status"] not in counts:
        counts[o["status"]] = 0
    counts[o["status"]] += 1
print(counts)
```

```output
{'delivered': 5, 'cancelled': 1, 'pending': 1}
```

</details>

2. same 7 orders. a retry appends 101 and 102 (both delivered) again to the list. predict len and the delivered count before and after deduping by order_id, keeping the first copy.
<details><summary>answer</summary>

```python
import json
raw = '[{"order_id": 101, "status": "delivered"}, {"order_id": 102, "status": "delivered"}, {"order_id": 103, "status": "delivered"}, {"order_id": 104, "status": "cancelled"}, {"order_id": 105, "status": "delivered"}, {"order_id": 106, "status": "pending"}, {"order_id": 107, "status": "delivered"}]'
orders = json.loads(raw)
orders = orders + orders[:2]
unique = {}
for o in orders:
    if o["order_id"] not in unique:
        unique[o["order_id"]] = o
print(len(orders), sum(1 for o in orders if o["status"] == "delivered"))
print(len(unique), sum(1 for o in unique.values() if o["status"] == "delivered"))
```

```output
9 7
7 5
```

delivered looks like 7 until you dedupe. the tempting answer is 5 before dedupe too, from remembering the clean list.

</details>

3. customer 1 is Asha, 2 is Bhavin, 4 is Disha. you dedupe the feed by customer_id and keep the first row seen. 3 rows come out, right count. whose city is wrong?
<details><summary>answer</summary>

```python
feed = [{"customer_id": 1, "city": "Jersey City", "changed_at": "2026-04-10 09:00:00"}, {"customer_id": 2, "city": "Edison", "changed_at": "2026-04-10 09:05:00"}, {"customer_id": 1, "city": "Hoboken", "changed_at": "2026-04-12 18:30:00"}, {"customer_id": 4, "city": "Hoboken", "changed_at": "2026-04-11 07:45:00"}, {"customer_id": 2, "city": "Edison", "changed_at": "2026-04-10 09:05:00"}]
first = {}
for row in feed:
    if row["customer_id"] not in first:
        first[row["customer_id"]] = row
print({cid: r["city"] for cid, r in first.items()})
```

```output
{1: 'Jersey City', 2: 'Edison', 4: 'Hoboken'}
```

Asha, still in Jersey City, her old row came first. the count was right, the data wrong, so counts alone never catch it.

</details>

4. keep the newest row per customer instead. predict the three lines, then say whether SQL agrees.
<details><summary>answer</summary>

```python
feed = [{"customer_id": 1, "city": "Jersey City", "changed_at": "2026-04-10 09:00:00"}, {"customer_id": 2, "city": "Edison", "changed_at": "2026-04-10 09:05:00"}, {"customer_id": 1, "city": "Hoboken", "changed_at": "2026-04-12 18:30:00"}, {"customer_id": 4, "city": "Hoboken", "changed_at": "2026-04-11 07:45:00"}, {"customer_id": 2, "city": "Edison", "changed_at": "2026-04-10 09:05:00"}]
latest = {}
for row in feed:
    cid = row["customer_id"]
    if cid not in latest or row["changed_at"] > latest[cid]["changed_at"]:
        latest[cid] = row
for cid in sorted(latest):
    print(cid, latest[cid]["city"], latest[cid]["changed_at"])
```

```output
1 Hoboken 2026-04-12 18:30:00
2 Edison 2026-04-10 09:05:00
4 Hoboken 2026-04-11 07:45:00
```

the text dates compare in time order because the year comes first. SQL, the 194 way, gives the same rows:

```sql
SELECT customer_id, city, changed_at FROM (SELECT customer_id, city, changed_at, row_number() OVER (PARTITION BY customer_id ORDER BY changed_at DESC) AS rn FROM city_feed) AS t WHERE rn = 1 ORDER BY customer_id
```

```result
customer_id | city | changed_at
1 | Hoboken | 2026-04-12 18:30:00
2 | Edison | 2026-04-10 09:05:00
4 | Hoboken | 2026-04-11 07:45:00
```

</details>

5. which customers have more than one different city in the feed, and does row count give the same answer?
<details><summary>answer</summary>

```python
feed = [{"customer_id": 1, "city": "Jersey City", "changed_at": "2026-04-10 09:00:00"}, {"customer_id": 2, "city": "Edison", "changed_at": "2026-04-10 09:05:00"}, {"customer_id": 1, "city": "Hoboken", "changed_at": "2026-04-12 18:30:00"}, {"customer_id": 4, "city": "Hoboken", "changed_at": "2026-04-11 07:45:00"}, {"customer_id": 2, "city": "Edison", "changed_at": "2026-04-10 09:05:00"}]
cities = {}
for row in feed:
    if row["customer_id"] not in cities:
        cities[row["customer_id"]] = {}
    cities[row["customer_id"]][row["city"]] = True
print([cid for cid in cities if len(cities[cid]) > 1])
print({cid: len(c) for cid, c in cities.items()})
```

```output
[1]
{1: 2, 2: 1, 4: 1}
```

only Asha moved. Bhavin has 2 rows but 1 city, so counting rows says 2 customers moved, counting distinct cities says 1.

</details>

---
prev: [343 calling an API from python, status first, then parse](./343-calling-an-api-from-python-status-first-then-parse.md) | next: not written yet
