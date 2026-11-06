# checks for notes/329-git-commits-as-snapshots-of-your-code.md
import subprocess, tempfile, os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

con = shop()
# report.py prints the shop's order count and item count
assert con.execute("SELECT count(*) FROM orders").fetchone()[0] == 7
assert con.execute("SELECT count(*) FROM order_items").fetchone()[0] == 13

env = dict(os.environ, GIT_AUTHOR_NAME="kushal", GIT_AUTHOR_EMAIL="k@example.com",
           GIT_COMMITTER_NAME="kushal", GIT_COMMITTER_EMAIL="k@example.com",
           GIT_AUTHOR_DATE="2026-01-01T10:00:00 +0000", GIT_COMMITTER_DATE="2026-01-01T10:00:00 +0000")


def git(d, *a):
    r = subprocess.run(["git", *a], cwd=d, env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return r.stdout


def build(first_msg):
    d = tempfile.mkdtemp()
    git(d, "init", "-q")
    p = os.path.join(d, "report.py")
    open(p, "w").write('print("orders: 7")\n')
    git(d, "add", "report.py"); git(d, "commit", "-q", "-m", first_msg)
    open(p, "a").write('print("items: 13")\n')
    git(d, "add", "report.py"); git(d, "commit", "-q", "-m", "add item count")
    open(os.path.join(d, "notes.txt"), "w").write("run it with python3 report.py\n")
    git(d, "add", "notes.txt"); git(d, "commit", "-q", "-m", "add notes file")
    return d

d = build("first report")
try:
    log = git(d, "log", "--oneline").splitlines()
    assert log == ["1c7c5fd add notes file", "647663e add item count", "bf699e9 first report"], log
    # the visual's table: files in each snapshot
    assert git(d, "ls-tree", "-r", "--name-only", "bf699e9").split() == ["report.py"]
    assert git(d, "ls-tree", "-r", "--name-only", "647663e").split() == ["report.py"]
    assert git(d, "ls-tree", "-r", "--name-only", "1c7c5fd").split() == ["notes.txt", "report.py"]
    # git show prints the first version, one line
    assert git(d, "show", "bf699e9:report.py") == 'print("orders: 7")\n'
    # unchanged files are reused, not stored again: same blob id in commits 2 and 3
    assert git(d, "rev-parse", "647663e:report.py") == git(d, "rev-parse", "1c7c5fd:report.py")
    # q2: a new untracked file is not in the next snapshot unless added
    open(os.path.join(d, "todo.txt"), "w").write("x\n")
    open(os.path.join(d, "report.py"), "a").write("# edit\n")
    git(d, "add", "report.py"); git(d, "commit", "-q", "-m", "edit")
    assert "todo.txt" not in git(d, "ls-tree", "-r", "--name-only", "HEAD").split()
    assert "notes.txt" in git(d, "ls-tree", "-r", "--name-only", "HEAD").split()
finally:
    shutil.rmtree(d)

# q3: a different first message changes every later id
d2 = build("first draft")
try:
    log2 = git(d2, "log", "--format=%h").split()
    assert not set(log2) & {"1c7c5fd", "647663e", "bf699e9"}, log2
finally:
    shutil.rmtree(d2)

# source: https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F
#   confirmed (opened this run): git thinks of its data as a series of snapshots; every commit takes a picture of what all files look like and stores a reference to it; if files have not changed git does not store the file again, just a link to the previous identical file
# source: https://git-scm.com/book/en/v2/Git-Internals-Git-Objects
#   confirmed (opened this run): a commit object specifies the top-level tree for the snapshot, the parent commits, the author/committer information with a timestamp, and the commit message

# audit: git init does not track files, a commit id includes author and time, and commit needs a name and email
d3 = tempfile.mkdtemp()
try:
    git(d3, "init", "-q")
    open(os.path.join(d3, "f.txt"), "w").write("x\n")
    assert git(d3, "status", "--porcelain").strip() == "?? f.txt"  # untracked right after init
    git(d3, "add", "f.txt"); git(d3, "commit", "-q", "-m", "m")
    body = git(d3, "cat-file", "-p", "HEAD")
    assert "author kushal <k@example.com> " in body and "committer " in body  # author and a timestamp are inside the commit
    env2 = dict(env, GIT_AUTHOR_NAME="someone", GIT_COMMITTER_NAME="someone")
    sha = lambda e: subprocess.run(["git", "commit-tree", "HEAD^{tree}", "-m", "m"], cwd=d3, env=e, capture_output=True, text=True).stdout
    assert sha(env) != sha(env2)  # same snapshot and message, different author, different id
    bare = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    bare.update(HOME=d3, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", EMAIL="")
    open(os.path.join(d3, "g.txt"), "w").write("y\n")
    subprocess.run(["git", "add", "g.txt"], cwd=d3, env=bare)
    r = subprocess.run(["git", "-c", "user.useConfigOnly=true", "commit", "-m", "m2"], cwd=d3, env=bare, capture_output=True, text=True)
    assert r.returncode != 0 and "identity" in r.stderr.lower(), r.stderr
finally:
    shutil.rmtree(d3)
# source: https://git-scm.com/book/en/v2/Git-Internals-Git-Objects
#   confirmed (opened this run): a commit has the tree, parents, "the author/committer information (which uses your user.name and user.email configuration settings and a timestamp)" and the message
# source: https://git-scm.com/docs/git-init
#   confirmed (opened this run): "This command creates an empty Git repository"
# source: https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup
#   confirmed (opened this run): "The first thing you should do when you install Git is to set your user name and email address ... every Git commit uses this information"
