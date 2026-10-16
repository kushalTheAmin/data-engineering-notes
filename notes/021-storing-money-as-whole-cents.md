# 021: storing money as whole cents
builds on: [015 integer sizes, 8, 16, 32 and 64 bit numbers](./015-integer-sizes.md), [019 floating point, digits plus where the point sits](./019-floating-point.md), [020 why 0.1 + 0.2 is not exactly 0.3](./020-why-0-1-plus-0-2-is-not-0-3.md)
section: data at the atom level, part 21, ~2 min read

add a 10 cent delivery fee on three orders in python and you get 0.30000000000000004, not 0.30. thats the [0.1 + 0.2 problem](./020-why-0-1-plus-0-2-is-not-0-3.md) again, because a [float](./019-floating-point.md), digits plus a sliding point, only keeps a close neighbor of 0.10.

so money doesnt go in floats. you store whole cents: an integer, a whole number, holding the price times 100 (for money with 2 decimals). the shop, the imaginary gujarati snack store these notes run on, has 6 products, here they are as cents. SELECT asks for columns, FROM names the table, and ::INTEGER turns the result into a whole number:

```sql
SELECT name, price, (price * 100)::INTEGER AS cents FROM products;
```

```result
name | price | cents
dhokla | 6.00 | 600
khandvi | 7.50 | 750
jalebi | 5.00 | 500
kaju katli | 12.00 | 1200
masala chai | 3.00 | 300
fafda | 4.50 | 450
```

and the fee problem from the top, both ways:

```python
print(sum([0.10] * 3))
print(sum([10] * 3))
```

```output
0.30000000000000004
30
```

integers add exactly, so 10 + 10 + 10 is 30 every time and nothing gets rounded. you only turn cents back into a price when a human looks at it: 1200 // 100 is 12 (whole number divide) and 1200 % 100 is 0 (the remainder). i assumed money needed some special clever type, but the trick is just moving the point two places once, up front. discounts and splits still need a rounding rule, see below. an exact decimal type is the other option.

some payment APIs work this way. Stripe wants 1099 to charge 10.99 USD, and 10 to charge 10 JPY, since yen has no cents: https://docs.stripe.com/currencies#zero-decimal

one gotcha: a 32 bit [integer](./015-integer-sizes.md), one with 4 bytes of room, tops out at 2147483647 cents, which is 21,474,836.47 in money, and a total past that errors out. a 64 bit BIGINT fixes it.

### check yourself

1. a 15 percent discount on khandvi, which is 750 cents. in python, 750 * 15 // 100 gives 112 for the discount. whats the catch, and is 112 or 113 right?
<details><summary>answer</summary>

the exact answer is 112.5 cents, and an integer cant hold half a cent. // just chops it to 112, but whether 112 or 113 is right is a rule your business has to pick (round half up, round to even, always chop). the tempting answer is that 112 is simply correct, but it only looks that way because the chop was silent. write the rule down, because it repeats on every order.

</details>

2. order 105 in the shop has 2 kaju katli at 1200 cents, 2 jalebi at 500 and 1 masala chai at 300. whats the total in cents, and how do you show it as a price?
<details><summary>answer</summary>

2 * 1200 + 2 * 500 + 1 * 300 = 3700 cents. show it with 3700 // 100 for 37 and 3700 % 100 for 00, so 37.00. the tempting answer is 2000, from adding the three prices and forgetting quantity. cents fix the rounding, not the multiplying.

</details>

---
prev: [020 why 0.1 + 0.2 is not exactly 0.3](./020-why-0-1-plus-0-2-is-not-0-3.md) | next: [022 exact decimal types](./022-exact-decimal-types.md)
