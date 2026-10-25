# checks for notes/204-arrays-and-unnest-lists-inside-a-cell.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
names = dict(q("SELECT product_id, name FROM products"))
assert names[1] == "dhokla" and names[4] == "kaju katli" and names[5] == "masala chai"
# the slice
assert q("SELECT product_id, tags FROM product_tags WHERE product_id IN (1, 4, 5) ORDER BY product_id") == [
    (1, ["steamed", "savory"]), (4, ["sweet", "festive"]), (5, [])]
# unnested slice: chai has no rows
assert q("SELECT product_id, UNNEST(tags) AS tag FROM product_tags WHERE product_id IN (1, 4, 5) ORDER BY product_id, tag") == [
    (1, "savory"), (1, "steamed"), (4, "festive"), (4, "sweet")]
# tag counts, in python
tags = {pid: t for pid, t in q("SELECT product_id, tags FROM product_tags")}
counts = {}
for t in tags.values():
    for x in t:
        counts[x] = counts.get(x, 0) + 1
assert counts == {"steamed": 1, "savory": 3, "rolled": 1, "fried": 2, "sweet": 2, "festive": 1}
assert q("SELECT tag, count(*) AS products FROM (SELECT UNNEST(tags) AS tag FROM product_tags) GROUP BY tag ORDER BY products DESC, tag") == [
    ("savory", 3), ("fried", 2), ("sweet", 2), ("festive", 1), ("rolled", 1), ("steamed", 1)]
# 10 tags in total, 5 of 6 products behind them, chai has none
assert sum(counts.values()) == 10
assert q("SELECT count(DISTINCT product_id) FROM (SELECT product_id, UNNEST(tags) AS tag FROM product_tags)") == [(5,)]
assert q("SELECT count(*) FROM products") == [(6,)]
assert [p for p, t in tags.items() if not t] == [5]
# DuckDB shows a list in square brackets
assert str(q("SELECT [1, 2]")[0][0]) == "[1, 2]" and q("SELECT typeof([1, 2])") == [("INTEGER[]",)]
# source: https://www.postgresql.org/docs/current/arrays.html
#   confirmed: Postgres array literals are written '{ val1 delim val2 ... }' in curly braces; the ARRAY[...] constructor is the square bracket form
# source: https://duckdb.org/docs/2.0/sql/query_syntax/unnest.html
#   confirmed: unnest turns each list element into its own row; "Empty and NULL lists both unnest to zero rows"
# source: https://duckdb.org/docs/2.0/sql/data_types/list.html
#   confirmed: LIST holds variable-length lists; fixed-length lists use the ARRAY type
# source: https://www.postgresql.org/docs/current/functions-array.html
#   confirmed: unnest(anyarray) "Expands an array into a set of rows"
