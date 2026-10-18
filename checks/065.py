# checks for notes/065-the-header-row-naming-the-columns.md
import csv, io, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
orders = con.execute("SELECT order_id, customer_id, CAST(ordered_at AS VARCHAR), status FROM orders WHERE order_id IN (101,102,104) ORDER BY order_id").fetchall()
assert orders == [(101, 1, '2026-04-01 09:15:00', 'delivered'), (102, 2, '2026-04-01 18:40:00', 'delivered'), (104, 3, '2026-04-04 08:30:00', 'cancelled')]
a = "order_id,customer_id,ordered_at,status\n" + "".join(f"{o},{c},{t},{s}\n" for o, c, t, s in orders)
b = "status,order_id,customer_id,ordered_at\n" + "".join(f"{s},{o},{c},{t}\n" for o, c, t, s in orders)
assert a == "order_id,customer_id,ordered_at,status\n101,1,2026-04-01 09:15:00,delivered\n102,2,2026-04-01 18:40:00,delivered\n104,3,2026-04-04 08:30:00,cancelled\n"
assert b == "status,order_id,customer_id,ordered_at\ndelivered,101,1,2026-04-01 09:15:00\ndelivered,102,2,2026-04-01 18:40:00\ncancelled,104,3,2026-04-04 08:30:00\n"
ra = list(csv.reader(io.StringIO(a)))
rb = list(csv.reader(io.StringIO(b)))
assert ra[1][3] == "delivered" and rb[1][3] == "2026-04-01 09:15:00"
da = list(csv.DictReader(io.StringIO(a)))
db = list(csv.DictReader(io.StringIO(b)))
assert da[0]["status"] == "delivered" and db[0]["status"] == "delivered"
assert sum(1 for r in ra[1:] if r[3] == "delivered") == 2
assert sum(1 for r in rb[1:] if r[3] == "delivered") == 0
assert sum(1 for r in da if r["status"] == "delivered") == 2
assert sum(1 for r in db if r["status"] == "delivered") == 2
# a file with no header: DictReader turns the first order into the names
nh = csv.DictReader(io.StringIO("101,1,2026-04-01 09:15:00,delivered\n102,2,2026-04-01 18:40:00,delivered\n"))
assert nh.fieldnames == ["101", "1", "2026-04-01 09:15:00", "delivered"]
assert len(list(nh)) == 1
# source: https://docs.python.org/3/library/csv.html
#   confirmed: if fieldnames is omitted, the first row supplies the names and is omitted from the results
# source: https://www.rfc-editor.org/rfc/rfc4180
#   confirmed: the header line is optional in csv; "There maybe an optional header line appearing as the first line of the file"
print("065 ok")
