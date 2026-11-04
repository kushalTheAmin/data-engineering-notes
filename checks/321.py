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
assert check("shop.example 5 6767", sig, public) is False
assert check("shop.example 5 6767", sign("shop.example 5 6767", public), public) is False
assert 3233 == 61 * 53  # shop key modulus from note 318
# source: https://www.rfc-editor.org/rfc/rfc5280.txt
#   confirmed (opened this run): certificates bind public keys to subjects, a trusted CA signs each; fields include issuer, validity dates, subject, public key
# source: https://letsencrypt.org/docs/faq/
#   confirmed (opened this run): Lets Encrypt is a CA, its certificates trusted by most browsers and operating systems
# source: https://en.wikipedia.org/wiki/Public_key_certificate
#   confirmed (opened this run): all web browsers come with a built-in list of trusted root certificates
