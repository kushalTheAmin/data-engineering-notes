# checks for notes/306-dns-turning-names-into-addresses.md
import socket
assert socket.gethostbyname("localhost") == "127.0.0.1"
# 192.0.2.10 is the same example address 085 used
assert bytes(int(p) for p in "192.0.2.10".split(".")).hex(" ") == "c0 00 02 0a"
# source: https://www.rfc-editor.org/rfc/rfc1034
# confirmed: host name to host address translation, "one or more 32 bit IP addresses", and "a multiple address return is recommended"
# source: https://man7.org/linux/man-pages/man5/hosts.5.html
# confirmed: the hosts file is a simple text file that associates IP addresses with hostnames on the machine
# source: https://curl.se/libcurl/c/libcurl-errors.html
# confirmed: CURLE_COULDNT_RESOLVE_HOST (6) "Could not resolve host", separate from CURLE_COULDNT_CONNECT (7)
# source: https://www.rfc-editor.org/rfc/rfc2606
# confirmed: .example is reserved for use in documentation or as examples
print("306 ok")
