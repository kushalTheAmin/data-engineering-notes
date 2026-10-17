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
# source: https://man7.org/linux/man-pages/man1/kill.1.html
# confirmed: the kill command's arguments are process ids (pid), it sends a signal to them
# source: https://en.wikipedia.org/wiki/Process_(computing)
# confirmed: a process is the instance of a computer program being executed; processes must share parts of their address spaces to communicate, so by default they are separate
print("050 ok")
