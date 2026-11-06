# 330: git branches, trying something without breaking main
builds on: [329 git, commits as snapshots of your code](./329-git-commits-as-snapshots-of-your-code.md), [049 the terminal, running programs by typing](./049-the-terminal.md), [040 folders and paths](./040-folders-and-paths.md), [280 trees, data that branches](./280-trees-data-that-branches.md)
section: python for data work, part 6, ~2 min read

you want to rewrite the shop report script, but the three good snapshots from [329](./329-git-commits-as-snapshots-of-your-code.md) have to stay safe. copying the whole [folder](./040-folders-and-paths.md) works, but git has a cheaper way.

a branch is a name that points at one commit, and a new commit moves only the branch you are standing on. the shop is the imaginary gujarati snack store these notes run on, and this is its report, in the [terminal](./049-the-terminal.md), with a risky rewrite on a new branch:

```text
$ git branch
* main
$ git switch -c rewrite
$ echo 'print("customers: 5")' > report.py
$ git add report.py
$ git commit -m "try a rewrite"
$ git log --oneline --all --decorate
1c7c5fd (main) add notes file
bd6972e (HEAD -> rewrite) try a rewrite
647663e add item count
bf699e9 first report
$ git switch main
$ cat report.py
print("orders: 7")
print("items: 13")
```

| branch | points at |
|---|---|
| main | 1c7c5fd |
| rewrite | bd6972e |

switch -c makes a branch and moves onto it. the rewrite commit sits one step ahead of main, which never moved. after switching back, git rewrites the files in your folder to match main, so report.py has its two lines again. the rewrite commit isnt gone, it just belongs to the other name. your ids will differ, same as in 329.

i assumed a branch was a copy of the project, but it is a 41 byte file holding one commit id, so making one is instant ([pro git](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)). main is the usual name of the first branch, older setups say master.

word clash: this branch isnt the branches of a tree in [280](./280-trees-data-that-branches.md), its a label on a commit.

if you have uncommitted edits that the other branch would overwrite, git refuses to switch until you commit them. teams lean on this: keep one branch stable, do the experiments elsewhere ([pro git](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows)).

---
prev: [329 git, commits as snapshots of your code](./329-git-commits-as-snapshots-of-your-code.md) | next: not written yet
