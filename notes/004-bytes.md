# 004: bytes, 8 bits and 256 possible values
builds on: [001 data is facts written down](./001-data-is-facts-and-numbers.md), [002 bits, everything is a tiny switch](./002-bits.md), [003 counting in binary](./003-counting-in-binary.md)
section: data at the atom level, part 4, ~2 min read

why does a dotted ip address, the number a device goes by online, like 192.168.1.1, never have a part over 255? colors on screen usually stop at 255 too.

a byte is a group of 8 [bits](./002-bits.md), the tiny on/off switches, handled as one unit.

8 bits make 256 patterns ([002](./002-bits.md)), and read as numbers they start at 0 ([003](./003-counting-in-binary.md)). so one byte counts 0 to 255, the whole reason for the 255.

the shop, the imaginary snack store these notes run on, sells dhokla, a steamed savory cake. in [001](./001-data-is-facts-and-numbers.md) every letter got a number. each of those numbers fits in one byte, so here are the 6 bytes of "dhokla":

```python
for b in "dhokla".encode():
    print(b, format(b, "08b"))
```

```output
100 01100100
104 01101000
111 01101111
107 01101011
108 01101100
97 01100001
```

`.encode()` turns text into its bytes. 6 letters, 6 bytes, 8 switches each. the first, 01100100, has the 64, 32 and 4 places on, and 64 plus 32 plus 4 is 100. the zero on the left still counts, a byte is always 8 wide.

the gotcha: you cant fit 300 in one byte. python refuses, `bytes([300])` raises "bytes must be in range(0, 256)". bigger numbers need more bytes, a later note shows how.

thats why a typical screen color uses one byte each for red, green and blue: 256 times 256 times 256 is 16,777,216 colors. every part of a dotted ip address is one byte too.

i assumed 8 was a law of nature. its not, older machines used other sizes, 8 is just what everybody settled on.

### check yourself

1. the shop stores each product name one byte per character. how many bytes is "kaju katli", a cashew sweet?

<details><summary>answer</summary>

its 10. the space between the words gets its own number too (32), so it takes a byte. the tempting answer is 9, from counting only letters.

</details>

2. you want to store the number 1000 in bytes. how many do you need, and why isnt one enough?

<details><summary>answer</summary>

two. one byte tops out at 255, and 1000 needs 10 switches, so it spills into a second byte (16 switches reach 65,535). the tempting answer is 4, one byte per digit, which is what it costs if you store 1000 as text instead of as a number.

</details>

3. the shop numbers its products with one byte per id, starting at 0. how many different products can it ever have?

<details><summary>answer</summary>

its 256. ids run 0 to 255, and zero counts as a value. the tempting answer is 255, from reading the biggest id as the count.

</details>

---
prev: [003 counting in binary](./003-counting-in-binary.md) | next: [005 hexadecimal, counting with sixteen digits](./005-hexadecimal.md)
