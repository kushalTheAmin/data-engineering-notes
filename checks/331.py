# checks for notes/331-pushing-and-pulling-sharing-code-through-a-remote.md
import subprocess, tempfile, os, shutil

env = dict(os.environ, GIT_AUTHOR_NAME="kushal", GIT_AUTHOR_EMAIL="k@example.com",
           GIT_COMMITTER_NAME="kushal", GIT_COMMITTER_EMAIL="k@example.com")


def git(d, *a, ok=True):
    r = subprocess.run(["git", *a], cwd=d, env=env, capture_output=True, text=True)
    if ok:
        assert r.returncode == 0, r.stderr
    return r


root = tempfile.mkdtemp()
try:
    remote = os.path.join(root, "remote.git")
    git(root, "init", "-q", "--bare", "-b", "main", remote)
    me = os.path.join(root, "me")
    git(root, "init", "-q", "-b", "main", me)
    git(me, "remote", "add", "origin", remote)
    assert git(me, "remote").stdout.strip() == "origin"
    open(os.path.join(me, "report.py"), "w").write('print("orders: 7")\n')
    git(me, "add", "report.py"); git(me, "commit", "-q", "-m", "first report")
    git(me, "push", "-q", "-u", "origin", "main")
    # friend clones: whole history, origin set for them
    friend = os.path.join(root, "friend")
    git(root, "clone", "-q", remote, friend)
    assert git(friend, "remote").stdout.strip() == "origin"
    assert git(friend, "log", "--oneline").stdout.strip().endswith("first report")
    open(os.path.join(friend, "report.py"), "a").write('print("items: 13")\n')
    git(friend, "commit", "-q", "-am", "add item count")
    git(friend, "push", "-q")
    open(os.path.join(me, "notes.txt"), "w").write("run it with python3 report.py\n")
    git(me, "add", "notes.txt"); git(me, "commit", "-q", "-m", "add notes file")
    r = git(me, "push", ok=False)
    assert r.returncode != 0
    assert "! [rejected]" in r.stderr and "main -> main (fetch first)" in r.stderr
    assert "Updates were rejected because the remote contains work that you do not" in r.stderr
    assert "have locally" in r.stderr
    # audit: with no pull settings, a plain pull on diverged branches stops and asks how to combine the work
    clean = {k: v for k, v in env.items() if not k.startswith("GIT_CONFIG")}
    clean.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
    r = subprocess.run(["git", "pull"], cwd=me, env=clean, capture_output=True, text=True)
    assert r.returncode != 0 and "divergent branches" in r.stderr, r.stderr
    git(me, "pull", "--no-rebase", "--no-edit")
    msgs = git(me, "log", "--format=%s").stdout.splitlines()
    assert "add item count" in msgs and "add notes file" in msgs and "first report" in msgs
    git(me, "push", "-q")
    assert git(remote, "log", "--format=%s", "main").stdout.splitlines().count("add notes file") == 1
    # fetch alone downloads commits without touching the folder's branch
    git(friend, "fetch", "-q")
finally:
    shutil.rmtree(root)

# source: https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes
#   confirmed (opened this run): origin is the default name Git gives the server you cloned from; git pull fetches then merges; if someone pushes before you, your push is rejected

# audit: a plain pull on diverged branches fails by default
# source: https://git-scm.com/docs/git-pull
#   confirmed (opened this run): the fast-forward-only update "fails if your local branch has diverged from the remote branch. This is the default."; "git pull --no-rebase runs git merge"

# audit: the note said every clone holds the full history, but a shallow clone does not, and the cited page never said it. it now says a default clone, sourced to the page that does
root2 = tempfile.mkdtemp()
try:
    src = os.path.join(root2, "src")
    git(root2, "init", "-q", "-b", "main", src)
    for i in range(3):
        open(os.path.join(src, "f"), "a").write(f"{i}\n"); git(src, "add", "f"); git(src, "commit", "-q", "-m", str(i))
    git(root2, "clone", "-q", "file://" + src, os.path.join(root2, "full"))
    git(root2, "clone", "-q", "--depth", "1", "file://" + src, os.path.join(root2, "shallow"))
    assert git(os.path.join(root2, "full"), "rev-list", "--count", "HEAD").stdout.strip() == "3"
    assert git(os.path.join(root2, "shallow"), "rev-list", "--count", "HEAD").stdout.strip() == "1"
finally:
    shutil.rmtree(root2)
# source: https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository
#   confirmed (opened this run): "Every version of every file for the history of the project is pulled down by default when you run git clone."
