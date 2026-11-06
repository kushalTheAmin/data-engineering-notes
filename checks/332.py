# checks for notes/332-merge-conflicts-when-git-cant-combine-two-edits.md
import subprocess, tempfile, os, shutil, sys

env = dict(os.environ, GIT_AUTHOR_NAME="kushal", GIT_AUTHOR_EMAIL="k@example.com",
           GIT_COMMITTER_NAME="kushal", GIT_COMMITTER_EMAIL="k@example.com")


def git(d, *a, ok=True):
    r = subprocess.run(["git", *a], cwd=d, env=env, capture_output=True, text=True)
    if ok:
        assert r.returncode == 0, r.stderr
    return r


BASE = 'print("orders: 7")\nprint("top snack: dhokla")\nprint("items: 13")\n'


def setup(root, name):
    d = os.path.join(root, name)
    git(root, "init", "-q", "-b", "main", d)
    open(os.path.join(d, "report.py"), "w").write(BASE)
    git(d, "add", "report.py"); git(d, "commit", "-q", "-m", "first report")
    git(d, "switch", "-q", "-c", "friend")
    return d


root = tempfile.mkdtemp()
try:
    # same line edited on both sides: conflict
    d = setup(root, "a")
    p = os.path.join(d, "report.py")
    open(p, "w").write(BASE.replace("dhokla", "jalebi"))
    git(d, "commit", "-q", "-am", "friend: top snack jalebi")
    git(d, "switch", "-q", "main")
    open(p, "w").write(BASE.replace("dhokla", "khandvi"))
    git(d, "commit", "-q", "-am", "me: top snack khandvi")
    r = git(d, "merge", "friend", ok=False)
    assert r.returncode != 0
    assert "Auto-merging report.py" in r.stdout
    assert "CONFLICT (content): Merge conflict in report.py" in r.stdout
    assert "Automatic merge failed; fix conflicts and then commit the result." in r.stdout
    assert git(d, "status", "-s").stdout.strip() == "UU report.py"
    got = open(p).read()
    want = ('print("orders: 7")\n<<<<<<< HEAD\nprint("top snack: khandvi")\n=======\n'
            'print("top snack: jalebi")\n>>>>>>> friend\nprint("items: 13")\n')
    assert got == want, got
    # a script left with markers cannot even run
    r = subprocess.run([sys.executable, p], capture_output=True, text=True)
    assert r.returncode != 0 and "SyntaxError" in r.stderr, r.stderr
    assert "<<<<<<< HEAD" in r.stderr
    # resolve: keep mine, add, commit
    open(p, "w").write(BASE.replace("dhokla", "khandvi"))
    git(d, "add", "report.py"); git(d, "commit", "-q", "--no-edit")
    parents = git(d, "log", "-1", "--format=%p").stdout.split()
    assert len(parents) == 2
    assert open(p).read() == BASE.replace("dhokla", "khandvi")

    # different lines edited: merges clean (answer to question 1)
    d = setup(root, "b")
    p = os.path.join(d, "report.py")
    open(p, "w").write(BASE.replace('items: 13', 'items: 13 sold'))
    git(d, "commit", "-q", "-am", "friend: items label")
    git(d, "switch", "-q", "main")
    open(p, "w").write(BASE.replace('orders: 7', 'orders: 7 placed'))
    git(d, "commit", "-q", "-am", "me: orders label")
    r = git(d, "merge", "--no-edit", "friend")
    assert r.returncode == 0 and "CONFLICT" not in r.stdout
    assert open(p).read() == 'print("orders: 7 placed")\nprint("top snack: dhokla")\nprint("items: 13 sold")\n'

    # adjacent lines (2 and 3) touch, so they conflict
    d = setup(root, "c")
    p = os.path.join(d, "report.py")
    open(p, "w").write(BASE.replace("dhokla", "jalebi"))
    git(d, "commit", "-q", "-am", "friend line 2")
    git(d, "switch", "-q", "main")
    open(p, "w").write(BASE.replace("items: 13", "items: 13 sold"))
    git(d, "commit", "-q", "-am", "me line 3")
    r = git(d, "merge", "--no-edit", "friend", ok=False)
    assert r.returncode != 0 and "CONFLICT" in r.stdout

    # commit with markers left in is accepted after git add (question 2)
    d = setup(root, "d")
    p = os.path.join(d, "report.py")
    open(p, "w").write(BASE.replace("dhokla", "jalebi"))
    git(d, "commit", "-q", "-am", "friend")
    git(d, "switch", "-q", "main")
    open(p, "w").write(BASE.replace("dhokla", "khandvi"))
    git(d, "commit", "-q", "-am", "me")
    git(d, "merge", "friend", ok=False)
    git(d, "add", "report.py"); git(d, "commit", "-q", "--no-edit")
    assert "<<<<<<< HEAD" in open(p).read()
finally:
    shutil.rmtree(root)

# source: https://git-scm.com/docs/git-merge
#   confirmed (opened this run): conflicting changes are marked with <<<<<<<, =======, >>>>>>>; the part before ======= is typically your side, after it the other side
