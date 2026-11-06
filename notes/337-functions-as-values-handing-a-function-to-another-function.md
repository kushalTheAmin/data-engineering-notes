# 337: functions as values, handing a function to another function
builds on: [336 classes in one picture, data and functions together](./336-classes-in-one-picture-data-and-functions-together.md), [278 hash tables, how a dictionary finds a key without searching](./278-hash-tables-how-a-dictionary-finds-a-key-without-searching.md), [117 order by, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md)
section: python for data work, part 13, ~2 min read

sorted() can put the shops products in price order, and nobody told it what a price is. where does it get the rule?

in python a function is a value, like a number or a list, so you can hand it to another function. write the name with no parentheses and you pass the function itself. add parentheses and you call it and pass its answer.

the shop, the imaginary gujarati snack store these notes run on, has products, here a slice of 4 kept as [dictionaries](./278-hash-tables-how-a-dictionary-finds-a-key-without-searching.md), pythons name to value lookup. i write by_price, a function that takes one product and returns its price. sorted, pythons built-in that returns a new ordered list, takes a named argument, key=by_price, and calls it on each product to get something it can compare. same job as ORDER BY price in [117](./117-order-by-sorting-by-one-or-more-columns.md), SQLs way to sort rows.

| product | by_price(product) gives |
| --- | --- |
| dhokla | 6.0 |
| kaju katli | 12.0 |
| masala chai | 3.0 |
| fafda | 4.5 |

sorted orders by that right hand column, so the result is masala chai, fafda, dhokla, kaju katli.

```python
products = [
    {"name": "dhokla", "price": 6.0},
    {"name": "kaju katli", "price": 12.0},
    {"name": "masala chai", "price": 3.0},
    {"name": "fafda", "price": 4.5},
]
calls = []
def by_price(p):
    calls.append(p["name"])
    return p["price"]

print([p["name"] for p in sorted(products, key=by_price)])
print(len(calls))
try:
    sorted(products, key=by_price())
except TypeError as e:
    print(e)
```

```output
['masala chai', 'fafda', 'dhokla', 'kaju katli']
4
by_price() missing 1 required positional argument: 'p'
```

i expected sorted to need a whole rule for comparing two products, but it only wants a function that turns one product into something comparable, here a number. and it calls it once per product, 4 calls, not once per comparison (the python docs say so). the third print is the parentheses trap: by_price() runs the function with nothing to look at, so it fails before sorted even starts.

max and min take key= the same way, so max(products, key=by_price) gives the kaju katli dictionary, the priciest product.

---
prev: [336 classes in one picture, data and functions together](./336-classes-in-one-picture-data-and-functions-together.md) | next: [338 returning a function, building a function inside a function](./338-returning-a-function-building-a-function-inside-a-function.md)
