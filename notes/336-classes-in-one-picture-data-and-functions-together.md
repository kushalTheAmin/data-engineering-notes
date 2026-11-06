# 336: classes in one picture, data and functions together
builds on: [255 entities and attributes](./255-entities-and-attributes.md), [335 with, opening and closing things safely](./335-with-opening-and-closing-things-safely.md), [278 hash tables, how a dictionary finds a key without searching](./278-hash-tables-how-a-dictionary-finds-a-key-without-searching.md)
section: python for data work, part 12, ~2 min read

when you open a file in python you write f.write(...) and f.close(), and i never asked what f is. why do a files actions hang off the file itself?

a class is a blueprint that bundles data with the functions that work on that data. each thing you build from it is an object, the data is its attributes (a different thing from the column kind in [255](./255-entities-and-attributes.md)), and the functions are its methods.

the shop, the imaginary gujarati snack store these notes run on, has order 105 (2 kaju katli, a cashew fudge, at 12.00, 2 jalebi, a crisp syrupy swirl, at 5.00, and 1 masala chai at 3.00) and order 106 (2 khandvi, a gram flour roll, at 7.50). without a class you would keep each order in a [dictionary](./278-hash-tables-how-a-dictionary-finds-a-key-without-searching.md), pythons name to value lookup, plus a loose total function. a class glues them:

```python
class Order:
    def __init__(self, order_id, status, items):
        self.order_id = order_id
        self.status = status
        self.items = items

    def total(self):
        t = 0
        for price, qty in self.items:
            t += price * qty
        return t

o105 = Order(105, "delivered", [(12.0, 2), (5.0, 2), (3.0, 1)])
o106 = Order(106, "pending", [(7.5, 2)])
print(o105.status, o105.total())
print(o106.status, o106.total())
print(Order.total(o105))
```

```output
delivered 37.0
pending 15.0
37.0
```

__init__ (double underscores mark it special) runs when you build one, and self.status = status stores the value on the new object. i assumed o105.total() was a function living inside o105, but there is one total, kept on Order. o105.total() is shorthand for Order.total(o105), and o105 lands in the parameter self, the object it was called on. the data is per object, the code is shared. leave self out of the def and the call fails with "takes 0 positional arguments but 1 was given".

the file in [335](./335-with-opening-and-closing-things-safely.md) is an object of a class python ships with, and write and close are its methods.

---
prev: [335 with, opening and closing things safely](./335-with-opening-and-closing-things-safely.md) | next: not written yet
