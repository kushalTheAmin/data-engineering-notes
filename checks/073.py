# checks for notes/073-yaml.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
assert con.execute("SELECT c.name FROM orders o JOIN customers c USING (customer_id) WHERE order_id = 103").fetchone() == ("Asha",)
assert con.execute("""SELECT p.name, i.quantity FROM order_items i JOIN products p USING (product_id)
  WHERE order_id = 103 ORDER BY p.name""").fetchall() == [("khandvi", 1), ("masala chai", 1)]
lines = ["order_id: 103", "customer: Asha", "items:", "  - product: khandvi", "    quantity: 1", "  - product: masala chai", "    quantity: 1"]
assert [len(l) - len(l.lstrip(" ")) for l in lines] == [0, 0, 0, 2, 4, 2, 4]
assert len("\n".join(lines)) == 113
# 130 is the json length from note 072's check, 190 the xml length
import json
assert len(json.dumps({"order_id": 103, "customer": "Asha", "items": [{"product": "khandvi", "quantity": 1}, {"product": "masala chai", "quantity": 1}]})) == 130
assert 113 < 130 < 190
# "- " is 2 characters, so product (after the dash) starts at 2 + 2 = 4, the same column as quantity
assert lines[3].index("product") == 4 == lines[4].index("quantity")
# source: https://yaml.org/spec/1.2.2/
#   confirmed: "To maintain portability, tab characters must not be used in indentation"
# source: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
#   confirmed: "Workflow files use YAML syntax"
print("073 ok")
