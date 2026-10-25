# checks for notes/209-images-and-containers-the-packed-box-and-the-running-copy.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the shop has 7 orders
assert q("SELECT count(*) FROM orders") == [(7,)]
# trace table: replay the five steps with a model of one image and per-container scratch space
image = {"loader.py": "original"}
containers = {}
def run(name): containers[name] = {}
def edited(name): return "loader.py" in containers[name]
run("a"); run("b")
assert (len(image), len(containers)) == (1, 2)
containers["a"]["loader.py"] = "edited"
assert edited("a") and not edited("b") and image["loader.py"] == "original"
del containers["a"]
assert len(containers) == 1 and not edited("b")
run("c")
assert len(containers) == 2 and not edited("c")
# source: https://docs.docker.com/engine/storage/drivers/
#   confirmed: "multiple containers can share access to the same underlying image and yet have their own data state"; "The major difference between a container and an image is the top writable layer"; "When the container is deleted, the writable layer is also deleted. The underlying image remains unchanged."
# source: https://docs.docker.com/engine/storage/
#   confirmed: "Data written to the container layer doesn't persist when the container is destroyed."
# source: https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/
#   confirmed: "Images are immutable. Once an image is created, it can't be modified."; an image is a package of "all of the files, binaries, libraries, and configurations"
# source: https://docs.docker.com/reference/cli/docker/container/run/
#   confirmed: docker run is described as "Create and run a new container from an image"
