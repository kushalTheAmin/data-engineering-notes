# checks for notes/317-encryption-locking-data-so-only-a-key-opens-it.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
def lock(data, key):
    return bytes((b + key) % 256 for b in data)
def unlock(data, key):
    return bytes((b - key) % 256 for b in data)
plain = "dhokla".encode()
sealed = lock(plain, 77)
assert list(plain) == [100, 104, 111, 107, 108, 97]
assert list(sealed) == [177, 181, 188, 184, 185, 174]
assert unlock(sealed, 77) == b"dhokla"
assert unlock(sealed, 78) == b"cgnjk`"
# toy has 256 possible keys (a key above 255 repeats one of them)
assert len({lock(plain, k) for k in range(1000)}) == 256
# check yourself 1
assert ord("E") == 69 and 69 + 200 == 269 and (69 + 200) % 256 == 13
assert con.sql("SELECT name FROM customers WHERE customer_id = 5").fetchone() == ("Esha",)
# check yourself 2: dhokla is a product, the wrong key result is not
names = {r[0] for r in con.sql("SELECT name FROM products").fetchall()}
assert "dhokla" in names and "cgnjk`" not in names
# source: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197-upd1.pdf
#   confirmed (opened this run): AES is capable of using cryptographic keys of 128, 192, and 256 bits
# 308 said real phones encrypt: that note's own text
# audit: the claim that one key locks and unlocks (symmetric encryption) had no source
# source: https://csrc.nist.gov/glossary/term/symmetric_key
#   confirmed (opened this run): a symmetric key is a single cryptographic key used with a symmetric-key algorithm, to encrypt and decrypt
