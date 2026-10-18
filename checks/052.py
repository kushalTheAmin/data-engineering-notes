# checks for notes/052-the-working-directory.md
import os
import subprocess
import tempfile

with tempfile.TemporaryDirectory() as d:
    for sub in ("exports", "backup"):
        os.makedirs(os.path.join(d, "shop", sub))
        open(os.path.join(d, "shop", sub, "orders.csv"), "w").close()
    script = "cd {0}/shop/exports; pwd; ls; cd {0}/shop/backup; pwd; ls".format(d)
    out = subprocess.run(["bash", "-c", script], capture_output=True, text=True).stdout.split("\n")
    assert out[:-1] == [d + "/shop/exports", "orders.csv", d + "/shop/backup", "orders.csv"]
    # a bare name is looked up from the working directory
    a = subprocess.run(["python3", "-c", "print(open('orders.csv').name)"], cwd=d + "/shop/exports", capture_output=True, text=True)
    assert a.stdout.strip() == "orders.csv"
    # a child that changes its own directory leaves the parent where it was
    before = os.getcwd()
    subprocess.run(["python3", "-c", "import os; os.chdir('/')"])
    assert os.getcwd() == before
    # a new process starts in the working directory of the one that started it
    child = subprocess.run(["python3", "-c", "import os; print(os.getcwd())"], cwd=d, capture_output=True, text=True)
    assert os.path.realpath(child.stdout.strip()) == os.path.realpath(d)
# cd is built into bash
assert subprocess.run(["bash", "-c", "type cd"], capture_output=True, text=True).stdout.startswith("cd is a shell builtin")
# source: https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html
#   confirmed: cd is a bourne shell builtin, "Change the current working directory"
# source: https://man7.org/linux/man-pages/man1/pwd.1.html
#   confirmed: pwd prints the name of the current/working directory
# source: https://man7.org/linux/man-pages/man2/chdir.2.html
#   confirmed: chdir changes the current working directory of the calling process
# source: https://man7.org/linux/man-pages/man1/ls.1.html
#   confirmed: "List information about the FILEs (the current directory by default)"
# source: https://en.wikipedia.org/wiki/Working_directory
#   confirmed: "Typically, each process has a separate working directory"
# source: https://pubs.opengroup.org/onlinepubs/9699919799/functions/fork.html
#   confirmed: "The new process (child process) shall be an exact copy of the calling process (parent process) except as detailed below", and the working directory is not among the exceptions
print("052 ok")
