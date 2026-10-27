# checks for notes/232-durability-surviving-a-crash.md
# the note has no shop rows and no computed numbers
# source: https://www.postgresql.org/docs/current/runtime-config-wal.html
#   confirmed (opened this run): synchronous_commit valid values "remote_apply, on (the default), remote_write, local, and off"; the local behavior of all non-off modes "is to wait for local flush of WAL to disk"; in off mode "there is no waiting" and the maximum delay before a commit is safe against a server crash is "three times wal_writer_delay"; off "does not create any risk of database inconsistency: ... some recent allegedly-committed transactions being lost, but the database state will be just the same as if those transactions had been aborted cleanly"
# source: https://www.postgresql.org/docs/current/wal-async-commit.html
#   confirmed (opened this run): synchronous commit "waits for the transaction's WAL records to be flushed to permanent storage before returning a success indication to the client"; "for short transactions this delay is a major component of the total transaction time"; asynchronous commit risk "is of data loss, not data corruption"; "the net effect is therefore loss of the last few transactions"
# source: https://www.postgresql.org/docs/current/wal-intro.html
#   confirmed (opened this run): "only the WAL file needs to be flushed to disk to guarantee that a transaction is committed, rather than every data file changed by the transaction"
assert 3 * 1 == 3
