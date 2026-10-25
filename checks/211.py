# checks for notes/211-a-database-server-postgres-where-most-app-data-lives.md
# the only numbers are the port 5432 and the 3 clients drawn in the diagram
clients = ["Ashas app", "Bhavins app", "report script"]
assert len(clients) == 3
port = 5432
assert port == 5432
# source: https://www.postgresql.org/docs/current/tutorial-arch.html
#   confirmed: a server process "manages the database files, accepts connections to the database from client applications, and performs database actions on behalf of the clients"; it handles multiple concurrent connections by starting ("forking") a new process for each connection, while the supervisor process keeps waiting for client connections
# source: https://www.postgresql.org/docs/current/runtime-config-connection.html
#   confirmed: port is "The TCP port the server listens on; 5432 by default."
# source: https://duckdb.org/docs/current/connect/concurrency.html
#   confirmed: "Read-write mode: one process can both read and write to the database."; writing from several processes goes through a separate server, not the file
