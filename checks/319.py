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
# audit: the note said git names every object by SHA-1, but git can also make repositories that use SHA-256 (git init --object-format=sha256 gives 64 hex digit names). it now says by default
# source: https://git-scm.com/docs/hash-function-transition
#   confirmed (opened this run): the git project picked SHA-256 as the successor to SHA-1 and a repository can be transitioned one at a time; a git 2.43 sha256 repository printed 64 hex digit object names, a default one 40
# source: https://devclass.com/2022/06/23/vs-code-react-git-dominant-technologies-increase-their-grip-says-stack-overflow-survey
#   confirmed (opened this run): in the Stack Overflow 2022 survey, 96.65 percent of professionals use Git, SVN second at 5.96 percent (backs "the tool most devs save code with")
