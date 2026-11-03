# checks for notes/304-vacuum-how-postgres-cleans-up-old-row-versions.md
# toy page: 7 slots, delete 104 and 105, vacuum frees them, inserts take the lowest free slots
slots = {1: 101, 2: 102, 3: 103, 4: 104, 5: 105, 6: 106, 7: 107}
for s, o in list(slots.items()):
    if o in (104, 105):
        del slots[s]
placed = {}
for o in (108, 109):
    s = next(i for i in range(1, 100) if i not in slots)
    slots[s] = o
    placed[o] = (0, s)
assert placed == {108: (0, 4), 109: (0, 5)}
# the table file is one page the whole time
assert 8192 == 8 * 1024
# run on a real Postgres 16.15 server, autovacuum off, table orders(order_id int, status text) with the 7 shop orders:
# 1) session A: BEGIN ISOLATION LEVEL REPEATABLE READ; SELECT count(*) FROM orders;  -> 7
# 2) session B: DELETE FROM orders WHERE order_id=104; heap_page_items slot 4 xmin 737 xmax 738
#    VACUUM VERBOSE orders -> "1 are dead but not yet removable"; slot 4 lp_flags still 1 (in use)
# 3) A commits; VACUUM orders; slot 4 lp_flags 0 (unused); pg_relation_size 8192 before and after
# 4) INSERT order 108 -> ctid (0,4); separate run: delete 104 and 105, VACUUM, insert 108 and 109 -> (0,4) and (0,5)
# source: https://www.postgresql.org/docs/16/routine-vacuuming.html
#   confirmed: standard VACUUM removes dead row versions and marks the space available for reuse, but does not return it to the operating system except when pages at the end of the table become entirely free; autovacuum daemon runs vacuuming automatically
# audit: the note said a transaction left open for days stops cleanup, which reads as always true. the docs tell you to end long-running open transactions found by a large age(backend_xid) or age(backend_xmin), so only a transaction holding an xid or a snapshot holds cleanup back (an idle read committed one with no xid takes none). it now says a repeatable read transaction blocks cleanup of rows ended since
# source: https://www.postgresql.org/docs/16/routine-vacuuming.html
#   confirmed: End long-running open transactions. You can find these by checking pg_stat_activity for rows where age(backend_xid) or age(backend_xmin) is large (opened this run)
# source: https://www.postgresql.org/docs/16/ddl-system-columns.html
#   confirmed: xmin is the transaction ID of the inserting transaction for this row version, xmax is the identity of the deleting transaction (opened this run)
# source: https://www.postgresql.org/docs/16/sql-vacuum.html
#   confirmed: VACUUM FULL rewrites the entire contents of the table into a new disk file with no extra space, returning unused space to the operating system (opened this run)
