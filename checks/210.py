# checks for notes/210-running-postgres-in-a-container-on-your-laptop.md
# the note has no computed numbers beyond the port pairs in the command and table
cmd = "docker run --name shop-db -e POSTGRES_PASSWORD=snacks -p 5432:5432 -d postgres".split()
assert cmd[cmd.index("-p") + 1].split(":") == ["5432", "5432"]
host, box = "5433:5432".split(":")
assert (host, box) == ("5433", "5432")  # left number is the laptop side
# source: https://hub.docker.com/_/postgres
#   confirmed: example "docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres"; POSTGRES_PASSWORD "is required for you to use the PostgreSQL image. It must not be empty or undefined."
# source: https://docs.docker.com/reference/cli/docker/container/run/
#   confirmed: -p binds a container port to a host port (host side first); --detach starts a container as a background process that doesn't occupy your terminal; --name sets a custom identifier; --env sets a variable inside the container
# source: https://www.postgresql.org/docs/current/runtime-config-connection.html
#   confirmed: port is "The TCP port the server listens on; 5432 by default."
# source: https://docs.docker.com/engine/storage/
#   confirmed: "Data written to the container layer doesn't persist when the container is destroyed."
# source: https://docs.docker.com/reference/cli/docker/container/rm/
#   confirmed (opened this run): rm -v "Remove anonymous volumes associated with the container", so the unnamed volume is not simply the container's own layer
# source: https://hub.docker.com/_/postgres
#   confirmed (opened this run): the postgres image uses an anonymous volume "not reused across container re-creations"
