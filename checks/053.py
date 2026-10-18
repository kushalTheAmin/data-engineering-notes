# checks for notes/053-absolute-vs-relative-paths.md
import os.path

def land(stand, path):
    return os.path.normpath(os.path.join(stand, path))

assert land("/shop/exports", "orders.csv") == "/shop/exports/orders.csv"
assert land("/shop/backup", "orders.csv") == "/shop/backup/orders.csv"
assert land("/shop/exports", "/shop/backup/orders.csv") == "/shop/backup/orders.csv"
assert land("/shop/exports", "../backup/orders.csv") == "/shop/backup/orders.csv"
assert land("/shop", "../backup/orders.csv") == "/backup/orders.csv"
assert land("/shop/backup", "../exports/orders.csv") == "/shop/exports/orders.csv"
assert land("/shop/backup", "../exports/orders.csv") != "/shop/backup/exports/orders.csv"
# source: https://man7.org/linux/man-pages/man7/path_resolution.7.html
#   confirmed: a leading slash starts at the root, otherwise at the process working directory, and ".." is the parent directory
print("053 ok")
