# checks for notes/072-xml.md
import json, os, sys
import xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
assert con.execute("SELECT c.name FROM orders o JOIN customers c USING (customer_id) WHERE order_id = 103").fetchone() == ("Asha",)
assert con.execute("""SELECT p.name, i.quantity FROM order_items i JOIN products p USING (product_id)
  WHERE order_id = 103 ORDER BY p.name""").fetchall() == [("khandvi", 1), ("masala chai", 1)]
text = "<order><order_id>103</order_id><customer>Asha</customer><item><product>khandvi</product><quantity>1</quantity></item><item><product>masala chai</product><quantity>1</quantity></item></order>"
order = ET.fromstring(text)
assert order.find("customer").text == "Asha"
items = order.findall("item")
assert len(items) == 2
assert [(i.find("product").text, i.find("quantity").text) for i in items] == [("khandvi", "1"), ("masala chai", "1")]
assert len(text) == 190
as_json = json.dumps({"order_id": 103, "customer": "Asha", "items": [{"product": "khandvi", "quantity": 1}, {"product": "masala chai", "quantity": 1}]})
assert len(as_json) == 130
# JSON writes each name once, XML writes each twice (opening and closing tag)
assert as_json.count('"customer"') == 1 and text.count("customer") == 2
# source: https://www.sitemaps.org/protocol.html
#   confirmed: "The Sitemap protocol format consists of XML tags"
# source: https://docs.python.org/3/library/xml.etree.elementtree.html
#   confirmed: ElementTree has fromstring, which parses XML from a string
# source: https://www.sitemaps.org/protocol.html
#   confirmed: "in addition to the XML protocol, we support RSS feeds and text files"
# source: https://www.w3.org/TR/xmlschema11-2/
#   confirmed: XML Schema datatypes include decimal, float, integer
print("072 ok")
