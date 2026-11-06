# 332: merge conflicts, when git cant combine two edits
builds on: [331 pushing and pulling, sharing code through a remote](./331-pushing-and-pulling-sharing-code-through-a-remote.md), [330 git branches, trying something without breaking main](./330-git-branches-trying-something-without-breaking-main.md), [329 git, commits as snapshots of your code](./329-git-commits-as-snapshots-of-your-code.md)
section: python for data work, part 8, ~2 min read

you and a friend both edited the same line of report.py, and now git has to merge them, combine two lines of work into one. which edit wins?

neither, git stops and asks you. a merge conflict is what git reports when two branches changed the same lines and it cant tell which version to keep. here is report.py from the shop, the imaginary gujarati snack store these notes run on, as three versions of the file:

| line | start | mine | friend | git does |
|---|---|---|---|---|
| 1 | orders: 7 | same | same | keeps it |
| 2 | top snack: dhokla | top snack: khandvi | top snack: jalebi | conflict |
| 3 | items: 13 | same | same | keeps it |

git compares line by line against the [commit](./329-git-commits-as-snapshots-of-your-code.md) (a saved snapshot) both [branches](./330-git-branches-trying-something-without-breaking-main.md) (names pointing at a commit) grew from. a line only one side changed, git keeps. line 2 changed on both, so git gives up on it and writes both versions into the file:

```text
$ git merge friend
Auto-merging report.py
CONFLICT (content): Merge conflict in report.py
Automatic merge failed; fix conflicts and then commit the result.
$ cat report.py
print("orders: 7")
<<<<<<< HEAD
print("top snack: khandvi")
=======
print("top snack: jalebi")
>>>>>>> friend
print("items: 13")
```

above the ======= is yours (HEAD marks the branch you are on), below is your friends. you fix it by hand: keep one, or write a mix, delete the three marker lines, then git add report.py, which here means "this file is sorted", and git commit. that merge commit points back to both lines of work, and it is the merge step inside the pull from [331](./331-pushing-and-pulling-sharing-code-through-a-remote.md).

i assumed git understood the code, but it only compares lines of text. so edits on different lines merge clean even if they clash in meaning. lines that touch each other, like 2 and 3, still conflict.

the markers are ordinary text. commit them by accident and python3 report.py dies with a SyntaxError (python cant read the file) at line 2.

---

### check yourself

1. you change line 1 to print("orders: 7 placed"), your friend changes line 3 to print("items: 13 sold"), then you merge. line 2 is untouched. conflict or not?
<details><summary>answer</summary>

no conflict. the edits sit on different lines, so git keeps both and the file ends up with both new labels. the tempting answer is conflict because both of you touched report.py, but git works per line, not per file.

</details>

2. you resolve a conflict in your editor, save, run git add and git commit without deleting the marker lines. will git refuse the commit, and what happens when the team runs the script?
<details><summary>answer</summary>

git accepts it, the tempting answer that it refuses is wrong. python3 stops with a SyntaxError at the line holding the <<<<<<< marker. git only checks that the conflict was marked as handled with git add, it never reads your code, so a commit with markers inside is accepted.

</details>


---
prev: [331 pushing and pulling, sharing code through a remote](./331-pushing-and-pulling-sharing-code-through-a-remote.md) | next: not written yet
