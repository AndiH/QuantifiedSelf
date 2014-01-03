# Quantified Self: Git Commits

This set of scripts create an entry in a database for every Git commit, keeping track of my coding productivity.

Benjamin Meyer's `git-hooks` are needed: [https://github.com/icefox/git-hooks](https://github.com/icefox/git-hooks)

## Setup
Use `createLocalDb.py` to create an empty SQLite3 db. Clone aforementioned `git-hooks` repository to `/usr/local`, symlink `/usr/local/git-hooks/git-hooks/` from `/usr/local/bin/git-hooks`.

Create `~/.git_hooks/post-commit/` and symlink `updateDatabase` from there (`ln -s updateDatabase ~/.git_hooks/post-commit/updateDatabase`).

Fix the absolute paths in both `updateDatabase` and `updateLocalDb.py` to match your setup.

Run `git hooks --installglobal` to install the hook for all future repos. Run `git hooks --install` for every current working repo. Finally, test it with `git hooks`.

## Files
  * `createLocalDb.py` – Setups an SQLite3 database in which every commit is stored. More precisely, three columns are created: The hash value of the current commit, it's date and the commit message.
  * `updateLocalDb.py` – Updates the database created by `createLocalDb.py`. One argument is needed when calling the script (the hash of the commit), two are optional and set to default values if not provided (the date of the commit, the commit message).
  * `updateDatabase` — (Shell script) The file actually called by Git's `post_commit` hook. Retrieves the commit's hash, it's date and message and calls `updateLocalDb.py` with it.


## Todo
