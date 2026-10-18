# 067: JSON types, strings, numbers, booleans, null, objects and arrays
builds on: [020 why 0.1 + 0.2 is not exactly 0.3](./020-why-0-1-plus-0-2-is-not-0-3.md), [021 storing money as whole cents](./021-storing-money-as-whole-cents.md), [023 true and false, the boolean](./023-true-and-false-the-boolean.md), [031 null, a marker for a missing value](./031-null.md), [066 JSON, records with names on every value](./066-json-records-with-names-on-every-value.md)
section: giving data a shape, part 7, ~2 min read

i pasted a python dictionary into a JSON file and the program reading it choked on True. so what exactly is allowed in there?

in [066](./066-json-records-with-names-on-every-value.md) every value in a JSON record got a name. the value after a name can be one of six kinds, and only six: a string in double quotes, a number, true or false (a [boolean](./023-true-and-false-the-boolean.md), a two state value), null (a [marker](./031-null.md) for no value), an object (curly braces, like a python dictionary) and an array (square brackets, like a python list).

here is order 103 from the shop, the imaginary gujarati snack store these notes run on, with all six kinds in it, and what python makes of every value (json.loads turns JSON text into python values):

```python
import json
text = '{"order_id": 103, "customer": {"name": "Asha", "city": "Jersey City"}, "items": ["khandvi", "masala chai"], "total": 10.5, "delivered": true, "stars": null}'
for name, value in json.loads(text).items():
    print(name, type(value).__name__, value)
```

```output
order_id int 103
customer dict {'name': 'Asha', 'city': 'Jersey City'}
items list ['khandvi', 'masala chai']
total float 10.5
delivered bool True
stars NoneType None
```

in the file its lowercase true and null, python spells them True and None, and True in the file is an error. stars is null because 103 has no rating in the shop data.

i expected a date to be its own type, and there isnt one. ordered_at in 066 is just a string, and your code has to know. also JSON only says number: python made 103 an int and 10.5 a float because of the dot, thats python choosing. when a number like 0.1 gets loaded as a float it has the [float problem](./020-why-0-1-plus-0-2-is-not-0-3.md) again, tiny rounding errors in decimals, which is one reason to send money as [whole cents](./021-storing-money-as-whole-cents.md), 1050 instead of 10.50.

### check yourself

1. someone types `{"delivered": True}` into a file by hand and a program reads it with json.loads. what happens, and why?
<details><summary>answer</summary>

it raises an error. JSON spells the boolean in lowercase, true, and True is not a JSON word at all. the tempting answer is that it loads as True, since python prints that, but python is reading JSON text here, not python.

</details>

2. Esha has no city in the shop. one saved copy of the data writes `"city": null` and another writes `"city": "null"`. for which one is the loaded value None?
<details><summary>answer</summary>

only the first. the second has quotes, so its a string of 4 characters, n u l l, and the city looks present. the tempting answer is both, from reading the quotes as decoration.

</details>

---
prev: [066 JSON, records with names on every value](./066-json-records-with-names-on-every-value.md) | next: [068 nesting, records and lists inside records](./068-nesting.md)
