# ugit

ugit is a DIY project for learning git internals. ugit will have a basic commit, checkout, branch and merge functionality of the actual git.

## Installation

Use the package manager [uv](https://docs.astral.sh/uv/getting-started/installation/) to install ugit.

```bash
$ uv pip install .
```

## Usage

Create a new empty repository.

```bash
$ ugit init
```
Read the file. Hash the content of the file using SHA-1. Store the file under ".ugit/objects/{the SHA-1 hash}
```bash
$ ugit hash-object some_file
b74a9c8f370194a4fb2443d1ba4f66fea792600c
```

Given an object OID, read objects content.
```bash
ugit cat-file b74a9c8f370194a4fb2443d1ba4f66fea792600c
```

Save a current working directory snapshot into a git object of type tree.
```bash
$ ugit write-tree
f89901d57fcafa59aebcec4fd18e80913158d741
```

Write a snapshot of a tree into current directory.
```bash
$ ugit read-tree f89901d57fcafa59aebcec4fd18e80913158d741
```

Create a new commit.
```bash
$ ugit commit -m "some-message"
```

Walk the list of commits and print them, using parents until a commit with no parent is met.

```bash
$ ugit log
$ ugit log 2e9e77122a34e61596d240a7450cb13ae08d7b3a
```

Display what was changed in the working directory since the last commit.
```bash
$ echo new_line > new_file
$ ugit diff
--- a/new_file
+++ b/new_file
@@ -0,0 +1 @@
+new_line

```

Attach a name to a commit OID.
```bash
$ ugit tag my-cool-commit d8d43b0e3a21df0c845e185d08be8e4028787069

```

Checkout a commit.
```bash
$ ugit checkout my-cool-commit
$ ugit checkout d8d43b0e3a21df0c845e185d08be8e4028787069

```

Create a new branch on a commit.
```bash
$ ugit branch my-new-branch my-cool-commit
```

List all branches
```bash
$ ugit branch
  my-new-branch
* master
```
The visualize all refs and all the commits pointed by the refs.
```bash
$ ugit k
```

Print current branch name.
```bash
$ ugit status
```

Merge a branch.
```bash
$ ugit merge my-new-branch
```