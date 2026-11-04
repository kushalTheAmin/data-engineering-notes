# 319: cryptographic hashes, a fingerprint you cant reverse
builds on: [004 bytes, 8 bits and 256 possible values](./004-bytes.md), [006 one byte, two hex digits](./006-one-byte-two-hex-digits.md), [042 line endings, the invisible characters that break files](./042-line-endings.md), [277 hash functions, turning anything into a number in a fixed range](./277-hash-functions-turning-anything-into-a-number-in-a-fixed-range.md)
section: talking over a network, part 14, ~2 min read

the toy hash in [277](./277-hash-functions-turning-anything-into-a-number-in-a-fixed-range.md) added up a words bytes, so "kholda" got the same result as dhokla, same letters in another order. what if a hash was built so any change at all scrambled the result?

a cryptographic hash is a [hash function](./277-hash-functions-turning-anything-into-a-number-in-a-fixed-range.md) (same input, same number out) built for three things: the output is always the same size, any change to the input scrambles it completely, and you cant work backwards from output to input. the output is a fingerprint. SHA-256 is a common one: 32 [bytes](./004-bytes.md), shown as 64 [hex](./006-one-byte-two-hex-digits.md) digits (two per byte). here are fingerprints of names from the shop, the imaginary gujarati snack store these notes run on (first 16 digits only):

```python
import hashlib

def fp(text):
    return hashlib.sha256(text.encode()).hexdigest()

for name in ["dhokla", "dhokla ", "Dhokla", "kholda"]:
    print(fp(name)[:16], repr(name))

big = "dhokla" * 100000
print(len(big), "characters ->", len(fp(big)), "hex digits")
```

```output
a19df0bccb680b96 'dhokla'
b038b568eeeefecb 'dhokla '
e6ad910e1dd95f8b 'Dhokla'
3f014d197d4e13e5 'kholda'
600000 characters -> 64 hex digits
```

a trailing space, a capital, the same letters reordered: four fingerprints that look unrelated. i kept expecting similar inputs to land near each other, but they land nowhere near. and 600000 characters in still gives 64 digits out.

it cant be reversed because the math only runs one way, and for big inputs like those 600000 characters most of the input is simply gone, squeezed into 32 bytes. one caveat: you can still guess. hash "dhokla", compare, and you know it matched, which is why short guessable inputs are weak.

git, the tool most devs save code with, by default names every object it stores by the SHA-1 hash (an older hash, same idea) of its content plus a small header, so a changed file gets a new name ([source](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)).

### check yourself

1. one export has the line "Asha" ending with a line feed, the other with a carriage return plus line feed ([042](./042-line-endings.md)). on screen they look identical. will the SHA-256 fingerprints match, and if not, will they differ by just a digit or two?
<details><summary>answer</summary>

they differ, and not slightly. the bytes differ (one extra invisible byte), so the fingerprint is unrelated. the tempting answers are "they match", because the files look the same, or a near match.

```python
import hashlib
fp = lambda s: hashlib.sha256(s.encode()).hexdigest()
print(fp("Asha\n")[:16])
print(fp("Asha\r\n")[:16])
```

```output
8a69cdaab31f2eb1
54a4fd54002ffa79
```

</details>

2. Asha and Esha both picked the password dhokla, and a site hashes each password as is and stores only the fingerprint. a thief reads the table. what can they tell, without reversing anything?
<details><summary>answer</summary>

the two stored values are identical, so they know Asha and Esha share a password. same input always gives the same fingerprint. real sites mix in a random extra value per user so this does not happen, but this one did not. the tempting answer is nothing, because fingerprints cant be reversed.

```python
import hashlib
fp = lambda s: hashlib.sha256(s.encode()).hexdigest()
print(fp("dhokla")[:16], fp("dhokla")[:16])
```

```output
a19df0bccb680b96 a19df0bccb680b96
```

</details>

---
prev: [318 public and private keys, locking without sharing a secret](./318-public-and-private-keys-locking-without-sharing-a-secret.md) | next: [320 digital signatures, proof a message came from the key holder](./320-digital-signatures-proof-a-message-came-from-the-key-holder.md)
