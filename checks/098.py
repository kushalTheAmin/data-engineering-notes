# checks for notes/098-entity-relationship-diagrams.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
# order_items has exactly two foreign keys, so two lines touch its box
fks = con.execute("SELECT constraint_column_names, referenced_table FROM duckdb_constraints() WHERE table_name = 'order_items' AND constraint_type = 'FOREIGN KEY' ORDER BY referenced_table").fetchall()
assert [(list(c), t) for c, t in fks] == [(["order_id"], "orders"), (["product_id"], "products")]
assert con.execute("SELECT count(*) FROM orders WHERE customer_id = 1").fetchone()[0] == 3
# orders.customer_id is the foreign key to customers
fk = con.execute("SELECT constraint_column_names, referenced_table FROM duckdb_constraints() WHERE table_name = 'orders' AND constraint_type = 'FOREIGN KEY'").fetchall()
assert [(list(c), t) for c, t in fk] == [(["customer_id"], "customers")]
# the diagram boxes show fewer columns than the real tables have
assert len(con.execute("DESCRIBE customers").fetchall()) == 4 and len(con.execute("DESCRIBE orders").fetchall()) == 4
# source: https://mermaid.js.org/syntax/entityRelationshipDiagram.html
# confirmed: mermaid erDiagram attribute keys can be PK, FK or UK (primary, foreign, unique key)
# source: https://www.pgadmin.org/docs/pgadmin4/latest/erd_tool.html
# confirmed: pgAdmin ERD tool can "Generate the database diagram for an existing database"
print("098 ok")
