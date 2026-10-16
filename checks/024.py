# checks for notes/024-utc.md
from datetime import datetime
from zoneinfo import ZoneInfo as Z
u = datetime(2026, 4, 1, 13, 15, tzinfo=Z("UTC"))
ny = u.astimezone(Z("America/New_York"))
mu = u.astimezone(Z("Asia/Kolkata"))
assert ny.strftime("%Y-%m-%d %H:%M") == "2026-04-01 09:15" and ny.utcoffset().total_seconds() == -4 * 3600
assert mu.strftime("%Y-%m-%d %H:%M") == "2026-04-01 18:45" and mu.utcoffset().total_seconds() == 5.5 * 3600
# New York is 5 behind in winter
w = datetime(2026, 1, 15, 12, 0, tzinfo=Z("UTC")).astimezone(Z("America/New_York"))
assert w.utcoffset().total_seconds() == -5 * 3600
# quiz 1
assert datetime(2026, 4, 1, 9, 15, tzinfo=Z("America/New_York")).astimezone(Z("UTC")).strftime("%H:%M") == "13:15"
assert (9 - 4, 15) == (5, 15)
# quiz 2
a = datetime(2026, 4, 1, 22, 30, tzinfo=Z("Asia/Kolkata")).astimezone(Z("UTC"))
b = datetime(2026, 4, 1, 20, 0, tzinfo=Z("America/New_York")).astimezone(Z("UTC"))
assert a.strftime("%Y-%m-%d %H:%M") == "2026-04-01 17:00" and b.strftime("%Y-%m-%d %H:%M") == "2026-04-02 00:00"
assert a < b and "20:00" < "22:30"
# source: https://www.rfc-editor.org/rfc/rfc3339
#   confirmed: Z denotes a UTC offset of 00:00
# source: https://en.wikipedia.org/wiki/Coordinated_Universal_Time
#   confirmed: UTC is not adjusted for daylight saving time
print("024 ok")
