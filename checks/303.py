# checks for notes/303-the-buffer-pool-keeping-hot-pages-in-memory.md
# toy pool: 3 pages, least recently used dropped, requests 0 1 2 0 3 1
SIZE = 3
pool = []
hits = reads = 0
dropped = []
for page in [0, 1, 2, 0, 3, 1]:
    if page in pool:
        pool.remove(page); pool.append(page); hits += 1
    else:
        if len(pool) == SIZE:
            dropped.append(pool.pop(0))
        pool.append(page); reads += 1
assert (hits, reads) == (1, 5)
assert dropped == [1, 2]
assert pool == [0, 3, 1]
# 128MB default shared_buffers in 8192 byte pages
assert 128 * 1024 * 1024 // 8192 == 16384
# 037: SSD 150000 ns against memory 100 ns
assert 150_000 // 100 == 1500
# 8 pages of the 1000 order table (note 285) fit in the pool
assert 8 < 16384
# run on a real Postgres 16 server: orders1000 (1000 rows from generate_series 101..1100, 8 pages), server restarted,
# EXPLAIN (ANALYZE, BUFFERS, COSTS OFF, TIMING OFF, SUMMARY OFF) WHERE order_id = 106:
# run 1 Buffers: shared read=8 dirtied=7 (plus Planning buffers lines), run 2 Buffers: shared hit=8
# source: https://www.postgresql.org/docs/16/runtime-config-resource.html
#   confirmed: shared_buffers default is typically 128MB, unit without suffix is BLCKSZ blocks of typically 8kB, and Postgres also relies on the operating system cache
# source: https://www.postgresql.org/docs/16/sql-explain.html
#   confirmed: BUFFERS reports shared blocks hit and read; a hit means a read was avoided because the block was already in cache; shared blocks hold regular table and index data
# source: https://raw.githubusercontent.com/postgres/postgres/REL_16_STABLE/src/backend/storage/buffer/README
#   confirmed: the normal buffer replacement strategy is a clock sweep algorithm, not strict least recently used
