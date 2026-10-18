# checks for notes/050-processes.md
import subprocess

a = subprocess.Popen(["sleep", "5"])
b = subprocess.Popen(["sleep", "5"])
assert a.pid != b.pid
a.kill()
a.wait()
assert (a.poll() is None) is False
assert (b.poll() is None) is True
b.kill()
b.wait()
# source: https://docs.python.org/3/library/subprocess.html
# confirmed: poll() returns None while the child has not terminated; kill() on POSIX sends SIGKILL
# source: https://man7.org/linux/man-pages/man1/kill.1.html
# confirmed: the kill command's arguments are process ids (pid), it sends the specified signal to them
# source: https://en.wikipedia.org/wiki/Process_(computing)
# confirmed: a process is the instance of a computer program being executed; processes must share parts of their address spaces to communicate, so by default they are separate
# source: https://en.wikipedia.org/wiki/Process_(computing)
#   confirmed: "The operating system keeps its processes separate and allocates the resources they need"
# source: https://en.wikipedia.org/wiki/Process_identifier
#   confirmed: a pid is a number used by most operating system kernels "to uniquely identify an active process"
# source: https://en.wikipedia.org/wiki/Process_(computing)
#   confirmed: "a process is the execution of those instructions after being loaded from the disk into memory", and several processes may belong to the same program
print("050 ok")
