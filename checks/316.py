# checks for notes/316-oauth-in-one-picture-a-token-without-the-password.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
# check yourself 1: the shop uses the customer saved with the token, not the url
tokens = {"t_x1": (1, "read orders")}
asked_customer = 2
customer = tokens["t_x1"][0]
assert customer == 1 != asked_customer
assert con.sql("SELECT order_id FROM orders WHERE customer_id = 1 ORDER BY order_id").fetchall() == [(101,), (103,), (106,)]
# the tempting answer is Bhavins orders
assert con.sql("SELECT order_id FROM orders WHERE customer_id = 2 ORDER BY order_id").fetchall() == [(101 + 1,), (107,)]
assert con.sql("SELECT name FROM customers WHERE customer_id = 2").fetchone() == ("Bhavin",)
assert con.sql("SELECT name FROM customers WHERE customer_id = 1").fetchone() == ("Asha",)
# the flow in the diagram has 7 messages, password goes to the shop only
flow = [("Asha", "app"), ("app", "Asha"), ("Asha", "shop"), ("shop", "Asha"), ("Asha", "app"), ("app", "shop"), ("shop", "app")]
assert len(flow) == 7
# source: https://www.rfc-editor.org/rfc/rfc6749.txt
#   confirmed (opened this run): 1.1/1.2 the client directs the resource owner to the authorization server, which obtains authorization and sends the code back; the owner only authenticates with the authorization server so credentials are never shared with the client
#   confirmed: 1 Introduction lists problems of sharing a password with third parties, including storing passwords and overly broad access
#   confirmed: 3.3 scope is the access range a token is issued for
#   confirmed: 4.1.2 the authorization code MUST expire shortly after it is issued, a maximum lifetime of 10 minutes is RECOMMENDED, and the client MUST NOT use it more than once
