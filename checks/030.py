# checks for notes/030-store-utc-show-local.md
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop
from datetime import datetime, timezone
from datetime import timedelta
from zoneinfo import ZoneInfo
con = shop()
ny, mu = ZoneInfo("America/New_York"), ZoneInfo("Asia/Kolkata")
f = lambda d: d.strftime("%Y-%m-%d %H:%M")
want = {101: ("2026-04-01 13:15", "2026-04-01 09:15", "2026-04-01 18:45"),
        102: ("2026-04-01 22:40", "2026-04-01 18:40", "2026-04-02 04:10"),
        106: ("2026-04-08 14:00", "2026-04-08 10:00", "2026-04-08 19:30")}
for oid, (u, n, m) in want.items():
    t = con.sql(f"SELECT ordered_at FROM orders WHERE order_id = {oid}").fetchone()[0]
    assert f(t) == n
    utc = t.replace(tzinfo=ny).astimezone(timezone.utc)
    assert f(utc) == u and f(utc.astimezone(mu)) == m
assert datetime(2026, 4, 1, 13, 15, tzinfo=timezone.utc).astimezone(ny).strftime("%z") == "-0400"
assert datetime(2026, 4, 1, 13, 15, tzinfo=timezone.utc).astimezone(mu).strftime("%z") == "+0530"
# 09:15 minus -4 hours is 13:15: undoing the offset means subtracting it
assert (datetime(2026, 4, 1, 9, 15) - timedelta(hours=-4)).strftime("%H:%M") == "13:15"
# python block
out = [(u := datetime(2026, 11, 1, h, 30, tzinfo=timezone.utc)).isoformat() + " -> " + u.astimezone(ny).isoformat() for h in [5, 6]]
assert out == ["2026-11-01T05:30:00+00:00 -> 2026-11-01T01:30:00-04:00", "2026-11-01T06:30:00+00:00 -> 2026-11-01T01:30:00-05:00"]
# quiz 1
rows = con.sql("SELECT order_id, (ordered_at + INTERVAL '9 hours 30 minutes')::DATE FROM orders WHERE order_id IN (101, 102) ORDER BY 1").fetchall()
assert [str(r[1]) for r in rows] == ["2026-04-01", "2026-04-02"]
assert (mu.utcoffset(None) if False else datetime(2026, 4, 1, tzinfo=mu).utcoffset() - datetime(2026, 4, 1, tzinfo=ny).utcoffset()).total_seconds() == 9.5 * 3600
# quiz 2
a = datetime(2026, 11, 1, 0, 30, tzinfo=ny).astimezone(timezone.utc)
b = datetime(2026, 11, 1, 2, 30, tzinfo=ny).astimezone(timezone.utc)
assert (a.strftime("%H:%M"), b.strftime("%H:%M")) == ("04:30", "07:30")
assert (b - a).total_seconds() == 3 * 3600
# source: https://www.postgresql.org/docs/current/datatype-datetime.html
# confirmed: timestamptz is stored internally as UTC, shown in the session time zone, and the original zone is not retained
print("030 ok")
# source: https://www.postgresql.org/docs/current/tutorial-arch.html
# confirmed: "PostgreSQL uses a client/server model", so Postgres is a server database; the note no longer calls it popular, which no page here supports
