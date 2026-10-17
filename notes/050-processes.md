# 050: processes, a program while it runs
builds on: [036 memory vs disk, one forgets and one remembers](./036-memory-vs-disk.md), [039 a file is a named list of bytes](./039-a-file-is-a-named-list-of-bytes.md), [049 the terminal, running programs by typing](./049-the-terminal.md)
section: memory, disks and files, part 16, ~2 min read

if you start the same program twice and stop one, why does the other keep going?

a process is one running copy of a program. the program is a file of bytes (groups of 8 bits) on disk, storage that keeps them without power, like [039](./039-a-file-is-a-named-list-of-bytes.md) built. when you press enter in the [terminal](./049-the-terminal.md), the text window where you type commands, the operating system, the software running the machine, loads the program into [memory](./036-memory-vs-disk.md), the working space that forgets at power off. that running copy gets a number called a process id, or pid.

the shop, the imaginary gujarati snack store these notes run on, could start its order loader twice at once, and the difference looks like this:

| | program | process |
|---|---|---|
| what | a file | a running copy |
| lives in | disk | memory |
| how many | 1 file | one per run |
| name | its path | a pid, unique among running ones |
| after a power cut | still there | gone |

sleep is a program that just waits, so it makes a clean example. here python starts it twice (Popen starts a program, and poll() gives None while it still runs):

```python
import subprocess
a = subprocess.Popen(["sleep", "5"])
b = subprocess.Popen(["sleep", "5"])
print(a.pid != b.pid)
a.kill()
a.wait()
print("a still running:", a.poll() is None)
print("b still running:", b.poll() is None)
b.kill()
```

```output
True
a still running: False
b still running: True
```

same file, two pids, and stopping a leaves b alone. each process gets its own memory, and by default other processes cant read it.

i kept using "program" and "the thing running" as one noun, and the pid is what shows theyre two. the file doesnt change when a process dies, only that copy in memory goes.

the terminal command kill stops a process by its pid, not by program name. python wraps that in a.kill().

---
prev: [049 the terminal, running programs by typing](./049-the-terminal.md) | next: not written yet
