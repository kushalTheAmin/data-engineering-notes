# checks for notes/282-the-trade-off-faster-reads-usually-mean-slower-writes.md
def run(ids, want):
    loose, tidy = [], []
    w_loose = w_tidy = 0
    for v in ids:
        loose.append(v)
        w_loose += 1
        pos = 0
        while pos < len(tidy) and tidy[pos] < v:
            pos += 1
        w_tidy += 1 + (len(tidy) - pos)
        tidy.insert(pos, v)
    r_loose = loose.index(want) + 1
    lo, hi, r_tidy = 0, len(tidy) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        r_tidy += 1
        if tidy[mid] == want:
            break
        if tidy[mid] < want:
            lo = mid + 1
        else:
            hi = mid - 1
    return w_loose, w_tidy, r_loose, r_tidy

assert run([104, 102, 106, 101, 103, 105, 107], 107) == (7, 14, 7, 3)
_ids = [101 + (i * 37) % 700 for i in range(700)]
assert len(set(_ids)) == 700
assert run(_ids, _ids[-1]) == (700, 118348, 700, 10)
# check yourself 1: ids in order, nothing moves, 7 write steps
assert run(list(range(101, 108)), 107)[1] == 7
# source: https://www.postgresql.org/docs/current/indexes-intro.html
# confirmed: "After an index is created, the system has to keep it synchronized with the table. This adds overhead to data manipulation operations."
# source: https://www.postgresql.org/docs/current/indexes-types.html
# confirmed: B-tree is the default index type, but Hash is also a type (equality only, a 32-bit hash code, not ordered), so an index is not always sorted
# source: https://en.wikipedia.org/wiki/AVL_tree
# confirmed: "Lookup, insertion, and deletion all take O(log n) time in both the average and worst cases."
# source: https://docs.python.org/3/builtins/time-complexity.html
# confirmed: list insert at index k is O(n - k), it shifts every element after k, so a balanced tree (log n) pays far less than shifting a list
