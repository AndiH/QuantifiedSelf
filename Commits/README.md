# Quantified Self: Git Commits

These set of scripts make an entry in a database for every Git commit, keeping track of my coding productivity.

Benjamin Meyer's `git-hooks` are needed: [https://github.com/icefox/git-hooks](https://github.com/icefox/git-hooks)

## Setup
Use `createLocalDb.py` to create an empty SQLite3 db. Clone aforementioned `git-hooks` repository to `/usr/local`, symlink `/usr/local/git-hooks/git-hooks/` from `/usr/local/bin/git-hooks`.

Create `~/.git_hooks/post-commit/` and symlink `updateDatabase` from there (`ln -s updateDatabase ~/.git_hooks/post-commit/updateDatabase`).

Fix the absolute paths in both `updateDatabase` and `updateLocalDb.py` to match your setup.

Run `git hooks --installglobal` to install the hook for all future repos. Run `git hooks --install` for every current working repo. Finally, test it with `git hooks`.

## Files


## Todo
