# checks for notes/205-querying-json-inside-a-column.md
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT count(*) FROM app_events") == [(4,)]
assert q("SELECT event_id, payload ->> '$.customer' AS customer, payload ->> '$.quantity' AS quantity FROM app_events ORDER BY event_id") == [
    (1, "Asha", None), (2, "Asha", "2"), (3, "Disha", None), (4, "Bhavin", "1")]
# the extracted value is text
assert q("SELECT typeof(payload ->> '$.quantity') FROM app_events WHERE event_id = 2") == [("VARCHAR",)]
# a typo in the path gives NULL on all 4 rows, no error
assert q("SELECT count(*) FROM app_events WHERE payload ->> '$.custmer' IS NULL") == [(4,)]
# python agrees on the data: view events have no quantity key
rows = [json.loads(p) for (p,) in q("SELECT payload FROM app_events ORDER BY event_id")]
assert ["quantity" in r for r in rows] == [False, True, False, True]
assert q("SELECT payload ->> '$.customer' AS customer, sum(CAST(payload ->> '$.quantity' AS INTEGER)) AS added FROM app_events WHERE payload ->> '$.type' = 'add_to_cart' GROUP BY customer ORDER BY customer") == [
    ("Asha", 2), ("Bhavin", 1)]
# source: https://duckdb.org/docs/2.0/data/json/json_functions.html
#   confirmed: ->> is the operator for json_extract_string, returns VARCHAR; paths start with $ and separate fields with a dot (the docs do not say what a missing path returns, the asserts above ran it: NULL)
assert q("SELECT payload ->> 'customer' FROM app_events WHERE event_id = 1") == [('Asha',)]  # DuckDB also takes a bare key
# source: https://www.postgresql.org/docs/current/functions-json.html
#   confirmed: json ->> text extracts the object field with the given key as text; no such key returns NULL instead of failing
