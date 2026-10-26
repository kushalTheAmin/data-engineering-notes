# checks for notes/216-unique-no-two-rows-may-share-a-value.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
con.execute("CREATE TABLE login (customer_id INTEGER NOT NULL, email VARCHAR UNIQUE)")
con.execute("INSERT INTO login VALUES (1, 'asha@example.com'), (2, 'bhavin@example.com')")
assert q("SELECT * FROM login ORDER BY customer_id") == [(1, "asha@example.com"), (2, "bhavin@example.com")]
try:
    con.execute("INSERT INTO login VALUES (3, 'asha@example.com')")
    assert False
except Exception as e:
    assert "unique" in str(e).lower()
assert q("SELECT count(*) FROM login") == [(2,)]
con.execute("INSERT INTO login VALUES (4, NULL), (5, NULL)")
assert q("SELECT count(*), count(email) FROM login") == [(4, 2)]
# check yourself 1
con.execute("CREATE TABLE coupon (code VARCHAR UNIQUE, customer_id INTEGER)")
con.execute("INSERT INTO coupon VALUES ('DIWALI', 1), ('diwali', 2)")
assert q("SELECT count(*) FROM coupon") == [(2,)]
# check yourself 2
con.execute("CREATE TABLE hub (city VARCHAR UNIQUE)")
con.execute("INSERT INTO hub VALUES ('Jersey City'), ('Edison'), ('Hoboken'), (NULL), (NULL)")
assert q("SELECT count(*), count(city) FROM hub") == [(5, 3)]
# the shop cities used in question 2 are real
assert sorted(r[0] for r in q("SELECT DISTINCT city FROM customers WHERE city IS NOT NULL")) == ["Edison", "Hoboken", "Jersey City"]
# source: https://www.postgresql.org/docs/current/ddl-constraints.html
#   confirmed (opened this run): null values are never considered equal in the unique comparison, so duplicate rows with a null are storable; NULLS NOT DISTINCT changes this.
# source: https://learn.microsoft.com/en-us/sql/relational-databases/tables/unique-constraints-and-check-constraints
#   confirmed (opened this run): SQL Server UNIQUE "allow for the value NULL. However, as with any value participating in a UNIQUE constraint, only one null value is allowed per column", so two NULLs both getting in is DuckDB and Postgres behavior, not every database
# source: https://duckdb.org/docs/2.0/sql/expressions/collations.html
#   confirmed (opened this run): "By default, the BINARY collation is used", so 'hello' = 'hElLO' is false and DIWALI, diwali are different values in DuckDB
# source: https://dev.mysql.com/doc/refman/8.4/en/case-sensitivity.html
#   confirmed (opened this run): "The default character set and collation are utf8mb4 and utf8mb4_0900_ai_ci, so nonbinary string comparisons are case-insensitive by default."
# source: https://www.postgresql.org/docs/current/ddl-constraints.html
#   confirmed (opened this run): "A table can have at most one primary key"
assert q("SELECT 'DIWALI' = 'diwali'") == [(False,)]
# source: https://www.postgresql.org/docs/15/release-15.html
#   confirmed (opened this run): "this can now be changed by creating constraints and indexes using UNIQUE NULLS NOT DISTINCT", and the postgres 14 constraints page has no NULLS NOT DISTINCT, so the option starts at Postgres 15
# the five rows in question 2 hold only 3 different cities plus 2 NULLs
assert q("SELECT count(*), count(DISTINCT city), count(*) - count(city) FROM hub") == [(5, 3, 2)]
