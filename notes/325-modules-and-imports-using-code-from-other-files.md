# 325: modules and imports, using code from other files
builds on: [324 capstone, one shop order fetched from an API, hop by hop](./324-capstone-one-shop-order-fetched-from-an-api-hop-by-hop.md), [039 a file is a named list of bytes](./039-a-file-is-a-named-list-of-bytes.md)
section: python for data work, part 1, ~2 min read

[324](./324-capstone-one-shop-order-fetched-from-an-api-hop-by-hop.md) had a report script fetching order 101, and now an email script needs the same order total. copy paste the function, and the day the price rule changes you fix one copy and forget the other. how do two scripts share code?

a module is just a python file, and import runs that file once and hands your code the names it made. here is the shop, the imaginary gujarati snack store these notes run on, with two [files](./039-a-file-is-a-named-list-of-bytes.md) in one folder:

```text
shop_utils.py
    print("loading shop_utils")
    PRICES = {"dhokla": 6.00, "masala chai": 3.00}
    def line_total(name, qty):
        return PRICES[name] * qty

report.py
    import shop_utils
    import shop_utils
    print(shop_utils.line_total("dhokla", 2) + shop_utils.line_total("masala chai", 2))
```

running report.py prints:

```text
loading shop_utils
18.0
```

the module name is the file name without .py. `import shop_utils` ran that file top to bottom, which is why the print fired, then gave report.py a name, shop_utils, holding PRICES and line_total. 18.0 is order 101: 2 dhokla at 6.00 and 2 masala chai (tea with milk and spices) at 3.00. `from shop_utils import line_total` skips the prefix.

i expected the second import to print again, but it didnt. python remembers a module after the first import and just reuses it. the flip side is that anything sitting at the top of the file, outside a function, runs the moment someone imports it, so a module that calls an API up there fires on import.

and python looks in the scripts own folder before the modules that come with python ([python docs](https://docs.python.org/3/tutorial/modules.html)). name your file json.py and `import json` quietly loads yours. its a confusing way for a script to crash.

next up is running these files from the terminal.

---
prev: [324 capstone, one shop order fetched from an API, hop by hop](./324-capstone-one-shop-order-fetched-from-an-api-hop-by-hop.md) | next: [326 running a python script from the terminal](./326-running-a-python-script-from-the-terminal.md)
