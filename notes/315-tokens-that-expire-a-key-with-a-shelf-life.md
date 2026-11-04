# 315: tokens that expire, a key with a shelf life
builds on: [025 unix time, seconds since 1970](./025-unix-time.md), [310 HTTP headers, notes attached to a request](./310-http-headers-notes-attached-to-a-request.md), [311 status codes, what 200, 404 and 500 mean](./311-status-codes-what-200-404-and-500-mean.md), [312 APIs, a door built for programs](./312-apis-a-door-built-for-programs.md), [314 API keys, a password for programs](./314-api-keys-a-password-for-programs.md)
section: talking over a network, part 10, ~2 min read

a leaked [API key](./314-api-keys-a-password-for-programs.md) (a secret string a program sends) works until someone deletes its entry. so what if the string killed itself?

a token is a key the server hands out with an expiry time saved beside it (in this toy, anyway). an access token is usually the short lived one, and a refresh token is the longer lived one that can only be swapped for a new access token. the shop, the imaginary gujarati snack store these notes run on, has an [API](./312-apis-a-door-built-for-programs.md) (requests it promises to answer) that works like this. now counts seconds, like [unix time](./025-unix-time.md) (seconds since 1970), and starts at 0 when t_a1 is handed out:

```python
tokens = {"t_a1": ("report script", 3600)}
refresh = {"r_9x": "report script"}

def shop_api(headers, now):
    t = tokens.get(headers.get("x-token"))
    if t is None:
        return 401, "unknown caller"
    if now >= t[1]:
        return 401, "token expired"
    return 200, "hello " + t[0]

def swap(refresh_token, now):
    who = refresh.get(refresh_token)
    if who is None:
        return None
    tokens["t_b2"] = (who, now + 3600)
    return "t_b2"

print(shop_api({"x-token": "t_a1"}, 100))
print(shop_api({"x-token": "t_a1"}, 4000))
print(swap("r_9x", 4000))
print(shop_api({"x-token": "t_b2"}, 4100))
print(shop_api({"x-token": "t_a1"}, 9000))
```

```output
(200, 'hello report script')
(401, 'token expired')
t_b2
(200, 'hello report script')
(401, 'token expired')
```

i assumed expiring meant the server had to go delete things, but its one comparison, now against a number saved with the token. t_a1 died at second 3600 and nobody touched it. at 4000 the script showed r_9x, got t_b2, and carried on. the last line is a stranger holding the old t_a1, who gets a [401](./311-status-codes-what-200-404-and-500-mean.md) (not let in, here because the token ran out).

you might spot the catch already, the refresh token lives long, so a leaked one is as bad as a leaked key from 314. it only gets sent to the swap door though, not on every request. OAuth 2.0 (RFC 6749, the standard for handing out tokens) describes both kinds, and its example answer has expires_in 3600, one hour. real servers make a new token each swap, ours always says t_b2.

### check yourself

1. the script holds t_b2, which was issued at second 4000 and lasts 3600 seconds. it asks for Ashas order ids at second 7600. what does it get, and what about second 7599?
<details><summary>answer</summary>

7600 gets 401 token expired, because the check is now >= 7600. 7599 gets 200, and the API runs:

```sql
SELECT order_id FROM orders WHERE customer_id = 1 ORDER BY order_id
```

```result
order_id
101
103
106
```

the tempting answer is 200 for both, from reading "lasts until 7600" as including 7600.

</details>

2. r_9x gets pasted into a public repo. a stranger finds it 5 days later (432000 seconds). what can they do, and what is the fix?
<details><summary>answer</summary>

they can call swap and get a fresh access token, because the toy refresh token never expires. the fix is deleting the entry from refresh, and any access token it already made lives until its time is up. the tempting answer is that nothing works after 5 days since tokens expire, but only access tokens do.

</details>

---
prev: [314 API keys, a password for programs](./314-api-keys-a-password-for-programs.md) | next: not written yet
