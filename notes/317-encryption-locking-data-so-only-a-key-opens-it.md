# 317: encryption, locking data so only a key opens it
builds on: [004 bytes, 8 bits and 256 possible values](./004-bytes.md), [007 text is numbers, one character and one number](./007-text-is-numbers.md), [277 hash functions, turning anything into a number in a fixed range](./277-hash-functions-turning-anything-into-a-number-in-a-fixed-range.md)
section: talking over a network, part 12, ~2 min read

[308](./308-request-and-response-one-message-out-one-message-back.md) said real phones encrypt their requests, and i pictured something magical. what does scrambled data even look like, and what unscrambles it?

encryption turns [bytes](./004-bytes.md) (groups of 8 bits) into other bytes using a key, a secret number, so only someone holding the key can turn them back. this key is not a primary key or an [API key](./314-api-keys-a-password-for-programs.md), it just feeds the lock. here is a toy lock for "dhokla", a steamed savory cake from the shop, the imaginary gujarati snack store these notes run on. each [character is a number](./007-text-is-numbers.md), and % is the [remainder](./277-hash-functions-turning-anything-into-a-number-in-a-fixed-range.md) so a byte wraps at 256:

```python
def lock(data, key):
    return bytes((b + key) % 256 for b in data)

def unlock(data, key):
    return bytes((b - key) % 256 for b in data)

plain = "dhokla".encode()
sealed = lock(plain, 77)
print(list(plain))
print(list(sealed))
print(unlock(sealed, 77))
print(unlock(sealed, 78))
```

```output
[100, 104, 111, 107, 108, 97]
[177, 181, 188, 184, 185, 174]
b'dhokla'
b'cgnjk`'
```

the sealed bytes are still just bytes, nothing special. the same key undoes it, which is called symmetric encryption: one key locks and unlocks.

i expected the wrong key to throw an error, but 78 hands back cgnjk and a backtick with total confidence. nothing complains, you only notice because it looks like garbage.

this toy has 256 possible keys, so anyone could try them all in a blink. real ones like AES, a widely used standard, take keys of 128, 192 or 256 bits, far too many to try. but how do both sides get the same key without sending it in the open? the next one is about that.

### check yourself

1. the shop locks customer names with this toy and the key 200. what number does the first byte of "Esha" become?
<details><summary>answer</summary>

it becomes 13. E is 69, 69 + 200 is 269, and a byte holds at most 255, so it wraps to 13. the tempting answer is 269, from forgetting the wrap.

```python
print((ord("E") + 200) % 256)
```

```output
13
```

</details>

2. a loader unlocks product names with a key that is off by one, and no error appears. how could it still catch the problem?
<details><summary>answer</summary>

check the result after unlocking, like whether each name exists in products: dhokla does, cgnjk and a backtick does not. the tempting answer is to wait for an exception, but the toy happily returns wrong bytes.

</details>

---
prev: [316 OAuth in one picture, a token without the password](./316-oauth-in-one-picture-a-token-without-the-password.md) | next: not written yet
