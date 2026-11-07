# checks for notes/351-connection-pools-why-opening-a-connection-is-expensive.md
OPEN, QUERY = 150, 50
assert OPEN == 3 * 50 and QUERY == 50
assert 100 * (OPEN + QUERY) == 20000
assert OPEN + 100 * QUERY == 5150
assert 100 * OPEN == 15000 and 20000 - 5150 > 0
# source: https://www.postgresql.org/docs/current/runtime-config-connection.html
#   opened this run: max_connections default is typically 100 connections
# source: https://www.postgresql.org/docs/current/connect-estab.html
#   opened this run (51.2 How Connections Are Established): process per user, the postmaster spawns a new backend process for every connection request
