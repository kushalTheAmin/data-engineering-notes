# checks for notes/074-yaml-traps.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
import yaml

con = shop()
assert con.execute("SELECT note FROM order_notes WHERE order_id = 102").fetchone() == ("no nuts",)
assert con.execute("SELECT note FROM order_notes WHERE order_id = 105").fetchone() == ("gift, please wrap",)
assert con.execute("SELECT c.name FROM orders o JOIN customers c USING (customer_id) WHERE order_id = 105").fetchone() == ("Disha",)
def val(line):
    return list(yaml.safe_load(line).values())[0]
assert val("note: no nuts") == "no nuts"
assert val("gift_wrap: no") is False
assert val('gift_wrap: "no"') == "no"
assert val("gift_wrap: on") is True
assert val("gift_wrap: yes") is True
assert val("order_id: 102") == 102 and val('order_id: "102"') == "102"
assert val("lights: Off") is False and val('lights: "Off"') == "Off"
assert val("country: NO") is False and val('country: "NO"') == "NO"
assert val('a: Yes') is True and val('a: ON') is True and val('a: y') == 'y' and val('a: n') == 'n'
# source: https://yaml.org/type/bool.html
#   confirmed: YAML 1.1 bool regexp includes y|Y|yes|Yes|YES|n|N|no|No|NO|...|on|On|ON|off|Off|OFF
# source: https://yaml.org/spec/1.2.2/
#   confirmed: 1.2 core schema bool is only true|True|TRUE|false|False|FALSE, so yes stays a string
# source: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
#   confirmed: the alpha-2 code for Norway is NO
print("074 ok")
