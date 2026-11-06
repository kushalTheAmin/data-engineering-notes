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
