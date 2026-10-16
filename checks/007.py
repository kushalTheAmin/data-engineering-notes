# checks for notes/007-text-is-numbers.md
for ch, n, hx in [("2", 50, "32"), ("A", 65, "41"), ("a", 97, "61"), (" ", 32, "20")]:
    assert ord(ch) == n and format(n, "02x") == hx
assert "2" + "2" == "22" and 2 + 2 == 4
assert sorted(["10", "9", "2"]) == ["10", "2", "9"]
assert ord("1") == 49 and ord("2") == 50 and ord("9") == 57
assert "Asha" != "asha"
# a typical text file is utf-8 or ascii, where 2 is the single byte 0x32; utf-16 would store it as two bytes
assert "2".encode("utf-8") == b"\x32" and "2".encode("utf-16-le") == b"\x32\x00"
print("007 ok")
