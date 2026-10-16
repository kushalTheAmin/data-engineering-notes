# checks for notes/009-unicode.md
for ch, n, u in [("a", 97, "0061"), ("é", 233, "00E9"), ("ગ", 2711, "0A97"), ("ઢ", 2722, "0AA2"), ("🙂", 128578, "1F642")]:
    assert ord(ch) == n and format(n, "04X") == u
assert 0x10FFFF + 1 == 1114112
assert ord("a") == 97 and 2722 > 255
# codespace U+0000 to U+10FFFF, 172,808 characters defined in version 18.0, so over 150,000
# source: https://en.wikipedia.org/wiki/Unicode
print("009 ok")
