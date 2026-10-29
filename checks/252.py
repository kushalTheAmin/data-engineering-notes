# checks for notes/252-point-in-time-recovery-a-backup-plus-the-replayed-log.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the shop has 7 real orders and 106 is pending; 108 is imagined
assert q("SELECT count(*) FROM orders")[0][0] == 7
assert q("SELECT status FROM orders WHERE order_id = 106")[0][0] == 'pending'
assert q("SELECT count(*) FROM orders WHERE order_id = 108")[0][0] == 0

# replay the three records on the 02:00 copy, stopping after each
table = {r[0]: r[1] for r in q("SELECT order_id, status FROM orders")}
wal = [("09:30", "insert", 108, "pending"), ("10:15", "update", 106, "delivered"), ("11:00", "drop", None, None)]
def replay(stop):
    t = dict(table)
    for time, kind, oid, status in wal:
        if time > stop:
            break
        if kind == "drop":
            return None
        t[oid] = status
    return t
assert len(replay("02:00")) == 7 and replay("02:00")[106] == 'pending'
assert len(replay("09:30")) == 8 and replay("09:30")[106] == 'pending'
assert len(replay("10:59")) == 8 and replay("10:59")[106] == 'delivered'
assert replay("11:00") is None
# 02:00 to 11:00 is nine hours
assert (11 - 2) == 9
# source: https://www.postgresql.org/docs/current/continuous-archiving.html
# confirmed: PITR restores a file-system backup then replays archived WAL; recovery replays until it reaches the target or runs out of files; WAL segments are copied out by archive_command
# source: https://www.postgresql.org/docs/current/runtime-config-wal.html
# confirmed: recovery_target_time sets the time stamp up to which recovery proceeds; restore_command example is cp from an archive dir
# source: https://www.postgresql.org/docs/current/runtime-config-wal.html
# confirmed: if archive recovery ends before the target is reached, the server shuts down with a fatal error
# source: https://www.postgresql.org/docs/current/continuous-archiving.html
# confirmed: PITR needs a file-system-level backup plus archived WAL; WAL segments are copied out when completed
print("252 ok")
