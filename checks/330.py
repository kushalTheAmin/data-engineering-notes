# checks for notes/330-git-branches-trying-something-without-breaking-main.md
import subprocess, tempfile, os, shutil

env = dict(os.environ, GIT_AUTHOR_NAME="kushal", GIT_AUTHOR_EMAIL="k@example.com",
           GIT_COMMITTER_NAME="kushal", GIT_COMMITTER_EMAIL="k@example.com",
           GIT_AUTHOR_DATE="2026-01-01T10:00:00 +0000", GIT_COMMITTER_DATE="2026-01-01T10:00:00 +0000")


def git(d, *a, ok=True):
    r = subprocess.run(["git", *a], cwd=d, env=env, capture_output=True, text=True)
    if ok:
        assert r.returncode == 0, r.stderr
    return r


d = tempfile.mkdtemp()
try:
    git(d, "init", "-q", "-b", "main")
    p = os.path.join(d, "report.py")
    open(p, "w").write('print("orders: 7")\n')
    git(d, "add", "report.py"); git(d, "commit", "-q", "-m", "first report")
    open(p, "a").write('print("items: 13")\n')
    git(d, "add", "report.py"); git(d, "commit", "-q", "-m", "add item count")
    open(os.path.join(d, "notes.txt"), "w").write("run it with python3 report.py\n")
    git(d, "add", "notes.txt"); git(d, "commit", "-q", "-m", "add notes file")
    assert git(d, "branch").stdout == "* main\n"
    git(d, "switch", "-c", "rewrite")
    open(p, "w").write('print("customers: 5")\n')
    git(d, "add", "report.py"); git(d, "commit", "-q", "-m", "try a rewrite")
    log = git(d, "log", "--oneline", "--all", "--decorate").stdout.splitlines()
    # these fixed timestamps tie, so log order here is arbitrary; the order is asserted below with real, rising times
    assert sorted(log) == sorted(["1c7c5fd (main) add notes file", "bd6972e (HEAD -> rewrite) try a rewrite",
                                  "647663e add item count", "bf699e9 first report"]), log
    # table: where each branch points
    assert git(d, "rev-parse", "--short", "main").stdout.strip() == "1c7c5fd"
    assert git(d, "rev-parse", "--short", "rewrite").stdout.strip() == "bd6972e"
    # switching back rewrites the folder to main's snapshot
    git(d, "switch", "main")
    assert open(p).read() == 'print("orders: 7")\nprint("items: 13")\n'
    # the branch is a 41 byte file: 40 hex characters and a newline
    ref = os.path.join(d, ".git", "refs", "heads", "rewrite")
    assert os.path.getsize(ref) == 41 and open(ref).read().strip() == git(d, "rev-parse", "rewrite").stdout.strip()
    # audit: 41 bytes holds for sha1 loose refs only; sha256 refs are 65 bytes, and pack-refs removes the loose file
    git(d, "pack-refs", "--all")
    assert not os.path.exists(ref) and "refs/heads/rewrite" in open(os.path.join(d, ".git", "packed-refs")).read()
    d2 = tempfile.mkdtemp()
    try:
        git(d2, "init", "-q", "-b", "main", "--object-format=sha256")
        open(os.path.join(d2, "f"), "w").write("x\n")
        git(d2, "add", "f"); git(d2, "commit", "-q", "-m", "m")
        assert os.path.getsize(os.path.join(d2, ".git", "refs", "heads", "main")) == 65
    finally:
        shutil.rmtree(d2)
    # uncommitted edit that the other branch would overwrite: switch is refused
    open(p, "a").write("x\n")
    r = git(d, "switch", "rewrite", ok=False)
    assert r.returncode != 0 and "overwritten" in r.stderr
    assert git(d, "branch", "--show-current").stdout.strip() == "main"
finally:
    shutil.rmtree(d)

# audit: the note listed main above the newer rewrite commit, which only happens when timestamps tie. with rising times the newest commit prints first
d3 = tempfile.mkdtemp()
try:
    def at(day):
        e = dict(env, GIT_AUTHOR_DATE=f"2026-01-0{day}T10:00:00 +0000", GIT_COMMITTER_DATE=f"2026-01-0{day}T10:00:00 +0000")
        return e
    def g3(*a, e=env):
        r = subprocess.run(["git", *a], cwd=d3, env=e, capture_output=True, text=True); assert r.returncode == 0, r.stderr; return r.stdout
    g3("init", "-q", "-b", "main")
    for i, m in enumerate(["first report", "add item count", "add notes file"], 1):
        open(os.path.join(d3, "f"), "a").write(m + "\n"); g3("add", "f"); g3("commit", "-q", "-m", m, e=at(i))
    g3("switch", "-q", "-c", "rewrite"); open(os.path.join(d3, "f"), "w").write("x\n"); g3("add", "f"); g3("commit", "-q", "-m", "try a rewrite", e=at(4))
    g3("switch", "-q", "main")
    order = [l.split(" ", 1)[1].replace("(HEAD -> main) ", "").replace("(main) ", "").replace("(HEAD -> rewrite) ", "").replace("(rewrite) ", "") for l in g3("log", "--oneline", "--all", "--decorate").splitlines()]
    assert order == ["try a rewrite", "add notes file", "add item count", "first report"], order
finally:
    shutil.rmtree(d3)

# source: https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell
#   confirmed (opened this run): "Creating a new branch is as quick and simple as writing 41 bytes to a file (40 characters and a newline)"; the default branch name in Git is master
# source: https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows
#   confirmed (opened this run): many developers keep only entirely stable code in their master branch and use other branches for topic work
# source: https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging
#   confirmed (opened this run): Git won't let you switch branches if uncommitted changes conflict with the branch you're checking out
# source: https://git-scm.com/docs/git-pack-refs
#   confirmed (opened this run): refs are stored under $GIT_DIR/refs, and git pack-refs puts them into $GIT_DIR/packed-refs, usually removing the loose refs

# audit: stock git names the first branch master, so the note's * main only appears if init.defaultBranch is set
# source: https://git-scm.com/docs/git-init
#   confirmed (opened this run): "fall back to the default name (currently master, but this will change to main when Git 3.0 is released). The default name can be customized via the init.defaultBranch configuration variable."
