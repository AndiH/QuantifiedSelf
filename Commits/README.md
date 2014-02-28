# Quantified Self: Git Commits

This set of scripts create an entry in a database for every Git commit, keeping track of my coding productivity.

Everytime a `git commit` is invoked, an entry into my database is created with some of the commit's information. A Git hook is used for this.
Also, there's a script to import old Git commits.

Just go through this readme from top to bottom and you're set. The paths chosen in the following examples are just some choices, feel free to use your own.


## Setup
#### 1. git-hooks
Benjamin Meyer's **`git-hooks`** are needed: [https://github.com/icefox/git-hooks](https://github.com/icefox/git-hooks)

Clone git-hooks' repository locally and create a symlink for the executable in `/usr/local/bin` to put it to your $PATH. For example like this:

    cd /usr/local
    git clone https://github.com/icefox/git-hooks
    ln -s /usr/local/git-hooks/git-hooks /usr/local/bin

Finally, create the user directory for git hooks:

    mkdir -p ~/.git_hooks/post-commit/

#### 2. GitPython module
These scripts collect information from the Git repositories with the help of the [GitPython module](https://github.com/gitpython-developers/GitPython). To install, simply run

    easy_install gitpython

A `pip install gitpython` should also be possible, though.

#### 3. Initialize commit scripts
Clone this repo to somewhere. Use `createLocalDb.py` to create an empty SQLite3 database in the current directory.

**Fix the absolute path in `updateLocalDb.py` (line 11) to match your setup**.

#### 4. Setup the Git hook
Symlink the `updateLocalDb.py` from this repository into the directory created in step 1:

    ln -s updateLocalDb.py ~/.git_hooks/post-commit/

Then, install git-hooks to run after each new commit. Run `git hooks --installglobal` to install the hook for all future repos. Run `git hooks --install` for your current working repo (and, subsequently, all other already existing repos).  
Alternatively, let the import script (next step) install git-hooks into found repositories. Finally, test it with `git hooks`.

#### 5. (*Optional*) Import old commits and install Git hooks
If you want all **old commits** to be imported into the database, run the script `importLocalCommits.py` -- be aware it might take a while.  
To specify the paths it should search through, use the `--paths` argument like this:

    ./importLocalCommits.py --paths /path/to/repositories/ /another/path/

Depending on the directories you are scanning, this might take a while.

To install the Git hook for all Git repositories `importLocalCommits.py` has found while scanning, it offers up the option `--install-hooks` as a parameter.


## Files
  * `createLocalDb.py` – Setups an SQLite3 database in which every commit is stored. More precisely, three columns are created: The hash value of the current commit, it's date and the commit message. Help output:

        usage: createLocalDb.py [-h] [--dropDB]

        Initializes the local database for Git commits.

        optional arguments:
          -h, --help  show this help message and exit
          --dropDB    drop the database if it already exists

  * `updateLocalDb.py` – Updates the database created by `createLocalDb.py`. It is called by Git's `post_commit` hook and puts the latest commit from the current working directory in the database. No arguments passable.

  * `importLocalCommits.py` — Searches for Git repositories in the user's home directory and extracts the commits made so far. Calls functions to extract data from `updateLocalDb.py`. Only commits from the local user are considered. Help output:

        usage: importLocalCommits.py [-h] [--install-hooks] [--max-repos N]
                                     [--no-recursive] [--paths PATHS [PATHS ...]]

        Search for existing Git repositories and import commits made by the local
        user.

        optional arguments:
          -h, --help            show this help message and exit
          --install-hooks       install git-hooks in found directories
          --max-repos N         stop scanning after N repositories
          --no-recursive        don't scan recursively
          --paths PATHS [PATHS ...]
                                Paths to recursively scan for Git repositories. If not
                                specified, the user's home directory (~/) is scanned.
  * `createRemoteDb.py` — Creates a remote table in a MySQL database, with same structure as the SQLite3 local one. Credentials are provided via a `sqlInfo.py` file.
  * `syncSqliteToMysql.py` — Synchronizes the content of the local database with a remote one. Uses `common/sqliteToMySql.py` as an abstract updater.
  * `com.andi.commitsSync.plist` — An example launchctl script which calls `syncSqliteToMysql.py` everytime `gitCommits.db` is updated.


## Todo
  * Take care of the absolute directory in updateLocalDb.py. Config file?

## Known Limits
  * This will only work locally. It's intended, since I'm working with multiple computers at a time.
