# 329: git, commits as snapshots of your code
builds on: [328 venvs, one set of installed packages per project](./328-venvs-one-set-of-installed-packages-per-project.md), [326 running a python script from the terminal](./326-running-a-python-script-from-the-terminal.md), [319 cryptographic hashes, a fingerprint you cant reverse](./319-cryptographic-hashes-a-fingerprint-you-cant-reverse.md), [250 transaction snapshots, what your transaction is allowed to see](./250-transaction-snapshots-what-your-transaction-is-allowed-to-see.md), [228 commit and rollback, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md), [049 the terminal, running programs by typing](./049-the-terminal.md), [040 folders and paths](./040-folders-and-paths.md)
section: python for data work, part 5, ~2 min read

you edit the shop report script from [328](./328-venvs-one-set-of-installed-packages-per-project.md), it breaks, and you want yesterdays version back. a folder has no undo for that.

git is a tool that saves snapshots of a project [folder](./040-folders-and-paths.md), and a commit is one saved snapshot with a short message. here is report.py, a [script](./326-running-a-python-script-from-the-terminal.md), saved three times in the [terminal](./049-the-terminal.md) for the shop, the imaginary gujarati snack store these notes run on:

```text
$ git init
$ echo 'print("orders: 7")' > report.py
$ git add report.py
$ git commit -m "first report"
$ echo 'print("items: 13")' >> report.py
$ git add report.py
$ git commit -m "add item count"
$ echo "run it with python3 report.py" > notes.txt
$ git add notes.txt
$ git commit -m "add notes file"
$ git log --oneline
1c7c5fd add notes file
647663e add item count
bf699e9 first report
$ git show bf699e9:report.py
print("orders: 7")
```

| commit | message | files in the snapshot |
|---|---|---|
| bf699e9 | first report | report.py |
| 647663e | add item count | report.py |
| 1c7c5fd | add notes file | report.py, notes.txt |

echo > writes a file and >> adds a line to its end. git init makes the folder a repository with nothing saved yet, git add picks which files go into the next snapshot, git commit saves it (set your name and email with git config first). the log lists commits newest first; each id is a [fingerprint](./319-cryptographic-hashes-a-fingerprint-you-cant-reverse.md), a short code made from the snapshot, message, previous commits id, author and time, so yours will differ. git show with an id and a file name prints the file as it was then.

word clash: a git commit isnt the database COMMIT of [228](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md), which keeps a batch of changes, and this snapshot is files, not the query view of [250](./250-transaction-snapshots-what-your-transaction-is-allowed-to-see.md).

i assumed git kept a list of edits, but each commit is the whole project, and unchanged files are reused, not copied again ([pro git](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)). a diff, the list of edits, comes from comparing snapshots.

every id includes the one before it, so changing an old commit changes every id after it. next: trying a risky change without touching your good snapshot.

### check yourself

1. you commit report.py printing "orders: 7", then add the items line and commit again. what does git show print for the first commit, and why isnt it two lines?
<details><summary>answer</summary>

one line, orders: 7. each commit saved the whole folder as it was, so the second commit didnt overwrite the first. the tempting answer is two lines, from thinking the file just keeps its latest version.

</details>

2. you add a new file called todo.txt, edit report.py, then run git add report.py and git commit. does the new snapshot hold todo.txt?
<details><summary>answer</summary>

no. only files you added, plus files already saved earlier, go into a snapshot. the tempting answer is yes, because a snapshot sounds like a picture of everything in the folder.

</details>

3. the message of the first commit had been "first draft" instead. would the third commits id still be 1c7c5fd?
<details><summary>answer</summary>

no. the first id changes, so the second changes, so the third does. each id is made from the one before it. the tempting answer is that only the first one changes.

</details>

---
prev: [328 venvs, one set of installed packages per project](./328-venvs-one-set-of-installed-packages-per-project.md) | next: not written yet
