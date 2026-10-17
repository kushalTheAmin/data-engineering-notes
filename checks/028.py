# checks for notes/028-time-zone-offsets.md
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop
from datetime import datetime
con = shop()
t = lambda s: int(datetime.fromisoformat(s).timestamp())
assert t("2026-04-01T09:15:00-04:00") == t("2026-04-01T18:45:00+05:30") == t("2026-04-01T13:15:00Z") == 1775049300
assert str(con.sql("SELECT ordered_at - INTERVAL '5 hours 30 minutes' FROM orders WHERE order_id = 102").fetchone()[0]) == "2026-04-01 13:10:00"
# 18:40 + 5:30 would be 00:10 next day
assert str(con.sql("SELECT ordered_at + INTERVAL '5 hours 30 minutes' FROM orders WHERE order_id = 102").fetchone()[0]) == "2026-04-02 00:10:00"
assert t("2026-04-01T10:00:00+02:00") < t("2026-04-01T07:30:00-01:00")
assert t("2026-04-01T10:00:00+02:00") == t("2026-04-01T08:00:00Z") and t("2026-04-01T07:30:00-01:00") == t("2026-04-01T08:30:00Z")
# source: https://www.rfc-editor.org/rfc/rfc3339
# confirmed: time-numoffset is + or - then hh:mm, time-offset is Z or that
# india is 5 hours 30 minutes ahead of UTC, new york is -04:00 in april and -05:00 in january
from zoneinfo import ZoneInfo
from datetime import timedelta
assert datetime(2026, 4, 1, tzinfo=ZoneInfo("Asia/Kolkata")).utcoffset() == timedelta(hours=5, minutes=30)
assert datetime(2026, 4, 1, tzinfo=ZoneInfo("America/New_York")).utcoffset() == timedelta(hours=-4)
assert datetime(2026, 1, 15, tzinfo=ZoneInfo("America/New_York")).utcoffset() == timedelta(hours=-5)
# source: https://www.rfc-editor.org/rfc/rfc3339
# confirmed: Z is a suffix that denotes a UTC offset of 00:00
print("028 ok")
