# checks for notes/319-cryptographic-hashes-a-fingerprint-you-cant-reverse.md
import os, sys, hashlib
sys.path.insert(0, os.path.dirname(__file__))
fp = lambda s: hashlib.sha256(s.encode()).hexdigest()
assert [fp(n)[:16] for n in ["dhokla", "dhokla ", "Dhokla", "kholda"]] == ["a19df0bccb680b96", "b038b568eeeefecb", "e6ad910e1dd95f8b", "3f014d197d4e13e5"]
big = "dhokla" * 100000
assert len(big) == 600000 and len(fp(big)) == 64
assert len(hashlib.sha256(b"x").digest()) == 32  # 32 bytes = 64 hex digits
assert len({fp(n)[:16] for n in ["dhokla", "dhokla ", "Dhokla", "kholda"]}) == 4
# check yourself 1
assert fp("Asha\n")[:16] == "8a69cdaab31f2eb1" and fp("Asha\r\n")[:16] == "54a4fd54002ffa79"
assert len("Asha\r\n") - len("Asha\n") == 1
# check yourself 2
assert fp("dhokla") == fp("dhokla") and fp("dhokla")[:16] == "a19df0bccb680b96"
# source: https://en.wikipedia.org/wiki/SHA-2
#   confirmed (opened this run): SHA-256 digest is 256 bits
# source: https://git-scm.com/book/en/v2/Git-Internals-Git-Objects
#   confirmed (opened this run): git names stored content by the SHA-1 checksum of the content plus a header
