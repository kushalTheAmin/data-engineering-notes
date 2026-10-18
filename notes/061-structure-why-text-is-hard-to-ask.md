# 061: structure, why a pile of text is hard to ask questions of
builds on: [042 line endings, the invisible characters that break files](./042-line-endings.md), [056 grep, finding the lines that match](./056-grep-finding-matching-lines.md), [060 capstone, the life of one saved order, memory to disk and back](./060-capstone-the-life-of-one-saved-order.md)
section: giving data a shape, part 1, ~2 min read

how many dhokla did the shop sell? the answer is sitting right there in the text, and my code still got it wrong without a single error.

[060](./060-capstone-the-life-of-one-saved-order.md) ended with files that are just bytes and lines. [056](./056-grep-finding-matching-lines.md) showed the cost: grep 1 matched all 7 orders because it has never heard of a column. structure is an agreement about where each fact sits, so a program can find it without understanding the sentence.

here are three messages about dhokla (a steamed savory cake) orders at the shop, the imaginary gujarati snack store these notes run on. quantities are real, wording made up. each message is one [line](./042-line-endings.md). my rule: the quantity is the word just before dhokla.

| message | word before dhokla | found | real |
|---|---|---|---|
| Asha: 2 dhokla, 2 masala chai | 2 | 2 | 2 |
| Chirag wants dhokla x3 | wants | nothing | 3 |
| 1 dhokla and 1 jalebi for Bhavin | 1 | 1 | 1 |

now the same facts as rows, one line each, with a fixed spot for order id, product and quantity, commas between. the code prints the messages total, then the rows total:

```python
messages = ["Asha: 2 dhokla, 2 masala chai",
            "Chirag wants dhokla x3",
            "1 dhokla and 1 jalebi for Bhavin"]
found = 0
for m in messages:
    words = m.replace(",", "").split()
    before = words[words.index("dhokla") - 1]
    if before.isdigit():
        found += int(before)

rows = ["101,dhokla,2", "101,masala chai,2", "104,dhokla,3",
        "107,dhokla,1", "107,jalebi,1"]
total = 0
for row in rows:
    order, product, quantity = row.split(",")
    if product == "dhokla":
        total += int(quantity)
print(found, total)
```

```output
3 6
```

the messages give 3, the rows give 6, and 6 is right. the wrong total came back looking completely normal, and that is what i keep thinking about. the rows win because the quantity always sits after the second comma, so the code never reads the sentence at all.

you may have shipped a total like that. one caveat, the agreement only holds while everyone keeps it, and a comma inside a value, like a product called "chai, masala", would already break it.

the usual agreement for rows like these has a name, csv, and it is next.

---
prev: [060 capstone, the life of one saved order, memory to disk and back](./060-capstone-the-life-of-one-saved-order.md) | next: [062 CSV, rows and columns separated by commas](./062-csv-rows-and-columns-separated-by-commas.md)
