# checks for notes/037-disk-is-slow.md
# source: https://gist.github.com/jboner/2841832
#   confirmed: "Main memory reference 100 ns", "Read 4K randomly from SSD* 150,000 ns 150 us", "Disk seek 10,000,000 ns 10 ms"
# source: https://www.postgresql.org/docs/current/runtime-config-resource.html
#   confirmed: shared_buffers "Sets the amount of memory the database server uses for shared memory buffers"
# source: https://en.wikipedia.org/wiki/Hard_disk_drive
#   confirmed: delays on a hard drive are "mostly related to the mechanical nature of the rotating disks and moving heads"; the factors listed are seek time (head travel) and rotational latency (waiting for the disk to turn)
# source: https://en.wikipedia.org/wiki/Cache_(computing)
#   confirmed: "Database caching can substantially improve the throughput of database applications, for example in the processing of indexes, data dictionaries, and frequently used subsets of data"
mem, ssd, disk = 100, 150_000, 10_000_000
assert ssd // 1000 == 150  # 150 microseconds
assert disk // 1_000_000 == 10  # 10 milliseconds
assert mem == 1 * 60 + 40 and mem // 60 == 1 and mem % 60 == 40  # 1 min 40 s at 1 ns = 1 s
assert ssd == 1 * 86400 + 17 * 3600 + 40 * 60
assert disk == 115 * 86400 + 17 * 3600 + 46 * 60 + 40
assert ssd / mem == 1500
assert round(disk / ssd) == 67
assert 1000 * disk / 1_000_000_000 == 10
assert round(disk / ssd, 1) == 66.7
print("037 ok")
