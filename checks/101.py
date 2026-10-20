# checks for notes/101-sql-you-describe-the-result.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
# the query and the python loop give the same answer
sql = [r[0] for r in con.execute("SELECT name FROM customers WHERE city = 'Jersey City'").fetchall()]
customers = [("Asha", "Jersey City"), ("Bhavin", "Edison"), ("Chirag", "Jersey City"), ("Disha", "Hoboken"), ("Esha", None)]
found = [n for n, c in customers if c == "Jersey City"]
assert sql == found == ["Asha", "Chirag"]
# the python list mirrors the real customers table
assert [tuple(r) for r in con.execute("SELECT name, city FROM customers ORDER BY customer_id").fetchall()] == customers
# Esha: one row, city NULL
assert con.execute("SELECT city FROM customers WHERE name = 'Esha'").fetchall() == [(None,)]
# five customers
assert con.execute("SELECT count(*) FROM customers").fetchone()[0] == 5
# source: https://en.wikipedia.org/wiki/SQL
# confirmed: SQL is a set-based, declarative language; implementations are incompatible between vendors in places
# (dialects), and it has an ISO standard
# source: https://www.sqlite.org/lang.html
# confirmed: "SQLite understands most of the standard SQL language."
# source: https://www.postgresql.org/about/
# confirmed: PostgreSQL "uses and extends the SQL language"
# source: https://dev.mysql.com/doc/refman/8.4/en/introduction.html
# confirmed: "a very fast, multithreaded, multi-user, and robust SQL (Structured Query Language) database server"
# source: https://en.wikipedia.org/wiki/Database_index
# confirmed: an index is "a data structure that improves the speed of data retrieval operations on a database table"
# source: https://duckdb.org/why_duckdb
# confirmed: "DuckDB does not run as a separate process, but completely embedded within a host process."
# source: https://www.sqlite.org/lang_select.html
# confirmed: if a SELECT has no ORDER BY clause, "the order in which the rows are returned is undefined"
print("101 ok")
