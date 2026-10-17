# checks for notes/029-daylight-saving.md
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
con = shop()
ny = ZoneInfo("America/New_York")
rows = []
for h in [4, 5, 6, 7]:
    u = datetime(2026, 11, 1, h, 30, tzinfo=timezone.utc)
    l = u.astimezone(ny)
    rows.append((u.strftime("%H:%M"), l.strftime("%H:%M"), l.strftime("%z"), int(u.timestamp())))
assert rows == [("04:30", "00:30", "-0400", 1793507400), ("05:30", "01:30", "-0400", 1793511000),
                ("06:30", "01:30", "-0500", 1793514600), ("07:30", "02:30", "-0500", 1793518200)]
assert rows[2][3] - rows[1][3] == 3600
# spring: 02:30 on 8 March 2026 never appears, 01:30 is followed by 03:30
assert datetime(2026, 3, 8, 6, 30, tzinfo=timezone.utc).astimezone(ny).strftime("%H:%M") == "01:30"
assert datetime(2026, 3, 8, 7, 30, tzinfo=timezone.utc).astimezone(ny).strftime("%H:%M") == "03:30"
# quiz 1
t = lambda s: int(datetime.fromisoformat(s).timestamp())
assert t("2026-11-01T01:50:00-04:00") == t("2026-11-01T05:50:00Z")
assert t("2026-11-01T01:10:00-05:00") == t("2026-11-01T06:10:00Z")
assert t("2026-11-01T01:50:00-04:00") < t("2026-11-01T01:10:00-05:00")
# quiz 2
assert str(con.sql("SELECT ordered_at + INTERVAL '5 hours' FROM orders WHERE order_id = 106").fetchone()[0]) == "2026-04-08 15:00:00"
assert datetime(2026, 4, 8, 14, 0, tzinfo=timezone.utc).astimezone(ny).strftime("%H:%M %z") == "10:00 -0400"
# source: https://peps.python.org/pep-0495/
# confirmed: fold is 0 except for the second occurrence of an ambiguous time, where it is 1
# source: https://en.wikipedia.org/wiki/Daylight_saving_time
# confirmed: "A one-hour change is usual, but twenty-minute and two-hour changes have been used in the past. Notable exceptions today include Lord Howe Island with a thirty-minute change"
print("029 ok")
