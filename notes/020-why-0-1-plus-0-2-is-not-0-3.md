# 020: why 0.1 + 0.2 is not exactly 0.3
builds on: [018 why 0.1 has no exact binary form](./018-why-0-1-has-no-exact-binary-form.md), [019 floating point, digits plus where the point sits](./019-floating-point.md)
section: data at the atom level, part 20, ~2 min read

python says 0.1 + 0.2 is 0.30000000000000004. i expected the two tiny cut off errors to cancel each other. why dont they?

because a [float](./019-floating-point.md), binary digits plus a count of where the point slides, keeps 0.1 and 0.2 as [close neighbors](./018-why-0-1-has-no-exact-binary-form.md), not the real values, and both neighbors are slightly too big. the add itself is exact on paper, but the exact answer isnt a float either, so it gets rounded again. python has an exact digits type called Decimal, so it can print what was really stored:

```python
from decimal import Decimal, getcontext
getcontext().prec = 60
print(Decimal(0.1) + Decimal(0.2))
print(Decimal(0.1 + 0.2))
print(Decimal(0.3))
print(0.1 + 0.2 == 0.3)
```

```output
0.3000000000000000166533453693773481063544750213623046875
0.3000000000000000444089209850062616169452667236328125
0.299999999999999988897769753748434595763683319091796875
False
```

line 1 is the exact sum of the two stored values. line 3 is what typing 0.3 gets you, a neighbor cut slightly low. floats near 0.3 sit about 0.00000000000000005 apart (the 17th place after the point), and line 1 lands exactly halfway between line 3 and line 2. a tie goes to the neighbor whose last stored digit is 0, and thats line 2.

so 0.1 + 0.2 and 0.3 are two different floats, one slot apart, and == says False. i was surprised its an exact tie, not just a near miss.

this is why you dont compare floats with ==. python docs suggest math.isclose, which says yes when two numbers agree to about 9 digits: https://docs.python.org/3/library/math.html#math.isclose. tests asserting a float total equals a typed number are a classic way for a build to break for no visible reason.

### check yourself

1. a test says total = 0.1 + 0.2 + 0.3, summed left to right, then asserts total == 0.6, and it fails with 0.6000000000000001. someone "fixes" it by writing 0.3 + 0.2 + 0.1 and it passes. is the bug fixed?
<details><summary>answer</summary>

no. the new order rounds in different spots and happens to land on the float 0.6 becomes, so the order matters even though the real sum doesnt. the same total can pass or fail by luck. the tempting answer is that order cant change a sum, but that holds for exact numbers, not for rounded ones. compare with math.isclose instead.

</details>

2. the shop, the imaginary gujarati snack store these notes run on, has 6 products. this query casts each price to a float (DOUBLE in the database these notes use) and asks if adding 0.1 then 0.2 equals adding 0.3. on paper all 6 rows pass. how many do?
```sql
SELECT name, price FROM products WHERE price::DOUBLE + 0.1 + 0.2 = price::DOUBLE + 0.3;
```
<details><summary>answer</summary>

```result
name | price
dhokla | 6.00
khandvi | 7.50
jalebi | 5.00
fafda | 4.50
```

4 pass. kaju katli (12.00) and masala chai (3.00) land a slot apart. you cant tell which from the algebra, only by running it. the tempting answer is 6.

</details>

---
prev: [019 floating point, digits plus where the point sits](./019-floating-point.md) | next: not written yet
