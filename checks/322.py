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
# source: https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security
#   confirmed (opened this run): TLS secures HTTP, the result is HTTPS; handshake agrees a secret key; afterwards headers and bodies are encrypted with it
# source: https://www.rfc-editor.org/rfc/rfc8446.txt
#   confirmed (opened this run): TLS 1.3 removed static RSA cipher suites, key exchange uses (EC)DHE; TLS prevents eavesdropping
# audit: the note said a wire watcher never sees 77, which is false for the toy (3233 = 61 * 53 factors at once, so 413 and then 77 follow). it now says never once the numbers are real sizes
assert [k for k in range(2, 3233) if 3233 % k == 0][:1] == [53]
assert pow(sent, 413, 3233) == 77  # anyone who factors 3233 can rebuild 413 and read this
