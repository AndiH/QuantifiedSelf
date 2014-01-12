#!/usr/bin/ python
from socket import gethostname
import os
import datetime
# import argparse
import sqlite3 as sql
import git

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


def extractRepoInfo(repo):
  commitInfo = {}
  commits = list(repo.iter_commits())

  userConf = repo.config_reader('global')
  userName = userConf.get('user', 'name')
  userEmail = userConf.get('user', 'email')
  if userEmail.startswith('"') and userEmail.endswith('"'):
    userEmail = userEmail[1:-1]

  for commit in commits:
    # check if author of commit is the same as the local user
    author = commit.author.name.encode('utf8')
    email = commit.author.email.encode('utf8')
    if author != userName or email != userEmail:
      continue

    commitHash = commit.name_rev.split(' ')[0]
    commitInfo[commitHash] = {
      'message': commit.message.encode('utf8').strip(),
      'date': datetime.datetime.fromtimestamp(commit.authored_date),
      'filesAdded': [],   # todo
      'filesChanged': [], # todo
      'filesRemoved': [], # todo
      'linesAdded': 0,    # todo
      'linesRemoved': 0   # todo
    }
  return commitInfo


def importLocalCommits(localGitRepos):
  machineName = gethostname()
  commitCounter = 0

  dbConnection = sql.connect(_pathToDB)
  with dbConnection:
    dbCursor = dbConnection.cursor()

    for repoPath in localGitRepos:
      repoInfo = extractRepoInfo(git.Repo(repoPath))
      for hash, commit in repoInfo.items():
        dbCursor.execute(
          "INSERT OR REPLACE INTO commits VALUES (?,?,?,?,?,?,?,?,?,?)",
          (
            hash,
            commit['date'].strftime("%s"),
            commit['message'],
            ','.join(commit['filesAdded']),
            ','.join(commit['filesChanged']),
            ','.join(commit['filesRemoved']),
            commit['linesAdded'],
            commit['linesRemoved'],
            repoPath,
            machineName
          )
        )
      commitCounter += len(repoInfo)

  print "Added {} commits from {} repositories.".format(commitCounter, len(localGitRepos))


if __name__ == "__main__":
  localGitRepos = getLocalGitRepos()
  importLocalCommits(localGitRepos)
