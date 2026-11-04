# checks for notes/311-status-codes-what-200-404-and-500-mean.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
# the toy slice: 101 delivered, 104 cancelled are real rows; 999 does not exist
rows = dict(con.execute("SELECT order_id, status FROM orders WHERE order_id IN (101, 104)").fetchall())
assert rows == {101: "delivered", 104: "cancelled"}
assert con.execute("SELECT count(*) FROM orders WHERE order_id = 999").fetchone()[0] == 0
# 107 exists, 108 does not
assert [r[0] for r in con.execute("SELECT order_id FROM orders WHERE order_id IN (107, 108)").fetchall()] == [107]
orders = {101: "delivered", 104: "cancelled"}
def shop_(path, database_up=True):
    if not database_up:
        return 500
    order_id = int(path.split("/")[-1])
    return 200 if order_id in orders else 404
assert [shop_("/orders/101"), shop_("/orders/104"), shop_("/orders/999"), shop_("/orders/101", False)] == [200, 200, 404, 500]
# source: https://www.rfc-editor.org/rfc/rfc9110.txt
# confirmed (section 15): the first digit of the status code defines the class; 2xx successful, 3xx redirection, 4xx client error, 5xx server error; 15.5.5 404 means no current representation found; 15.6.1 500 means an unexpected condition prevented fulfilling the request
# source: https://developer.mozilla.org/en-US/docs/Web/API/Window/fetch
# confirmed: a fetch() promise does not reject on HTTP error statuses like 404 or 504, a then() handler must check Response.ok or Response.status
# audit: check yourself 1 said the toy shop, but the toy server holds only 101 and 104, so it answers 404 for both 107 and 108, not 200 then 404. the question now says a shop holding the 7 real orders
assert [shop_("/orders/107"), shop_("/orders/108")] == [404, 404]
assert [200 if r in {107} else 404 for r in (107, 108)] == [200, 404]
print("311 ok")
# audit: the note said 404 means the server looked and found nothing. RFC 9110 15.5.5 says 404 means the origin server did not find a current representation or is not willing to disclose that one exists. the note now says found nothing, or wont say if anything is
# source: https://www.rfc-editor.org/rfc/rfc9110.txt
#   confirmed (opened this run, 15.5.5): the 404 status code indicates that the origin server did not find a current representation for the target resource or is not willing to disclose that one exists
