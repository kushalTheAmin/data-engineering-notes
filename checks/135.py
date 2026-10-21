# checks for notes/135-one-language-many-dialects.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
from decimal import Decimal
con = shop()
a = con.execute("SELECT name, price FROM products ORDER BY price DESC FETCH FIRST 2 ROWS ONLY").fetchall()
b = con.execute("SELECT name, price FROM products ORDER BY price DESC LIMIT 2").fetchall()
assert a == b == [("kaju katli", Decimal("12.00")), ("khandvi", Decimal("7.50"))]
# DuckDB has no TOP n syntax
try:
    con.execute("SELECT TOP 2 name, price FROM products ORDER BY price DESC")
    raise SystemExit("TOP should fail in DuckDB")
except Exception as e:
    assert "Parser Error" in str(e)
# source: https://www.postgresql.org/docs/current/sql-select.html
# confirmed: "The clauses LIMIT and OFFSET are PostgreSQL-specific syntax, also used by MySQL. The SQL:2008 standard has introduced the clauses OFFSET ... FETCH {FIRST|NEXT} ..."; PostgreSQL supports both
# source: https://learn.microsoft.com/en-us/sql/t-sql/queries/top-transact-sql
# confirmed: SQL Server limits rows with TOP (expression); applies to SQL Server and Azure SQL
print("135 ok")
