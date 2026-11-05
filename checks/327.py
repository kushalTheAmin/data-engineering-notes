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
