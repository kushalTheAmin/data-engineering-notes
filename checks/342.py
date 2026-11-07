# checks for notes/342-environment-variables-settings-that-live-outside-the-code.md
import os, sys, subprocess, tempfile
sys.path.insert(0, os.path.dirname(__file__))
src = open(os.path.join(os.path.dirname(__file__), "..", "notes", "342-environment-variables-settings-that-live-outside-the-code.md")).read()
# the text block: report.py and three runs, rerun for real
tb = src.split("```text\n")[1].split("```", 1)[0]
script = "\n".join(l[4:] for l in tb.split("\n\n")[0].splitlines()[1:])
d = tempfile.mkdtemp()
open(os.path.join(d, "report.py"), "w").write(script + "\n")
def run(extra):
    env = {k: v for k, v in os.environ.items() if k not in ("SHOP_API_KEY", "ROW_LIMIT")}
    env.update(extra)
    return subprocess.run([sys.executable, "-I", os.path.join(d, "report.py")], capture_output=True, text=True, env=env)
r = run({})
assert r.stderr.strip().splitlines()[-1] == "KeyError: 'SHOP_API_KEY'", r.stderr
r = run({"SHOP_API_KEY": "k_report_7f3a"})
assert r.stdout.strip() == "k_re... 100", r.stdout
r = run({"SHOP_API_KEY": "k_report_7f3a", "ROW_LIMIT": "5"})
assert r.stdout.strip() == "k_re... 5", r.stdout
assert "k_re... 100\n" in tb and "k_re... 5\n" in tb and "KeyError: 'SHOP_API_KEY'" in tb
# values are text; comparing a number with text fails
os.environ["ROW_LIMIT"] = "5"
assert os.environ["ROW_LIMIT"] == "5" and isinstance(os.environ["ROW_LIMIT"], str)
try:
    7 > os.environ["ROW_LIMIT"]
    raise SystemExit("should fail")
except TypeError:
    pass
# a typo in the name with .get quietly gives the default
assert os.environ.get("ROW_LIMT", "100") == "100"
# child processes get a copy; a second shell has its own list
child = "import os; print(os.environ.get('SHOP_API_KEY'))"
out = subprocess.run([sys.executable, "-I", "-c", child], capture_output=True, text=True, env={"SHOP_API_KEY": "x"}).stdout.strip()
assert out == "x"
out = subprocess.run([sys.executable, "-I", "-c", child], capture_output=True, text=True, env={}).stdout.strip()
assert out == "None"
# the answer block
blocks = [b.split("```", 1)[0] for b in src.split("```python\n")[1:]]
r = subprocess.run([sys.executable, "-I", "-c", blocks[0]], capture_output=True, text=True)
assert r.stdout.strip() == "7", r.stdout
# the shop has 7 orders
from _shop import shop
assert shop().execute("SELECT count(*) FROM orders").fetchone()[0] == 7
# source: https://docs.python.org/3/library/os.html
# confirmed (opened this run): os.environ is a mapping of string keys and values representing the process environment, captured at python startup
# source: https://docs.python.org/3/library/subprocess.html
# confirmed (opened this run): by default a new process inherits the current process environment, env= replaces it
# audit: os.environ is a mapping object, not a dict
assert not isinstance(os.environ, dict)
# audit: a deleted key stays in git history (real repo, git show of the old commit)
g = tempfile.mkdtemp()
def git(*a): return subprocess.run(["git", "-C", g, "-c", "user.name=t", "-c", "user.email=t@t", *a], capture_output=True, text=True).stdout
git("init", "-q")
open(os.path.join(g, "a.py"), "w").write("key = 'k_report_7f3a'\n")
git("add", "a.py"); git("commit", "-qm", "one")
open(os.path.join(g, "a.py"), "w").write("")
git("add", "a.py"); git("commit", "-qm", "two")
assert "k_report_7f3a" in git("show", "HEAD~1:a.py") and "k_report_7f3a" not in git("show", "HEAD:a.py")
# source: https://docs.python.org/3/library/os.html
# confirmed (opened this run): os.environ is "A mapping object where keys and values are strings that represent the process environment", so dictionary-like, not a dict
# audit: NAME=value before a command sets it for that command only (bash)
out = subprocess.run(["bash", "-c", "SHOP_API_KEY=x python3 -I -c 'import os;print(os.environ.get(\"SHOP_API_KEY\"))'; python3 -I -c 'import os;print(os.environ.get(\"SHOP_API_KEY\"))'"], capture_output=True, text=True, env={"PATH": os.environ["PATH"]}).stdout.split()
assert out == ["x", "None"], out
# source: https://www.gnu.org/software/bash/manual/html_node/Environment.html
# confirmed (opened this run): variable assignments before a simple command "are part of that command's environment for as long as it executes. These assignment statements affect only the environment seen by that command"
# audit: export sets a variable for programs started from that shell, not for a second shell
out = subprocess.run(["bash", "-c", "export SHOP_API_KEY=k; python3 -I -c 'import os;print(os.environ.get(\"SHOP_API_KEY\"))'; env -i PATH=\"$PATH\" bash -c 'python3 -I -c \"import os;print(os.environ.get(\\\"SHOP_API_KEY\\\"))\"'"], capture_output=True, text=True, env={"PATH": os.environ["PATH"]}).stdout.split()
assert out == ["k", "None"], out
# source: https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html
# confirmed (opened this run): export "Mark each name to be passed to subsequently executed commands in the environment"
