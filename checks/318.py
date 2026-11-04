# checks for notes/318-public-and-private-keys-locking-without-sharing-a-secret.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
n = 3233
public, private = 17, 413
def lock(data, key):
    return [pow(b, key, n) for b in data]
assert n == 61 * 53
assert (public * private) % 780 == 1  # 780 = lcm(60, 52), the d from the wikipedia example
plain = "dhokla".encode()
assert list(plain) == [100, 104, 111, 107, 108, 97]
sealed = lock(plain, public)
assert sealed == [1773, 2170, 2185, 690, 745, 1632]
assert lock(sealed, public) == [1692, 2446, 3161, 1591, 840, 2398]
assert max(lock(sealed, public)) > 255  # not even bytes
assert bytes(lock(sealed, private)) == b"dhokla"
# anyone can find the factors of 3233 in a blink
assert [k for k in range(2, n) if n % k == 0][:1] == [53]
# check yourself 1
fafda = b"fafda"
assert con.sql("SELECT count(*) FROM products WHERE name = 'fafda'").fetchone() == (1,)
s2 = lock(fafda, public)
assert s2 == [1369, 1632, 1369, 1773, 1632]
assert lock(s2, public) == [2321, 2398, 2321, 1692, 2398]
assert bytes(lock(s2, private)) == b"fafda"
# check yourself 2: the public key cannot open what it locked (shown above)
# source: https://csrc.nist.gov/glossary/term/public_key_cryptography
#   confirmed (opened this run): two related keys, a public key and a private key; public freely provided, private kept secret
# source: https://en.wikipedia.org/wiki/RSA_cryptosystem
#   confirmed (opened this run): toy example n = 3233, e = 17, d = 413; keys typically 2048 to 4096 bits; padding added; message is almost always a single-use symmetric key
# source: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account
#   confirmed (opened this run): you add the public key to GitHub; the private key stays on your local machine (about-ssh page)
# equal bytes give equal numbers (toy weakness mentioned in the note)
assert lock([102, 102], public)[0] == lock([102, 102], public)[1]
assert 413 and 'fafda'.encode()[0] == 'fafda'.encode()[2]
# audit: the note said GitHub asks for the public half of your login key pair, which reads as always true, yet that page is about SSH keys only. it now says for SSH login
# source: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account
#   confirmed (opened this run): after you generate an SSH key pair, you must add the public key to GitHub
