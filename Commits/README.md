# Quantified Self: Git Commits

This set of scripts create an entry in a database for every Git commit, keeping track of my coding productivity.

Benjamin Meyer's `git-hooks` are needed: [https://github.com/icefox/git-hooks](https://github.com/icefox/git-hooks)

## Setup
Clone this repo to somewhere. Use `createLocalDb.py` to create an empty SQLite3 db.

Clone aforementioned `git-hooks` repository to `/usr/local`, symlink `/usr/local/git-hooks/git-hooks/` from `/usr/local/bin/git-hooks` to put the executable to your $PATH.  
Create `~/.git_hooks/post-commit/` and symlink `updateDatabase` from there (`ln -s updateDatabase ~/.git_hooks/post-commit/updateDatabase`).

Fix the absolute paths in both `updateDatabase` and `updateLocalDb.py` to match your setup.

Run `git hooks --installglobal` to install the hook for all future repos. Run `git hooks --install` for your current working repo (and, subsequently, all other already existing repos). Finally, test it with `git hooks`.

## Files
  * `createLocalDb.py` – Setups an SQLite3 database in which every commit is stored. More precisely, three columns are created: The hash value of the current commit, it's date and the commit message.
  * `updateLocalDb.py` – Updates the database created by `createLocalDb.py`. One argument is needed when calling the script (the hash of the commit), two are optional and set to default values if not provided (the date of the commit, the commit message).
  * `updateDatabase` — (*Shell script*) The file actually called by Git's `post_commit` hook. Retrieves the commit's hash, it's date and message and calls `updateLocalDb.py` with it.


## Todo
  * Include some repo identifier into database (maybe `basename _'_git rev-parse --show-toplevel_'_`) ← remember the apostrophes
  * Merge the shell script `updateDatabase` into the Python `updateLocalDb.py` script to call this one directly. Should be possible from git hooks' perspective, I think. Advantage: No need to take care of multiple files. Simplicity.
  * Include a duplicity check on the hash key value in the sql db prior to trying to update the db.
  * Take care of the absolute directories in the files. They are ugly. (Maybe this can be easier done when first taking care of merging the shell script into the Python one.)
  * Write a cronjob / launchctl script to transfer data to remote MySQL db from different computers used for coding

## Known Limits
  * This will only work locally and only for the last commit
    * Pull requests, website edits, whatnots will not be covered in the database (they shouldn't, though, if I'm not the author…)
    * A **TODO** would be to check not only for the last commit but for the last 20 commits and, if necessary, update the database accordingly. If above Todos are done, this souldn't be a problem. Additional todo coming out of this one: Include the other name into the scripts to match against.
