# checks for notes/232-durability-surviving-a-crash.md
# the note has no shop rows and no computed numbers; the only number is "three times" below
# source: https://www.postgresql.org/docs/current/runtime-config-wal.html
#   confirmed (opened this run): synchronous_commit valid values "remote_apply, on (the default), remote_write, local, and off"; the local behavior of all non-off modes "is to wait for local flush of WAL to disk"; in off mode "there is no waiting" and the maximum delay before a commit is safe against a server crash is "three times wal_writer_delay"; off "does not create any risk of database inconsistency: ... some recent allegedly-committed transactions being lost, but the database state will be just the same as if those transactions had been aborted cleanly"
# source: https://www.postgresql.org/docs/current/wal-async-commit.html
#   confirmed (opened this run): synchronous commit "waits for the transaction's WAL records to be flushed to permanent storage before returning a success indication to the client"; WAL records, a short record of the change, are what get flushed; asynchronous commit risk "is of data loss, not data corruption"
assert 3 * 1 == 3
