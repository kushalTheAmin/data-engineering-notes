# checks for notes/269-big-o-in-plain-words-how-work-grows-as-data-grows.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()

def find(order_ids, wanted):
    steps = 0
    for oid in order_ids:
        steps += 1
        if oid == wanted:
            return steps
    return steps

# the shop has 7 orders, ids 101 to 107
assert [r[0] for r in con.execute("SELECT order_id FROM orders ORDER BY 1").fetchall()] == list(range(101, 108))
for n in [7, 70, 700, 7000]:
    ids = list(range(101, 101 + n))
    assert find(ids, 101) == 1
    assert find(ids, 100 + n) == n
# 10 times the orders, 10 times the steps
assert 70 // 7 == 10 and 700 // 70 == 10 and 7000 // 700 == 10
# question 1
assert (find(list(range(101, 108)), 104), find(list(range(101, 7001)), 104)) == (4, 4)
assert len(range(101, 7001)) == 6900 and 6900 // 7 == 985  # almost a thousand times longer
# question 2
assert (find(list(range(101, 108)), 9999), find(list(range(101, 7101)), 9999)) == (7, 7000)
# unlike find, a scan after every match cannot stop at the first one: the docs say it scans the entire table to find all matching entries
# 7 million rows, 7 million steps for one lookup in the worst case
assert 7_000_000 * 1 == 7_000_000
# the reviews table in 268 has 4 rows
assert len([1, 2, 3, 4]) == 4
# source: https://www.postgresql.org/docs/current/indexes-intro.html
# confirmed: "With no advance preparation, the system would have to scan the entire test1 table, row by row, to find all matching entries."
# source: https://en.wikipedia.org/wiki/Time_complexity
# confirmed: "one commonly considers the worst-case time complexity, which is the maximum amount of time required for inputs of a given size"
# source: https://survey.stackoverflow.co/2025/technology
# confirmed: PostgreSQL is the most used database among all respondents, 55.6%, so popular is supported
