# checks for notes/051-the-operating-system.md
loader, report = 3, 2
rows = []
for who in "lrlrl":
    if who == "l":
        loader -= 1
    else:
        report -= 1
    rows.append((loader, report))
assert rows == [(2, 2), (2, 1), (1, 1), (1, 0), (0, 0)]
# report finishes on turn 4, loader on turn 5
assert rows.index((1, 0)) + 1 == 4
assert rows.index((0, 0)) + 1 == 5
# source: https://en.wikipedia.org/wiki/Operating_system
# confirmed: Windows, macOS and Linux are operating systems; application code frequently makes system calls to an OS function; most operating systems interrupt a thread (preemptive multitasking) so it cannot monopolize the processor
# source: https://en.wikipedia.org/wiki/Multi-core_processor
#   confirmed: a multi-core processor has "two or more separate central processing units (CPUs), called cores"
print("051 ok")
