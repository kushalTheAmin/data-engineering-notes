# checks for notes/208-containers-a-program-packed-with-everything-it-needs.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the shop has 7 orders
assert q("SELECT count(*) FROM orders") == [(7,)]
# a missing library fails with ModuleNotFoundError
try:
    import a_library_the_server_lacks
except ModuleNotFoundError:
    pass
else:
    raise AssertionError
# the two laptop/server tables are invented example versions: 3.12, 3.8, 3.13 are all real python versions
# source: https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/
#   confirmed: "containers are isolated processes for each of your app's components"; "Each container has everything it needs to function with no reliance on any pre-installed dependencies"; "A container is simply an isolated process with all of the files it needs to run"; containers "all share the same kernel", unlike a VM which has its own kernel
# source: https://hub.docker.com/_/postgres
#   confirmed: Docker Official Image page for postgres, shows `docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres` as one command
# source: https://docs.docker.com/desktop/features/vmm/
#   confirmed: "Docker Desktop supports multiple Virtual Machine Managers (VMMs) to power the Linux VM that runs containers."
