# checks for notes/264-naming-conventions-names-people-can-guess.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the guessed join works because both tables name the key customer_id
assert q("SELECT c.name, k.phone FROM customers c JOIN customer_contacts k ON k.customer_id = c.customer_id ORDER BY c.customer_id") == [('Asha', '555-0101'), ('Bhavin', '555-0102'), ('Disha', '555-0104')]
assert [r[0] for r in q("DESCRIBE customer_contacts")][:1] == ['customer_id']
# customer_id is the key name in customers and orders too
assert 'customer_id' in [r[0] for r in q("SELECT column_name FROM information_schema.columns WHERE table_name = 'orders'")]
assert 'ordered_at' in [r[0] for r in q("SELECT column_name FROM information_schema.columns WHERE table_name = 'orders'")]
# source: https://www.postgresql.org/docs/current/sql-syntax-lexical.html
# confirmed: unquoted names are folded to lower case in PostgreSQL, quoting makes an identifier case-sensitive so "Foo" differs from foo
# source: https://survey.stackoverflow.co/2025/technology
# confirmed: PostgreSQL is the most used database among all survey respondents, 55.6 percent (chart data), so popular is supported and most app data is not
# customers holds customer_id as its primary key, only tables that point at customers hold it as a foreign key
assert q("SELECT constraint_column_names FROM duckdb_constraints() WHERE table_name = 'customers' AND constraint_type = 'PRIMARY KEY'") == [(['customer_id'],)]
fk = {r[0] for r in q("SELECT table_name FROM duckdb_constraints() WHERE constraint_type = 'FOREIGN KEY' AND constraint_column_names = ['customer_id']")}
assert {'customer_contacts', 'orders'} <= fk and 'customers' not in fk
