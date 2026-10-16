# checks for notes/026-seconds-milliseconds-microseconds.md
from datetime import datetime, timezone
import duckdb
s = 1775049300
m = datetime(2026, 4, 1, 13, 15, tzinfo=timezone.utc)
assert int(m.timestamp()) == s
assert s * 1000 == 1775049300000
assert s * 1000 * 1000 == 1775049300000000
assert [len(str(x)) for x in (s, s * 1000, s * 10 ** 6)] == [10, 13, 16]
assert str(datetime.fromtimestamp(s / 1000, timezone.utc)) == "1970-01-21 13:04:09.300000+00:00"
assert (datetime.fromtimestamp(s / 1000, timezone.utc) - datetime(1970, 1, 1, tzinfo=timezone.utc)).days == 20
try:
    datetime.fromtimestamp(s * 1000, timezone.utc)
    raise SystemExit("expected failure")
except ValueError as e:
    assert str(e) == "year 58219 is out of range"
assert round(s * 1000 / 31556952 + 1970) == 58219
assert (datetime(2026, 4, 1, 18, 40) - datetime(2026, 4, 1, 9, 15)).total_seconds() == 33900 == 9 * 3600 + 25 * 60
assert 33900 * 1000 == 33900000
assert duckdb.sql("SELECT epoch_ms(TIMESTAMP '2026-04-01 18:40:00') - epoch_ms(TIMESTAMP '2026-04-01 09:15:00')").fetchone()[0] == 33900000
# a 10 digit seconds count read as milliseconds is about 1.8 billion ms, about 20 days
assert 1.8e9 / 1000 / 86400 < 21
# source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/now
#   confirmed: Date.now() returns milliseconds elapsed since the epoch, midnight 1 January 1970 UTC
# source: https://www.postgresql.org/docs/current/datatype-datetime.html
#   confirmed: timestamp resolution is 1 microsecond
print("026 ok")
assert datetime.fromtimestamp(10 ** 9, timezone.utc).year == 2001 and datetime.fromtimestamp(10 ** 10 - 1, timezone.utc).year == 2286
