# 330: git branches, trying something without breaking main
builds on: [329 git, commits as snapshots of your code](./329-git-commits-as-snapshots-of-your-code.md), [049 the terminal, running programs by typing](./049-the-terminal.md), [040 folders and paths](./040-folders-and-paths.md), [280 trees, data that branches](./280-trees-data-that-branches.md)
section: python for data work, part 6, ~2 min read

you want to rewrite the shop report script, but the three good snapshots from [329](./329-git-commits-as-snapshots-of-your-code.md) have to stay safe. copying the whole [folder](./040-folders-and-paths.md) works, but git has a cheaper way.

a branch is a name that points at one commit (a saved snapshot), and a new commit moves only the branch you are standing on. here is the shop, the imaginary gujarati snack store these notes run on, in the [terminal](./049-the-terminal.md), with a risky report rewrite on a new branch:

```text
$ git branch
* main
$ git switch -c rewrite
$ echo 'print("customers: 5")' > report.py
$ git add report.py
$ git commit -m "try a rewrite"
$ git log --oneline --all --decorate
bd6972e (HEAD -> rewrite) try a rewrite
1c7c5fd (main) add notes file
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

switch -c makes a branch and moves onto it, and the * in git branch and HEAD -> in the log mark the branch you are on. the rewrite commit sits one step ahead of main. after switching back, git rewrites your folder to match main, so report.py has its two lines again, while the rewrite commit lives on. your ids will differ, as in 329.

i assumed a branch was a copy of the project, but it is one commit id, stored as a 41 byte file in a default repository (git may pack it later), so making one is fast ([pro git](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)). git itself still names the first branch master unless configured, so if git branch shows master, read master for main.

word clash: this branch isnt the branches of a tree in [280](./280-trees-data-that-branches.md), its a label on a commit.

if uncommitted edits would be overwritten by the other branch, git refuses to switch until you commit them. teams keep one branch stable and experiment elsewhere ([pro git](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows)).

---
prev: [329 git, commits as snapshots of your code](./329-git-commits-as-snapshots-of-your-code.md) | next: [331 pushing and pulling, sharing code through a remote](./331-pushing-and-pulling-sharing-code-through-a-remote.md)
