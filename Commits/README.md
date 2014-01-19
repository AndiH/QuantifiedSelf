# Quantified Self: Git Commits

This set of scripts create an entry in a database for every Git commit, keeping track of my coding productivity.

Benjamin Meyer's `git-hooks` are needed: [https://github.com/icefox/git-hooks](https://github.com/icefox/git-hooks)

## Setup
Clone this repo to somewhere. Use `createLocalDb.py` to create an empty SQLite3 db.

Clone aforementioned `git-hooks` repository to `/usr/local`, symlink `/usr/local/git-hooks/git-hooks/` from `/usr/local/bin/git-hooks` to put the executable to your $PATH.
Create `~/.git_hooks/post-commit/` and symlink `updateLocalDb.py` from there (`ln -s updateLocalDb.py ~/.git_hooks/post-commit/updateLocalDb.py`).

Fix the absolute path in `updateLocalDb.py` to match your setup. If you want all old commits to import into the database, run `importLocalCommits.py` -- be aware it might take a while.

Run `git hooks --installglobal` to install the hook for all future repos. Run `git hooks --install` for your current working repo (and, subsequently, all other already existing repos). Finally, test it with `git hooks`.

## Files
  * `createLocalDb.py` – Setups an SQLite3 database in which every commit is stored. More precisely, three columns are created: The hash value of the current commit, it's date and the commit message.
  * `updateLocalDb.py` – Updates the database created by `createLocalDb.py`. It is called by Git's `post_commit` hook and puts the latest commit from the current working directory in the database.
  * `importLocalCommits.py` — Searches for Git repositories in the user's home directory and extracts the commits made so far. Calls functions to extract data from `updateLocalDb.py`. Only commits from the local user are considered.


## Todo
  * Take care of the absolute directories in the files. They are ugly. (Maybe this can be easier done when first taking care of merging the shell script into the Python one.)
  * Write a cronjob / launchctl script to transfer data to remote MySQL db from different computers used for coding

## Known Limits
  * This will only work locally
  * Pull requests, website edits, whatnots will not be covered in the database (they shouldn't, though, if I'm not the author…)

