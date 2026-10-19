# checks for notes/082-a-database-guards-the-data.md
class Database:
    def __init__(self, rows):
        self.rows = rows

    def set_status(self, order_id, status):
        for r in self.rows:
            if r["order_id"] == order_id:
                r["status"] = status

db = Database([
    {"order_id": 106, "status": "pending"},
    {"order_id": 107, "status": "delivered"},
])
db.set_status(106, "delivered")
db.set_status(107, "returned")
assert db.rows == [{'order_id': 106, 'status': 'delivered'}, {'order_id': 107, 'status': 'returned'}]
# 081 slice: 106 pending, 107 delivered, matches the shop orders table at start of 081's example
# source: https://www.postgresql.org/docs/current/tutorial-arch.html
#   confirmed: clients connect to the server process, which manages the database files and does the work for them
# source: https://dev.mysql.com/doc/refman/8.4/en/mysqld.html
#   confirmed: mysqld is the MySQL server that manages access to the database
print("082 ok")
