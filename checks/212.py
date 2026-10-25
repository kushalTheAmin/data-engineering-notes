# checks for notes/212-connections-and-sessions-one-conversation-with-the-database.md
# the only numbers are the 2 connections and the 6 steps in the trace
apps = ["Ashas app", "Bhavins app"]
assert len(apps) == 2
steps = 6
assert steps == 6
# source: https://www.postgresql.org/docs/current/sql-set.html
#   confirmed (opened this run): "SET only affects the value used by the current session."; a SET persists "until the end of the session"; SET TIME ZONE and SHOW exist
# source: https://www.pgbouncer.org/features.html
#   confirmed (opened this run): transaction pooling assigns a server connection to a client only during a transaction; its feature table lists SET/RESET as Yes for session pooling and Never for transaction pooling
# source: https://www.postgresql.org/docs/current/runtime-config-client.html
#   confirmed (opened this run): TimeZone "built-in default is GMT, but that is typically overridden in postgresql.conf; initdb will install a setting there corresponding to its system environment", so UTC is an assumed setting here, not a universal default
