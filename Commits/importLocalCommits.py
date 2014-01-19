#!/usr/bin/env python
import os
import git
import updateLocalDb

# configuration values
_pathToDB = '/Users/andre/Development/QuantifiedSelf/Commits/gitCommits.db'


def getLocalGitRepos():
  listOfRepos = []
  for root, dirs, files in os.walk(os.path.expanduser('~/')):
    if '.git' in dirs:
      listOfRepos.append(root)

    # during development we don't want to wait too long
    if len(listOfRepos) > 3:
      break
  return listOfRepos


if __name__ == "__main__":
  commitCounter = 0

  # get all local repositories (this might take a while)
  localGitRepos = getLocalGitRepos()

  for repoPath in localGitRepos:
    # get the relevant infos from the repository
    repoInfo = updateLocalDb.extractRepoInfo(git.Repo(repoPath))
    commitCounter += len(repoInfo)

    # fill everything into the database
    updateLocalDb.fillDatabase(repoInfo)

  print "Added {} commits from {} repositories.".format(commitCounter, len(localGitRepos))

