# 185: OVER, the window a function looks through
builds on: [140 sum and avg, adding up and averaging](./140-sum-and-avg-adding-up-and-averaging.md), [184 window functions, a total next to every row](./184-window-functions-a-total-next-to-every-row.md)
section: bigger queries, part 12, ~2 min read

how far is each product from the average price, on its own line? in [184](./184-window-functions-a-total-next-to-every-row.md) i typed OVER () and just trusted the empty parentheses, so here is what they actually mean.

the window is the set of rows a [window function](./184-window-functions-a-total-next-to-every-row.md) (a calculation that keeps every row, like an aggregate that doesnt collapse them) looks at while it works on one row, called the current row. OVER () says the window is every row. the shop, the imaginary snack store these notes run on, has 6 products (dhokla, a steamed savory cake, khandvi, a rolled gram flour snack, jalebi and kaju katli, sweets, masala chai, spiced tea, fafda, a crisp gram flour strip). picture a loop where every row gets its own window:

```python
rows = [("dhokla", 6.0), ("khandvi", 7.5), ("jalebi", 5.0), ("kaju katli", 12.0), ("masala chai", 3.0), ("fafda", 4.5)]
for name, price in rows:
    window = rows
    avg = sum(p for _, p in window) / len(window)
    print(name, price, round(price - avg, 2))
```

```output
dhokla 6.0 -0.33
khandvi 7.5 1.17
jalebi 5.0 -1.33
kaju katli 12.0 5.67
masala chai 3.0 -3.33
fafda 4.5 -1.83
```

the same thing in SQL, with [avg](./140-sum-and-avg-adding-up-and-averaging.md) (the sum divided by the count):

```sql
SELECT name, price, round(price - avg(price) OVER (), 2) AS vs_avg FROM products ORDER BY product_id
```

```result
name | price | vs_avg
dhokla | 6.00 | -0.33
khandvi | 7.50 | 1.17
jalebi | 5.00 | -1.33
kaju katli | 12.00 | 5.67
masala chai | 3.00 | -3.33
fafda | 4.50 | -1.83
```

i assumed the window was one fixed thing built once for the whole query. its a fresh look per row, it just happens to be the same look every time here. thats why the average never changes but the last column does, because price belongs to the current row.

price minus the average shows you how far a row sits from the middle, and kaju katli sits 5.67 above the average. the window doesnt have to be the whole table, and shrinking it is where these get useful.

---
prev: [184 window functions, a total next to every row](./184-window-functions-a-total-next-to-every-row.md) | next: [186 PARTITION BY, a separate window per group](./186-partition-by-a-separate-window-per-group.md)
