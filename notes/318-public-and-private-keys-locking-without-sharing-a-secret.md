# 318: public and private keys, locking without sharing a secret
builds on: [004 bytes, 8 bits and 256 possible values](./004-bytes.md), [007 text is numbers, one character and one number](./007-text-is-numbers.md), [277 hash functions, turning anything into a number in a fixed range](./277-hash-functions-turning-anything-into-a-number-in-a-fixed-range.md), [317 encryption, locking data so only a key opens it](./317-encryption-locking-data-so-only-a-key-opens-it.md)
section: talking over a network, part 13, ~2 min read

[317](./317-encryption-locking-data-so-only-a-key-opens-it.md) ended on a catch: both sides need the same key, so how does Chirag get one to the shop without a stranger reading it on the way?

the fix is to stop using one key. a key pair is two encryption keys made together, a public key you hand to anyone and a private key that never leaves home. what the public key locks, only the private key opens. that is asymmetric encryption, two different keys, unlike [symmetric](./317-encryption-locking-data-so-only-a-key-opens-it.md) (one key locks and unlocks). here are textbook numbers for "dhokla" from the shop, the imaginary gujarati snack store these notes run on. pow(b, key, n) multiplies key copies of b together, keeping the [remainder](./277-hash-functions-turning-anything-into-a-number-in-a-fixed-range.md) after dividing by n:

```python
n = 3233
public, private = 17, 413

def lock(data, key):
    return [pow(b, key, n) for b in data]

plain = "dhokla".encode()
sealed = lock(plain, public)
print(list(plain))
print(sealed)
print(lock(sealed, public))
print(bytes(lock(sealed, private)))
```

```output
[100, 104, 111, 107, 108, 97]
[1773, 2170, 2185, 690, 745, 1632]
[1692, 2446, 3161, 1591, 840, 2398]
b'dhokla'
```

the shop posts 17 and 3233 publicly and keeps 413 at home. Chirag locks with the public key. try it again and you get numbers above 255, too big for a [byte](./004-bytes.md) (a group of 8 bits). only 413, or 1193 in this toy, brings dhokla back. i assumed whoever locked a message could always undo it, but Chirag cant read his own.

so he can lock a fresh secret key for the shop, and only the shop opens it. this toy is unsafe: 3233 is 61 times 53, found in a blink, and equal bytes give equal numbers. real keys run 2048 bits or more, with random filler added.

for SSH (remote login), GitHub asks for the public half of your key pair, the private half stays on your machine.

### check yourself

1. Chirag locks "fafda" with the shop public key and gets [1369, 1632, 1369, 1773, 1632]. to check his work he unlocks it with the same public key. what comes back?
<details><summary>answer</summary>

not fafda, just numbers (and not even valid bytes). data locked with the public key opens only with the private key 413. the tempting answer is fafda, from thinking one key does both like in 317.

```python
n = 3233
sealed = [1369, 1632, 1369, 1773, 1632]
print([pow(c, 17, n) for c in sealed])
print(bytes(pow(c, 413, n) for c in sealed))
```

```output
[2321, 2398, 2321, 1692, 2398]
b'fafda'
```

</details>

2. a thief copies the shop public key off its website. does that let them read Chirags locked message?
<details><summary>answer</summary>

no, whatever the public key locks, only the private key opens. the thing to guard is the private key: whoever gets it can open every message locked to that public key. the tempting answer is yes, from treating the public key like a stolen password.

</details>

---
prev: [317 encryption, locking data so only a key opens it](./317-encryption-locking-data-so-only-a-key-opens-it.md) | next: [319 cryptographic hashes, a fingerprint you cant reverse](./319-cryptographic-hashes-a-fingerprint-you-cant-reverse.md)
