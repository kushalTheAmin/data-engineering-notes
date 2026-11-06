# checks for notes/333-pull-requests-asking-for-a-review-before-merging.md
import subprocess, tempfile, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop

# source: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
#   confirmed: pull requests are proposals to merge code changes, GitHub's collaboration feature for review before merging
# source: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request
#   confirmed: after opening you can keep changing files by adding new commits to your head branch
# source: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews
#   confirmed: reviewers comment, approve or request changes
# source: https://docs.gitlab.com/user/project/merge_requests/
#   confirmed: GitLab calls it a merge request, with reviewers who can approve
# source: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/about-merge-conflicts
#   confirmed: conflicts in a pull request are resolved on GitHub or in a local clone and pushed to the pull request branch

con = shop()
assert con.execute("SELECT count(*) FROM orders").fetchone()[0] == 7
assert con.execute("SELECT count(*) FROM order_items").fetchone()[0] == 13
assert con.execute("SELECT count(*) FROM customers").fetchone()[0] == 5

# the diff: git itself shows - and + lines for the rewrite
env = dict(os.environ, GIT_AUTHOR_NAME="k", GIT_AUTHOR_EMAIL="k@e.com", GIT_COMMITTER_NAME="k", GIT_COMMITTER_EMAIL="k@e.com")
def git(d, *a):
    r = subprocess.run(["git", *a], cwd=d, env=env, capture_output=True, text=True); assert r.returncode == 0, r.stderr; return r.stdout
d = tempfile.mkdtemp()
git(d, "init", "-q", "-b", "main")
open(d + "/report.py", "w").write('print("orders: 7")\nprint("items: 13")\n')
git(d, "add", "."); git(d, "commit", "-q", "-m", "a")
git(d, "switch", "-q", "-c", "rewrite")
open(d + "/report.py", "w").write('print("customers: 5")\n')
git(d, "commit", "-qam", "b")
out = git(d, "diff", "main", "rewrite")
lines = [l for l in out.split("\n") if l and l[0] in "+-" and not l.startswith(("+++", "---"))]
assert lines == ['-print("orders: 7")', '-print("items: 13")', '+print("customers: 5")'], lines
