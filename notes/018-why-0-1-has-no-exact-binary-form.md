# 018: why 0.1 has no exact binary form
builds on: [003 counting in binary](./003-counting-in-binary.md), [017 fractions in binary, halves, quarters, eighths](./017-fractions-in-binary.md)
section: data at the atom level, part 18, ~2 min read

a computer asked to keep 0.1 doesnt keep 0.1, python shows what it really kept as 0.1000000000000000055511151231257827021181583404541015625 ([017](./017-fractions-in-binary.md) ended there). 0.1 is one digit long, so why cant it just keep it?

because written as a [binary fraction](./017-fractions-in-binary.md), binary carried past the point, 0.1 never ends. its digits repeat forever, like 1/3 in decimal. to get the [binary](./003-counting-in-binary.md) digits, double the number. if it reaches 1 or more, that digit is 1 and you subtract the 1. otherwise the digit is 0.

| step | start | doubled | digit | keep |
|---|---|---|---|---|
| 1 | 0.1 | 0.2 | 0 | 0.2 |
| 2 | 0.2 | 0.4 | 0 | 0.4 |
| 3 | 0.4 | 0.8 | 0 | 0.8 |
| 4 | 0.8 | 1.6 | 1 | 0.6 |
| 5 | 0.6 | 1.2 | 1 | 0.2 |
| 6 | 0.2 | 0.4 | 0 | 0.4 |

step 6 is step 2 again, so the block 0011 loops forever and 0.1 is 0.0 then 0011 again and again.

```python
from fractions import Fraction  # exact fractions, no rounding
x = Fraction(1, 10)
bits = ""
for _ in range(16):
    x = x * 2
    if x >= 1:
        bits += "1"
        x = x - 1
    else:
        bits += "0"
print("0." + bits)
```

```output
0.0001100110011001
```

i assumed a short number gets a short pattern, and it felt unfair that it doesnt. ten is 2 times 5, and binary only knows twos. a fraction, simplified, ends only when the number under its line is made of twos alone, like 1/2, 1/4, 3/8 (8 is 2 times 2 times 2). 1/10 has a 5 in it, so 0.1, 0.2 and 0.3 repeat.

a float, the usual way computers keep fractions, has a fixed number of places, so it cuts the loop off and rounds. thats the close neighbor python printed. python docs say the same: https://docs.python.org/3/tutorial/floatingpoint.html

the shop, the imaginary gujarati snack store these notes run on, got lucky with its prices. 7.50 and 4.50 end in a half, the rest are whole numbers. a 0.10 delivery fee wouldnt be, so money gets stored more carefully, in a later note.

### check yourself

1. which of these end in binary and which loop forever: 0.375, 0.2, 0.35, 0.0625?
<details><summary>answer</summary>

0.375 is 3/8 and 0.0625 is 1/16, so both end. 0.2 is 1/5 and 0.35 is 7/20 (20 is 2 times 2 times 5), so a 5 sits under the line in each, so they loop. the tempting answer is all four end because they have few decimal digits, but decimal digits dont decide it.

</details>

2. the shop sells 6 products at 6.00, 7.50, 5.00, 12.00, 3.00 and 4.50. this query keeps the prices that are a whole number of eighths, so exact in 3 binary places. how many of the 6 pass?
```sql
SELECT name, price FROM products WHERE price * 8 = round(price * 8);
```
<details><summary>answer</summary>

```result
name | price
dhokla | 6.00
khandvi | 7.50
jalebi | 5.00
kaju katli | 12.00
masala chai | 3.00
fafda | 4.50
```

all 6, because every price is a whole number or ends in .50, and a half is 4 eighths.

the tempting answer is fewer, from thinking cents like .50 are messy.

</details>

---
prev: [017 fractions in binary, halves, quarters, eighths](./017-fractions-in-binary.md) | next: [019 floating point, digits plus where the point sits](./019-floating-point.md)
