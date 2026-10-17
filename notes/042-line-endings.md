# 042: line endings, the invisible characters that break files
builds on: [004 bytes, 8 bits and 256 possible values](./004-bytes.md), [006 one byte, two hex digits](./006-one-byte-two-hex-digits.md), [007 text is numbers, one character and one number](./007-text-is-numbers.md), [039 a file is a named list of bytes](./039-a-file-is-a-named-list-of-bytes.md), [041 text files vs binary files](./041-text-files-vs-binary-files.md)
section: memory, disks and files, part 8, ~2 min read

you filter a status column for `delivered`, every row on screen says delivered, and you get zero matches. what is hiding in the file?

a line ending is the character, or two, marking where one line stops and the next starts. [041](./041-text-files-vs-binary-files.md) said a text file is bytes that decode as characters, and a line break is one of those characters, just invisible.

the shop, the imaginary gujarati snack store these notes run on, has orders 101 and 102. as a tiny csv (text rows split by commas) that is two lines, `101,delivered` and `102,delivered`. here is how the end of each line is stored, as [bytes](./004-bytes.md) shown in [hex](./006-one-byte-two-hex-digits.md):

| style | ends each line with | hex | the 2 line file |
|---|---|---|---|
| LF, line feed | 1 character | 0a | 28 bytes |
| CRLF, carriage return then line feed | 2 characters | 0d 0a | 30 bytes |

linux and mac files normally use LF, and windows files often use CRLF. the names come from typewriters, where return slid the carriage back. i expected one line break to be one thing, so two bytes for the same job felt backwards.

now read a CRLF file with a tool that only knows LF (written \n in python, b means bytes):

```python
data = b"101,delivered\r\n102,delivered\r\n"
status = data.split(b"\n")[0].split(b",")[1]
print(status, status == b"delivered")
```

```output
b'delivered\r' False
```

the split cut at the 0a and left the 0d, written \r, glued to the end of the last column. it looks the same on screen and never equals the clean word.

the classic bug is a windows export landing on a linux server: every last column carries a hidden \r, so filters and joins quietly find nothing. python text mode hides it by turning every ending into \n, so the same file can behave differently in two tools.

### check yourself

1. the 7 shop orders are saved as `order_id,status` lines, one per order, each line ending included. how many bytes bigger is the CRLF version than the LF version?
<details><summary>answer</summary>

seven. every line gets exactly one extra byte, the 0d, and there are 7 lines. the tempting answer is 14, from counting both bytes of CRLF as extra, but the 0a is in both files.

</details>

2. same 7 lines, orders 101 to 107 in that order, in CRLF, but the file has no line break after the last line. you read it as bytes, split at 0a and keep rows whose status equals `delivered` exactly. 5 orders are delivered, including 107. how many match, and which?
<details><summary>answer</summary>

just one, order 107. the first six lines each end in a hidden 0d, so none equal `delivered`. the last line has no ending at all, so it is clean. the tempting answers are 5, from trusting the screen, and 0, from assuming every line is broken.

</details>

---
prev: [041 text files vs binary files](./041-text-files-vs-binary-files.md) | next: [043 reading start to end vs jumping to a spot](./043-reading-start-to-end-vs-jumping.md)
