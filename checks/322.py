# checks for notes/322-encryption-in-transit-tls-and-https.md
n, public, private = 3233, 17, 413
assert n == 61 * 53 and (public * private) % 780 == 1  # same pair as 318
session = 77
sent = pow(session, public, n)
assert sent == 3123
assert pow(sent, private, n) == 77
sealed = bytes((b + session) % 256 for b in b"GET /orders?customer_id=1")
assert list(sealed[:6]) == [148, 146, 161, 109, 124, 188]
assert bytes((b - session) % 256 for b in sealed) == b"GET /orders?customer_id=1"
# source: https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Transport_Layer_Security
#   confirmed (opened this run): TLS secures HTTP, the result is HTTPS; handshake agrees a secret key; afterwards headers and bodies are encrypted with it
# source: https://www.rfc-editor.org/rfc/rfc8446.txt
#   confirmed (opened this run): TLS 1.3 removed static RSA cipher suites, key exchange uses (EC)DHE; TLS prevents eavesdropping
# audit: the note said a wire watcher never sees 77, which is false for the toy (3233 = 61 * 53 factors at once, so 413 and then 77 follow). it now says never once the numbers are real sizes
assert [k for k in range(2, 3233) if 3233 % k == 0][:1] == [53]
assert pow(sent, 413, 3233) == 77  # anyone who factors 3233 can rebuild 413 and read this
# audit: headers was used with no gloss for a reader landing cold; it now says headers are the extra lines, as note 308 defines them
# audit: the note said TLS is a short opening conversation, which equates TLS with its handshake. it now says TLS opens with one
# source: https://www.rfc-editor.org/rfc/rfc8446.txt
#   confirmed (opened this run): "TLS consists of two primary components: A handshake protocol ... A record protocol"
# audit: the old mdn url answers 301 and moves to the Defenses path; note and check now use the new url
#   confirmed (opened this run): "Client and server agree on a secret key" and "After the handshake, client and server use the secret key to encrypt and decrypt any messages, including HTTP headers as well as bodies"
# audit: the note glossed the URL as the text at the start naming the rules for talking, which defines the whole address as only its scheme. it now says the URL is the web address and its first part, the scheme, names the rules
from urllib.parse import urlsplit
assert urlsplit('https://shop.example/orders/101').scheme == 'https'  # note 307 shows scheme, host, path
