# 338: returning a function, building a function inside a function
builds on: [337 functions as values, handing a function to another function](./337-functions-as-values-handing-a-function-to-another-function.md), [278 hash tables, how a dictionary finds a key without searching](./278-hash-tables-how-a-dictionary-finds-a-key-without-searching.md)
section: python for data work, part 14, ~2 min read

in 337 i wrote by_price by hand. do i need a second function for by_name, and a third for every other field? what if one function just made them for me?

a function can return another function. you define a function inside a function and return it with no parentheses, and the inner one keeps the outer variables it used. that pairing is called a closure.

the shop, the imaginary gujarati snack store these notes run on, has products, here a slice of 4 as [dictionaries](./278-hash-tables-how-a-dictionary-finds-a-key-without-searching.md), pythons name to value lookup. by(field) builds a getter for whichever field you name, and [337](./337-functions-as-values-handing-a-function-to-another-function.md) already showed sorted calling a key function, a function giving each item its sort value.

```python
products = [
    {"name": "dhokla", "price": 6.0},
    {"name": "khandvi", "price": 7.5},
    {"name": "jalebi", "price": 5.0},
    {"name": "fafda", "price": 4.5},
]
def by(field):
    def getter(p):
        return p[field]
    return getter

by_price = by("price")
by_name = by("name")
print([p["name"] for p in sorted(products, key=by_price)])
print([p["name"] for p in sorted(products, key=by_name)])
print(by_price(products[0]), by_name(products[0]))
```

```output
['fafda', 'jalebi', 'dhokla', 'khandvi']
['dhokla', 'fafda', 'jalebi', 'khandvi']
6.0 dhokla
```

| call | field it remembers | getter(dhokla row) gives |
| --- | --- | --- |
| by("price") | price | 6.0 |
| by("name") | name | dhokla |

i assumed field would vanish once by() finished, since thats when its variables normally go away. but each getter carries its own field along, so by_price and by_name stay two different functions made by one.

one gotcha: the getter looks field up when it runs, not when it was built. build three small functions in a loop that each return the loop counter i and they all see its final value, so calling them gives 2, 2, 2.

---
prev: [337 functions as values, handing a function to another function](./337-functions-as-values-handing-a-function-to-another-function.md) | next: not written yet
