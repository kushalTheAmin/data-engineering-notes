# 314: API keys, a password for programs
builds on: [086 client and server, you ask, the database answers](./086-client-and-server.md), [310 HTTP headers, notes attached to a request](./310-http-headers-notes-attached-to-a-request.md), [311 status codes, what 200, 404 and 500 mean](./311-status-codes-what-200-404-and-500-mean.md), [312 APIs, a door built for programs](./312-apis-a-door-built-for-programs.md), [313 JSON over HTTP, the answer is text until you parse it](./313-json-over-http-the-answer-is-text-until-you-parse-it.md)
section: talking over a network, part 9, ~2 min read

in [313](./313-json-over-http-the-answer-is-text-until-you-parse-it.md) the report script got Ashas orders as JSON, but nothing in that request said who was asking. so what stops a stranger typing the same GET?

an API key is a random string the shop hands to one program, and the program sends it in a [header](./310-http-headers-notes-attached-to-a-request.md) (a Name: value line) on every request. the [server](./086-client-and-server.md) (the program answering) looks it up. no match usually gets a 401, a [status code](./311-status-codes-what-200-404-and-500-mean.md) meaning the server doesnt know who you are. the shop, the imaginary gujarati snack store, has an [API](./312-apis-a-door-built-for-programs.md) (requests it promises to answer) that checks like this:

```python
keys = {"k_report_7f3a": "report script"}

def shop_api(headers):
    who = keys.get(headers.get("x-api-key"))
    if who is None:
        return 401, "unknown caller"
    return 200, "hello " + who

print(shop_api({}))
print(shop_api({"x-api-key": "k_report_7f3"}))
print(shop_api({"x-api-key": "k_report_7f3a"}))
```

```output
(401, 'unknown caller')
(401, 'unknown caller')
(200, 'hello report script')
```

the header name x-api-key is the shops own pick, and the toy assumes names arrive lowercase, like the dictionary in 310. i assumed a key was something clever, but its a dictionary lookup, the server just remembers which string it gave to whom. one wrong character gets the same 401 as no key.

each program has its own entry, so deleting one cuts off that script alone.

the gotcha: with a plain key the server cant tell the real script from a copy. whoever holds the string is the script. so a key typed into code pushed to a public repo (a project folder anyone can read) is a door left open. GitHub scanning by default flags known kinds of keys, so ours would likely slip past. keep keys out of code, and if one leaks, delete its entry, since removing the line later doesnt unpublish it.

### check yourself

1. the report scripts key k_report_7f3a gets pasted into a public repo, and a stranger sends GET /orders?customer_id=1 with it. what does the shop API answer, and what is the fix?
<details><summary>answer</summary>

it answers 200 and Ashas orders, because the lookup finds the key and cant tell who sent it. the fix is deleting that entry and giving the script a new key. the tempting answer is 401 because the sender is a stranger, but the server only knows the string.

</details>

2. the report script sends GET /orders?customer_id=1 with its key missing the last character. what status does it get, and does the database run Ashas query?
<details><summary>answer</summary>

401, and no. the lookup fails first, so the request never reaches the database. the tempting answer is 404 from 311, but that is for a thing that doesnt exist, here the caller is unknown.

</details>

---
prev: [313 JSON over HTTP, the answer is text until you parse it](./313-json-over-http-the-answer-is-text-until-you-parse-it.md) | next: [315 tokens that expire, a key with a shelf life](./315-tokens-that-expire-a-key-with-a-shelf-life.md)
