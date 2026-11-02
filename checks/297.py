# checks for notes/297-statistics-how-the-planner-guesses-row-counts.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
# run on a real Postgres 16.15 server: orders100k (order_id 101..100100, status cancelled when order_id % 1000 = 0 else delivered),
# index on status. ANALYZE then pg_stats: most_common_vals {delivered,cancelled}, most_common_freqs {0.9992333,0.00076666666}
# EXPLAIN of status = 'cancelled' after that ANALYZE showed rows=77. four more ANALYZE runs gave freqs 0.0010666667, 0.0007, 0.001, 0.0011
assert 100100 // 1000 - 100 // 1000 == 100
assert 23 / 30000 == 0.0007666666666666667 and round(23 / 30000, 8) == 0.00076667
assert round(23 / 30000 * 100000) == 77
assert [round(h / 30000 * 100000) for h in [23, 32, 21, 30, 33]] == [77, 107, 70, 100, 110]
assert round(0.0010666667 * 30000) == 32 and round(0.0007 * 30000) == 21 and round(0.001 * 30000) == 30 and round(0.0011 * 30000) == 33
assert round(1 - 23 / 30000, 7) == 0.9992333
# source: https://www.postgresql.org/docs/16/sql-analyze.html
#   confirmed: ANALYZE takes a random sample of a large table, statistics include most common values, and are approximate and change slightly each run (opened this run)
# source: https://www.postgresql.org/docs/16/routine-vacuuming.html
#   confirmed: the autovacuum daemon automatically issues ANALYZE whenever a table has changed sufficiently (opened this run)
# audit: the note said ANALYZE reads a random sample of rows, not every row, and that the guess is share times table size, both read as always true. the docs say "For large tables, ANALYZE takes a random sample of the table contents, rather than examining every row" (https://www.postgresql.org/docs/16/sql-analyze.html, opened this run), and for a value that is not in the most common list the estimate is made another way (https://www.postgresql.org/docs/16/row-estimation-examples.html, opened this run). the note now says on a big table and for a saved value
# Postgres 16.15 run this audit: six ANALYZE runs on orders100k gave cancelled freq * 30000 = 23, 38, 34, 31, 22, 23 (all whole numbers), so the 30000 row sample is right
assert [round(x) for x in [0.00076666666 * 30000, 0.0012666667 * 30000, 0.0011333333 * 30000]] == [23, 38, 34]
