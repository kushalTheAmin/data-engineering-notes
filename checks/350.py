# checks for notes/350-connecting-python-to-a-database-a-result-you-read-once.md
import os, sys, sqlite3
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
import duckdb
con0 = shop()
rows = con0.execute("SELECT name, city FROM customers WHERE name IN ('Asha','Bhavin','Esha') ORDER BY name").fetchall()
assert rows == [('Asha', 'Jersey City'), ('Bhavin', 'Edison'), ('Esha', None)]
con = duckdb.connect()
con.execute("CREATE TABLE customers (name VARCHAR, city VARCHAR)")
con.execute("INSERT INTO customers VALUES ('Asha', 'Jersey City'), ('Bhavin', 'Edison'), ('Esha', NULL)")
res = con.execute("SELECT name, city FROM customers ORDER BY name")
assert res.fetchone() == ('Asha', 'Jersey City')
assert res.fetchall() == [('Bhavin', 'Edison'), ('Esha', None)]
assert res.fetchall() == []
df = con.execute("SELECT name, city FROM customers ORDER BY name").df()
assert df["city"].isna().tolist() == [False, False, True]
# sqlite3 behaves the same
s = sqlite3.connect(":memory:")
s.execute("create table t(a)"); s.execute("insert into t values (1),(2),(3)")
cur = s.execute("select a from t")
assert cur.fetchone() == (1,) and cur.fetchall() == [(2,), (3,)] and cur.fetchall() == []
# 3 customers in the slice, 227 words of prose is within budget
# source: https://peps.python.org/pep-0249/
# confirmed: fetchall fetches all (remaining) rows, fetch calls continue where the last stopped
