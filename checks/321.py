# checks for notes/321-certificates-proving-whose-public-key-it-is.md
import os, sys, hashlib
sys.path.insert(0, os.path.dirname(__file__))
n, public, private = 2773, 17, 157
assert n == 47 * 59
assert (public * private) % ((47 - 1) * (59 - 1)) == 1  # CA toy keys are a valid pair
def tiny_fp(text):
    return list(hashlib.sha256(text.encode()).digest()[:3])
def sign(text, key):
    return [pow(b, key, n) for b in tiny_fp(text)]
def check(text, sig, key):
    return [pow(s, key, n) for s in sig] == tiny_fp(text)
cert = "shop.example 17 3233"
sig = sign(cert, private)
assert check(cert, sig, public) is True
assert check("shop.example 7 6767", sig, public) is False
assert check("shop.example 7 6767", sign("shop.example 7 6767", public), public) is False
assert 3233 == 61 * 53  # shop key modulus from note 318
# source: https://www.rfc-editor.org/rfc/rfc5280.txt
#   confirmed (opened this run): certificates bind public keys to subjects, a trusted CA signs each; fields include issuer, validity dates, subject, public key
# source: https://letsencrypt.org/docs/faq/
#   confirmed (opened this run): Lets Encrypt is a CA, its certificates trusted by most browsers and operating systems
# source: https://en.wikipedia.org/wiki/Public_key_certificate
#   confirmed (opened this run): all web browsers come with a built-in list of trusted root certificates
# audit: the note called a CA a company, but Lets Encrypt, named in the note, is a nonprofit
# source: https://letsencrypt.org/docs/faq/
#   confirmed (opened this run): "Let's Encrypt is a nonprofit"
# audit: the thief key was 5 with 6767, but 5 shares a factor with (67 - 1) * (101 - 1) = 6600, so no private key exists for it. it is now 7 with 6767, a valid public key
from math import gcd
assert 6767 == 67 * 101 and gcd(7, 66 * 100) == 1 and (7 * pow(7, -1, 6600)) % 6600 == 1 and gcd(5, 6600) == 5
# source: https://en.wikipedia.org/wiki/Public_key_certificate
#   confirmed (opened this run): an intermediate certificate is not self-signed, only signs other certificates, and sits between a root and the end certificate in the chain of trust (backs "real checks often pass through a middle CA first")
