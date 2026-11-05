# checks for notes/328-venvs-one-set-of-installed-packages-per-project.md
# the terminal demo is a text block, so this reruns its observable parts
import subprocess, sys, tempfile, os, shutil
d = tempfile.mkdtemp()
try:
    subprocess.run([sys.executable, "-m", "venv", os.path.join(d, ".venv")], check=True)
    py = os.path.join(d, ".venv", "bin", "python")
    # a fresh venv does not see packages installed outside it
    r = subprocess.run([py, "-c", "import wheel_that_is_not_here"], capture_output=True, text=True)
    assert "ModuleNotFoundError" in r.stderr
    # a fresh venv starts with pip only in its own site-packages
    r = subprocess.run([py, "-c", "import sys, site; print(sys.prefix != sys.base_prefix)"], capture_output=True, text=True)
    assert r.stdout.strip() == "True"
    r = subprocess.run([py, "-m", "pip", "--version"], capture_output=True, text=True)
    assert r.returncode == 0
    # include-system-site-packages is false by default, so installed packages outside are hidden
    cfg = open(os.path.join(d, ".venv", "pyvenv.cfg")).read()
    assert "include-system-site-packages = false" in cfg
finally:
    shutil.rmtree(d)
# source: https://docs.python.org/3/library/venv.html
#   confirmed (opened this run): venv creates lightweight virtual environments, each with their own independent set of Python packages, by default isolated from packages in the base environment; ships in the standard library; to move an environment you should recreate it at the new location
# source: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
#   confirmed (opened this run): source .venv/bin/activate on unix, .venv\Scripts\activate on windows; once activated pip installs into that environment; activation puts the venv python and pip on PATH
