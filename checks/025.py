# checks for notes/025-unix-time.md
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo as Z
m = datetime(2026, 4, 1, 13, 15, tzinfo=timezone.utc)
assert int(m.timestamp()) == 1775049300
assert int(m.astimezone(Z("America/New_York")).timestamp()) == 1775049300
assert int(m.astimezone(Z("Asia/Kolkata")).timestamp()) == 1775049300
assert int((m + timedelta(hours=1)).timestamp()) - int(m.timestamp()) == 3600
assert datetime.fromtimestamp(0, timezone.utc) == datetime(1970, 1, 1, tzinfo=timezone.utc)
assert datetime.fromtimestamp(-1, timezone.utc) == datetime(1969, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
assert 2 ** 31 - 1 == 2147483647
assert datetime.fromtimestamp(2 ** 31 - 1, timezone.utc) == datetime(2038, 1, 19, 3, 14, 7, tzinfo=timezone.utc)
assert 24 * 60 * 60 == 86400
# source: https://en.wikipedia.org/wiki/Unix_time
#   confirmed: epoch is 00:00:00 UTC 1 January 1970, leap seconds are not counted,
#   signed 32 bit overflows one second after 2038-01-19T03:14:07Z, earlier times are negative
assert datetime.fromtimestamp(-2 ** 31, timezone.utc) == datetime(1901, 12, 13, 20, 45, 52, tzinfo=timezone.utc)
assert 1775049300 - 1775034900 == 14400 == 4 * 3600
print("025 ok")
