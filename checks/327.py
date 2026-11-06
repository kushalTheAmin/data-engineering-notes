# checks for notes/327-packages-and-pip-installing-code-other-people-wrote.md
import subprocess, sys
src = ('import json\nprint("json ok")\ntry:\n    import dhokla_tools\n'
       'except ModuleNotFoundError as e:\n    print(e)\n')
r = subprocess.run([sys.executable, "-I", "-c", src], capture_output=True, text=True)
assert r.stdout == "json ok\nNo module named 'dhokla_tools'\n", r.stdout
# the install name pyyaml and the import name yaml differ
assert "pyyaml" != "yaml"
# source: https://pyyaml.org/wiki/PyYAMLDocumentation
#   confirmed (opened this run): the docs use import yaml
# source: https://pypi.org/pypi/PyYAML/json
#   confirmed (opened this run): the PyPI project is named PyYAML, a YAML parser and emitter for Python
# source: https://packaging.python.org/en/latest/glossary/
#   confirmed (opened this run): PyPI is the default Package Index for the Python community, open to all Python developers to consume and distribute
# source: https://pip.pypa.io/en/stable/
#   confirmed (opened this run): pip is the package installer for Python
# source: https://pip.pypa.io/en/stable/cli/pip/
#   confirmed (opened this run): python -m pip <command> is the documented way to run pip, and it runs pip with that python
# source: https://pypi.org/pypi/duckdb/json
#   confirmed (opened this run): duckdb is a project on PyPI, and note 102 says pip install duckdb

# audit: the note said everything you install lands in one shared place, which reads as always true. it now says by default
# source: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
#   confirmed (opened this run): "While a virtual environment is activated, pip will install packages into that specific environment."

# audit: python3 -m pip is the linux and mac form, so the note now says on windows the first word is usually py
#   confirmed (opened this run): https://pip.pypa.io/en/stable/cli/pip/ lists "Windows py -m pip <command>"; https://docs.python.org/3/using/windows.html says python3 on Windows "is not meant to be widely used or recommended"

# audit: the note said installing a package means running a strangers code, but installing a wheel only unpacks files; the code runs at import. it now says using
import zipfile, tempfile, shutil, os
w = tempfile.mkdtemp()
try:
    mark = os.path.join(w, "ran.txt")
    whl = os.path.join(w, "strangerpkg-1.0-py3-none-any.whl")
    di = "strangerpkg-1.0.dist-info"
    with zipfile.ZipFile(whl, "w") as z:
        z.writestr("strangerpkg/__init__.py", f"open({mark!r}, 'w').write('ran')\n")
        z.writestr(di + "/METADATA", "Metadata-Version: 2.1\nName: strangerpkg\nVersion: 1.0\n")
        z.writestr(di + "/WHEEL", "Wheel-Version: 1.0\nGenerator: x\nRoot-Is-Purelib: true\nTag: py3-none-any\n")
        z.writestr(di + "/RECORD", "")
    subprocess.run([sys.executable, "-m", "venv", os.path.join(w, "v")], check=True)
    vpy = os.path.join(w, "v", "bin", "python")
    subprocess.run([vpy, "-m", "pip", "install", "-q", "--no-index", "--no-deps", whl], check=True, capture_output=True)
    assert not os.path.exists(mark)  # install ran none of the package's code
    subprocess.run([vpy, "-c", "import strangerpkg"], check=True)
    assert os.path.exists(mark)  # import did
finally:
    shutil.rmtree(w)
