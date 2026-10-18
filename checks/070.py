# checks for notes/070-flattening-nested-objects-into-columns.md
import csv, io, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
rows = con.execute("SELECT customer_id, name, city FROM customers WHERE customer_id IN (1,4,5) ORDER BY 1").fetchall()
assert rows == [(1, "Asha", "Jersey City"), (4, "Disha", "Hoboken"), (5, "Esha", None)]
assert con.execute("SELECT name, city, joined_on::VARCHAR FROM customers WHERE customer_id = 2").fetchone() == ("Bhavin", "Edison", "2026-01-20")

def flatten(text):
    flat = {}
    for key, value in json.loads(text).items():
        if isinstance(value, dict):
            for inner, v in value.items():
                flat[key + "_" + inner] = v
        else:
            flat[key] = value
    return flat

records = [
    '{"customer_id": 5, "name": "Esha", "address": {}}',
    '{"customer_id": 1, "name": "Asha", "address": {"city": "Jersey City"}}',
    '{"customer_id": 4, "name": "Disha", "address": {"city": "Hoboken"}}',
]
flat_rows = [flatten(r) for r in records]
assert list(flat_rows[0]) == ["customer_id", "name"]
# a header taken from row 1 refuses row 2
buf = io.StringIO()
w = csv.DictWriter(buf, fieldnames=list(flat_rows[0]), lineterminator="\n")
try:
    w.writerow(flat_rows[1])
    raise SystemExit("should fail")
except ValueError:
    pass
header = []
for row in flat_rows:
    for name in row:
        if name not in header:
            header.append(name)
assert header == ["customer_id", "name", "address_city"]
buf = io.StringIO()
w = csv.DictWriter(buf, fieldnames=header, lineterminator="\n")
w.writeheader(); w.writerows(flat_rows)
assert buf.getvalue() == "customer_id,name,address_city\n5,Esha,\n1,Asha,Jersey City\n4,Disha,Hoboken\n"
# check yourself 1: Bhavin brings a new flat name the old header lacks
b = flatten('{"customer_id": 2, "name": "Bhavin", "address": {"city": "Edison"}, "account": {"joined_on": "2026-01-20"}}')
assert "account_joined_on" in b and "account_joined_on" not in header
try:
    csv.DictWriter(io.StringIO(), fieldnames=header).writerow(b)
    raise SystemExit("should fail")
except ValueError:
    pass
# check yourself 2: city and state make two inner names, csv cannot tell missing from empty text
assert len({"city": 1, "state": 2}) == 2
assert list(csv.reader(io.StringIO("5,Esha,\n")))[0][2] == ""
# source: https://pandas.pydata.org/docs/reference/api/pandas.json_normalize.html
#   confirmed: sep default '.', "Nested records will generate names separated by sep", {'foo': {'bar': 0}} -> foo.bar
print("070 ok")
