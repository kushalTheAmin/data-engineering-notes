# checks for notes/314-api-keys-a-password-for-programs.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
keys = {"k_report_7f3a": "report script"}
def shop_api(headers):
    who = keys.get(headers.get("x-api-key"))
    if who is None:
        return 401, "unknown caller"
    return 200, "hello " + who
assert shop_api({}) == (401, "unknown caller")
assert shop_api({"x-api-key": "k_report_7f3"}) == (401, "unknown caller")
assert shop_api({"x-api-key": "k_report_7f3a"}) == (200, "hello report script")
# key missing its last character fails the lookup
assert "k_report_7f3".__len__() == len("k_report_7f3a") - 1 and shop_api({"x-api-key": "k_report_7f3"})[0] == 401
# Esha (customer 5) exists and has no orders: valid caller, empty list (note 312)
assert con.execute("SELECT count(*) FROM customers WHERE customer_id = 5").fetchone()[0] == 1
assert con.execute("SELECT count(*) FROM orders WHERE customer_id = 5").fetchone()[0] == 0
# Asha is customer 1
assert con.execute("SELECT name FROM customers WHERE customer_id = 1").fetchone()[0] == "Asha"
# removing one entry cuts off that script only
keys2 = {"k_report_7f3a": "report script", "k_other": "other script"}
del keys2["k_report_7f3a"]
assert "k_other" in keys2 and "k_report_7f3a" not in keys2
# source: https://www.rfc-editor.org/rfc/rfc9110.txt
# confirmed: section 15.5.2 says 401 means the request lacks valid authentication credentials for the target resource
# source: https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning
# confirmed: secret scanning scans repositories for hardcoded credentials including API keys and passwords
print("314 ok")
# audit: the note said GitHub scanning flags only known kinds of keys, but the page says that is the default detection and generic patterns (such as generic API keys), custom patterns and AI-detected secrets can extend it. the note now says by default and likely slip past
# source: https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning
#   confirmed (opened this run): scans for hardcoded credentials including API keys, passwords, tokens, and other known secret types; beyond the default detection of partner and provider secrets, generic patterns expand detection to secrets not tied to a specific provider, such as generic API keys
