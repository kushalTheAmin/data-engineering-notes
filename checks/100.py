# checks for notes/100-capstone-the-whole-shop-as-four-connected-tables.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
# row counts behind the diagram
assert con.execute("SELECT count(*) FROM customers").fetchone()[0] == 5
assert con.execute("SELECT count(*) FROM orders").fetchone()[0] == 7
assert con.execute("SELECT count(*) FROM order_items").fetchone()[0] == 13
assert con.execute("SELECT count(*) FROM products").fetchone()[0] == 6
# column lists in the diagram
def cols(t):
    return [r[0] for r in con.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name='{t}' ORDER BY ordinal_position").fetchall()]
assert cols("customers") == ["customer_id", "name", "city", "joined_on"]
assert cols("orders") == ["order_id", "customer_id", "ordered_at", "status"]
assert cols("order_items") == ["order_id", "product_id", "quantity"]
assert cols("products") == ["product_id", "name", "category", "price"]
# the shop holds 7 tables: these 4 core ones plus 3 side tables that each point at orders
assert [r[0] for r in con.execute("SELECT table_name FROM information_schema.tables ORDER BY 1").fetchall()] == ["app_events", "city_feed", "clicks", "customer_contacts", "customers", "daily_orders", "delivery_zones", "logins", "order_fees", "order_items", "order_messages", "order_notes", "order_ratings", "order_tracking", "orders", "price_export", "product_tags", "products", "promo_periods", "referrals", "signups"]
for t in ("order_ratings", "order_notes", "order_messages"):
    assert con.execute(f"SELECT referenced_table FROM duckdb_constraints() WHERE table_name = '{t}' AND constraint_type = 'FOREIGN KEY'").fetchall() == [("orders",)]
# Esha has no orders, fafda sits on no item
assert con.execute("SELECT count(*) FROM orders WHERE customer_id = 5").fetchone()[0] == 0
assert con.execute("SELECT count(*) FROM order_items WHERE product_id = 6").fetchone()[0] == 0
# nothing forces an order to have items: a bare order row is accepted
con.execute("INSERT INTO orders VALUES (999, 1, TIMESTAMP '2026-05-01 10:00:00', 'pending')")
assert con.execute("SELECT count(*) FROM order_items WHERE order_id = 999").fetchone()[0] == 0
# cancelled order 104 keeps its item row
assert con.execute("SELECT status FROM orders WHERE order_id = 104").fetchone()[0] == "cancelled"
assert con.execute("SELECT count(*) FROM order_items WHERE order_id = 104").fetchone()[0] == 1
print("100 ok")
