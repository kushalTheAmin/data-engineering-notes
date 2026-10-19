# checks for notes/081-why-a-shared-spreadsheet-breaks.md
import os, tempfile

path = os.path.join(tempfile.mkdtemp(), "orders.csv")
with open(path, "w") as f:
    f.write("106,pending\n107,delivered\n")

def load():
    return [line.split(",") for line in open(path).read().split("\n") if line]

def save(rows):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write("".join(",".join(r) + "\n" for r in rows))
    os.replace(tmp, path)

asha, bhavin = load(), load()
asha[0][1] = "delivered"
bhavin[1][1] = "returned"
save(asha)
assert open(path).read() == "106,delivered\n107,delivered\n"
save(bhavin)
assert open(path).read().strip() == "106,pending\n107,returned"
print("081 ok")
