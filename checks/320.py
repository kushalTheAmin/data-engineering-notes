# checks for notes/320-digital-signatures-proof-a-message-came-from-the-key-holder.md
import os, sys, hashlib
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
n = 3233
public, private = 17, 413
assert (public * private) % 780 == 1  # same toy keys as note 318
def tiny_fp(text):
    return list(hashlib.sha256(text.encode()).digest()[:3])
def sign(text, key):
    return [pow(b, key, n) for b in tiny_fp(text)]
def check(text, sig, key):
    return [pow(s, key, n) for s in sig] == tiny_fp(text)
msg = "order 104 cancelled"
assert con.sql("SELECT status FROM orders WHERE order_id = 104").fetchone() == ("cancelled",)
sig = sign(msg, private)
assert tiny_fp(msg) == [163, 167, 24]
assert sig == [1089, 1163, 206]
assert check(msg, sig, public) is True
assert check("order 104 delivered", sig, public) is False
assert check(msg, sign(msg, public), public) is False
assert len(hashlib.sha256(b"x").digest()) == 32  # real fingerprint is 32 bytes, toy keeps 3
assert all(b < n for b in tiny_fp(msg))  # each byte fits under n
# check yourself 1
assert con.sql("SELECT c.name, o.status FROM orders o JOIN customers c USING (customer_id) WHERE o.order_id = 105").fetchone() == ("Disha", "delivered")
assert con.sql("SELECT strftime(ordered_at, '%H:%M') FROM orders WHERE order_id = 105").fetchone() == ("19:10",)
s = sign("order 105 delivered", private)
assert check("order 105 delivered", s, public) is True
assert check("order 105 cancelled", s, public) is False
# check yourself 2: the fingerprint is 32 bytes whatever the input size (note 319)
import hashlib as _h
assert len(_h.sha256(b"dhokla"*100000).digest()) == 32 and len("dhokla"*100000) == 600000
assert msg.encode().decode() == msg
# source: https://www.rfc-editor.org/rfc/rfc7518.txt
#   confirmed (opened this run): RS256 is "RSASSA-PKCS1-v1_5 using SHA-256" (table in section 3.1, registry entry)
# source: https://en.wikipedia.org/wiki/Digital_signature
#   confirmed (opened this run): signatures made with a signing algorithm and private key pass verification with the corresponding public key
# audit: check yourself 2 asked what signing cost grows with but the answer never said. it now says the export size, through the one read that makes the fingerprint
