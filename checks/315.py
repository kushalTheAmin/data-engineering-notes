# checks for notes/315-tokens-that-expire-a-key-with-a-shelf-life.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
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
assert shop_api({"x-token": "t_a1"}, 100) == (200, "hello report script")
assert shop_api({"x-token": "t_a1"}, 4000) == (401, "token expired")
assert swap("r_9x", 4000) == "t_b2"
assert shop_api({"x-token": "t_b2"}, 4100) == (200, "hello report script")
assert shop_api({"x-token": "t_a1"}, 9000) == (401, "token expired")
# check yourself 1: issued at 4000, lasts 3600, expires at 7600
assert tokens["t_b2"][1] == 4000 + 3600 == 7600
assert shop_api({"x-token": "t_b2"}, 7599)[0] == 200
assert shop_api({"x-token": "t_b2"}, 7600) == (401, "token expired")
assert con.sql("SELECT order_id FROM orders WHERE customer_id = 1 ORDER BY order_id").fetchall() == [(101,), (103,), (106,)]
# check yourself 2: 5 days in seconds, and the refresh token still swaps
assert 5 * 24 * 3600 == 432000
assert swap("r_9x", 432000) == "t_b2"
# 3600 seconds is one hour
assert 3600 == 60 * 60

# 1.4 and 1.5 describe access and refresh tokens, 5.1 shows expires_in 3600 as one hour
# source: https://www.rfc-editor.org/rfc/rfc6749.txt
# audit: the note said an access token is the short lived one and a refresh token the long lived one, which reads as always true. RFC 6749 1.5 says access tokens "may have a shorter lifetime" than the grant, and 1.3.3 itself mentions a "long-lived access token". the note now says usually short lived and longer lived
# source: https://www.rfc-editor.org/rfc/rfc6749.txt
#   confirmed (opened this run): 1.5 refresh tokens are credentials used to obtain a new access token when the current one becomes invalid or expires; access tokens may have a shorter lifetime; 5.1 expires_in 3600 denotes the access token expires in one hour
