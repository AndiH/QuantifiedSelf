# Quantified Self: Git Commits

This set of scripts create an entry in a database for every Git commit, keeping track of my coding productivity.


## Setup
#### 1. git-hooks
Benjamin Meyer's **`git-hooks`** are needed: [https://github.com/icefox/git-hooks](https://github.com/icefox/git-hooks)

Clone this repository locally and create a symlink for the executable in `/usr/local/bin` to put it to your $PATH:

    cd /usr/local
    git clone https://github.com/icefox/git-hooks
    ln -s /usr/local/git-hooks/git-hooks /usr/local/bin

#### 2. GitPyhton module
These scripts collect information from the Git repositories with the help of the [GitPython module](https://github.com/gitpython-developers/GitPython). To install is, simply run

    easy_install gitpython

#### 3. Initialize commit scripts
Clone this repo to somewhere. Use `createLocalDb.py` to create an empty SQLite3 database in the current directory.

Fix the absolute path in `updateLocalDb.py` (line 11) to match your setup. If you want all old commits to import into the database, run `importLocalCommits.py` -- be aware it might take a while. To specify the paths the it should search through, use the `--paths` argument like this:

    ./importLocalCommits.py --paths /path/to/repositories/ /another/path/

Depending on the directories you are scanning, this might take a while.

#### 4. Setup the Git hook
Create the user directory for git hooks:

    mkdir -p ~/.git_hooks/post-commit/

Now symlink the `updateLocalDb.py` from this repository into the newly created directory.

    ln -s updateLocalDb.py ~/.git_hooks/post-commit/

Then, install git-hooks to run after each new commit. Run `git hooks --installglobal` to install the hook for all future repos. Run `git hooks --install` for your current working repo (and, subsequently, all other already existing repos). Finally, test it with `git hooks`.


## Files
  * `createLocalDb.py` – Setups an SQLite3 database in which every commit is stored. More precisely, three columns are created: The hash value of the current commit, it's date and the commit message. Help output:

        usage: createLocalDb.py [-h] [--dropDB]

        Initializes the local database for Git commits.

        optional arguments:
          -h, --help  show this help message and exit
          --dropDB    drop the database if it already exists

  * `updateLocalDb.py` – Updates the database created by `createLocalDb.py`. It is called by Git's `post_commit` hook and puts the latest commit from the current working directory in the database. No arguments passable.

  * `importLocalCommits.py` — Searches for Git repositories in the user's home directory and extracts the commits made so far. Calls functions to extract data from `updateLocalDb.py`. Only commits from the local user are considered. Help output:

        usage: importLocalCommits.py [-h] [--max-repos N] [--no-recursive]
                                     [--paths PATHS [PATHS ...]]

        Search for existing Git repositories and import commits made by the local
        user.

        optional arguments:
          -h, --help            show this help message and exit
          --max-repos N         stop scanning after N repositories
          --no-recursive        don't scan recursively
          --paths PATHS [PATHS ...]
                                Paths to recursively scan for Git repositories. If not
                                specified, the user's home directory (~/) is scanned.


## Todo
  * Take care of the absolute directories in the files. They are ugly. (Maybe this can be easier done when first taking care of merging the shell script into the Python one.)
  * Write a cronjob / launchctl script to transfer data to remote MySQL db from different computers used for coding

## Known Limits
  * This will only work locally
  * Pull requests, website edits, whatnots will not be covered in the database (they shouldn't, though, if I'm not the author…)

