# checks for notes/035-the-processor.md
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shop import shop

con = shop()
# order 101 in whole cents: 2 dhokla at 600, 2 masala chai at 300
rows = con.execute(
    "SELECT p.name, (p.price * 100)::INTEGER, i.quantity FROM order_items i "
    "JOIN products p USING (product_id) WHERE i.order_id = 101 ORDER BY p.product_id").fetchall()
assert rows == [("dhokla", 600, 2), ("masala chai", 300, 2)]
# replay the 7 steps in the table
total = 0                      # 1
item = 600                     # 2
assert total == 0
item *= 2; assert item == 1200  # 3
total += item; assert total == 1200  # 4
item = 300                     # 5
item *= 2; assert item == 600   # 6
total += item; assert total == 1800  # 7
assert total / 100 == 18.00
assert total == sum(p * q for _, p, q in rows)
# source: https://en.wikipedia.org/wiki/Central_processing_unit
#   confirmed: a CPU is the primary processor; clock rates reach several gigahertz;
#   multi-core chips hold multiple CPUs called cores; registers supply operands and store results;
#   instructions are represented by a number or sequence of numbers
#   confirmed: "Several CPUs (denoted cores) can be combined in a single processing chip"; a CPU executes "arithmetic, logic, controlling, and input/output" operations, more than add, multiply and compare
# giga is a billion: see checks/033.py
assert 1000 ** 3 == 1_000_000_000
print("035 ok")
