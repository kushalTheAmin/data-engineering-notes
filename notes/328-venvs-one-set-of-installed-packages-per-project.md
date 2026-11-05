# 328: venvs, one set of installed packages per project
builds on: [327 packages and pip, installing code other people wrote](./327-packages-and-pip-installing-code-other-people-wrote.md), [325 modules and imports, using code from other files](./325-modules-and-imports-using-code-from-other-files.md), [049 the terminal, running programs by typing](./049-the-terminal.md), [040 folders and paths](./040-folders-and-paths.md)
section: python for data work, part 4, ~2 min read

[327](./327-packages-and-pip-installing-code-other-people-wrote.md) ended with every package landing in one shared place. so what happens when the shop report script needs an older duckdb, a small database program, and its loader script needs a newer one? that place holds one version of a [package](./327-packages-and-pip-installing-code-other-people-wrote.md), code other people shared, at a time, so installing one replaces the other.

a venv, short for virtual environment, is a [folder](./040-folders-and-paths.md) with its own python and its own installed packages, usually one per project. here is the shop, the imaginary gujarati snack store these notes run on, with a fresh venv in the [terminal](./049-the-terminal.md), on a machine where duckdb is already installed:

```text
$ python3 -c "import duckdb"
$ python3 -m venv .venv
$ .venv/bin/python -c "import duckdb"
ModuleNotFoundError: No module named 'duckdb'
$ .venv/bin/python -m pip install duckdb
$ .venv/bin/python -c "import duckdb"
```

the first line prints nothing, which means the [import](./325-modules-and-imports-using-code-from-other-files.md) worked. the third fails with ModuleNotFoundError, python saying it cant find that package, though duckdb sits right there on the machine. i expected a new venv to inherit everything, but it starts empty on purpose, with little but pip, the installer from 327, inside. you install into it with its own python, and only code run by that python sees the result.

typing .venv/bin/python each time gets old, so people run source .venv/bin/activate once, after which plain python3 and pip mean the venvs ones. ([guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/), windows uses Scripts, not bin).

each project has its own venv, so nothing fights over a version. python itself ships the venv module ([docs](https://docs.python.org/3/library/venv.html)), but a venv breaks if you move it, the docs say recreate it, so you share a list of what to install instead.

---
prev: [327 packages and pip, installing code other people wrote](./327-packages-and-pip-installing-code-other-people-wrote.md) | next: not written yet
