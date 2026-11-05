# 320: digital signatures, proof a message came from the key holder
builds on: [004 bytes, 8 bits and 256 possible values](./004-bytes.md), [277 hash functions, turning anything into a number in a fixed range](./277-hash-functions-turning-anything-into-a-number-in-a-fixed-range.md), [317 encryption, locking data so only a key opens it](./317-encryption-locking-data-so-only-a-key-opens-it.md), [318 public and private keys, locking without sharing a secret](./318-public-and-private-keys-locking-without-sharing-a-secret.md), [319 cryptographic hashes, a fingerprint you cant reverse](./319-cryptographic-hashes-a-fingerprint-you-cant-reverse.md)
section: talking over a network, part 15, ~2 min read

a [fingerprint](./319-cryptographic-hashes-a-fingerprint-you-cant-reverse.md), a short scrambled summary that changes if the message does, catches edits. but anyone can make one, so a thief can edit and re-fingerprint. how would you know the shop sent it?

a digital signature is the fingerprint locked with the private key, the half of a key pair you never share. anyone can check it with the public half, but only the private key holder could have made it, if that public key really is theirs. in [318](./318-public-and-private-keys-locking-without-sharing-a-secret.md) the public key locks and the private one opens; with textbook RSA, the toy kind used there, it also works backwards. here is the shop, the imaginary gujarati snack store these notes run on, signing with 318s toy keys. pow(b, key, n), the lock step, keeps the [remainder](./277-hash-functions-turning-anything-into-a-number-in-a-fixed-range.md) after dividing by n:

```python
import hashlib
n = 3233
public, private = 17, 413

def tiny_fp(text):
    return list(hashlib.sha256(text.encode()).digest()[:3])

def sign(text, key):
    return [pow(b, key, n) for b in tiny_fp(text)]

def check(text, sig, key):
    return [pow(s, key, n) for s in sig] == tiny_fp(text)

msg = "order 104 cancelled"
sig = sign(msg, private)
print(tiny_fp(msg))
print(sig)
print(check(msg, sig, public))
print(check("order 104 delivered", sig, public))
print(check(msg, sign(msg, public), public))
```

```output
[163, 167, 24]
[1089, 1163, 206]
True
False
False
```

checking opens it with the public key and compares to a fresh fingerprint of the text: True. swap one word and they stop matching: False. a thief with only the public key tries signing with it: False. i assumed the private key only ever opened things, but run backwards it makes something anyone can check.

it does not hide the message though. the text travels in plain view. the toy keeps 3 [bytes](./004-bytes.md) (groups of 8 bits) of the fingerprint, so it is forgeable. real ones sign all 32 with padding, and some key types sign without any lock step.

signed login tokens (JWTs) can use RSA plus SHA-256, named RS256 ([source](https://www.rfc-editor.org/rfc/rfc7518.txt)).

### check yourself

1. the shop signs "order 105 delivered" (Disha, 19:10). a thief changes the text to "order 105 cancelled" and keeps the signature. what does the check say, and why cant the thief just make a new signature?
<details><summary>answer</summary>

False. the fingerprint of the new text differs from the one inside the signature. a new signature needs the private key, and the thief has only the public one. the tempting answer is True, because the signature is still the shops.

```python
n = 3233
import hashlib
fp = lambda t: list(hashlib.sha256(t.encode()).digest()[:3])
sig = [pow(b, 413, n) for b in fp("order 105 delivered")]
check = lambda t: [pow(s, 17, n) for s in sig] == fp(t)
print(check("order 105 delivered"), check("order 105 cancelled"))
```

```output
True False
```

</details>

2. the shop wants to sign a 600000 character export of all its orders. does the lock step now run over 600000 numbers, or fewer? and what does signing cost grow with?
<details><summary>answer</summary>

the lock step runs over the fingerprint only, 32 bytes however big the export is. only making the fingerprint reads all 600000 characters, so cost grows with the export size through that one read, not through the locking. the tempting answer is 600000 locks, from picturing the whole message being locked (that is what 317 and 318 did to short messages, and the public key lock is the slow kind, so real systems use it on small things only).

</details>

---
prev: [319 cryptographic hashes, a fingerprint you cant reverse](./319-cryptographic-hashes-a-fingerprint-you-cant-reverse.md) | next: [321 certificates, proving whose public key it is](./321-certificates-proving-whose-public-key-it-is.md)
