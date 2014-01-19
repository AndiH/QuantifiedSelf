#!/usr/bin/env python
from socket import gethostname
import sqlite3 as sql
import os, sys
import git


# The path to the local database, please adjust to your setting
def getPathToDB():
  return '/Users/andre/Development/QuantifiedSelf/Commits/gitCommits.db'


def getMachineName():
  return gethostname()


# Extract the repository information. If numCommits is set > 0, it will extract
# only this amount of commits.
def extractRepoInfo(repo, numCommits = 0):
  commitInfo = []
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

    commitInfo.append({
      'hash': commit.name_rev.split(' ')[0],
      'message': commit.message.encode('utf8').strip(),
      'timestamp': commit.authored_date,
      'path': repo.git_dir[:-4],
      'filesAdded': [],   # todo
      'filesChanged': [], # todo
      'filesRemoved': [], # todo
      'linesAdded': 0,    # todo
      'linesRemoved': 0,  # todo
      'machine': getMachineName()
    })

    if numCommits > 0 and len(commitInfo) >= numCommits:
      break
  return commitInfo


def fillDatabase(repoInfo):
  con = None
  try:
    con = sql.connect(getPathToDB())
    cur = con.cursor()
    for commit in repoInfo:
      cur.execute(
        "INSERT OR REPLACE INTO commits VALUES (?,?,?,?,?,?,?,?,?,?)",
        (
          commit['hash'],
          commit['timestamp'],
          commit['message'],
          ','.join(commit['filesAdded']),
          ','.join(commit['filesChanged']),
          ','.join(commit['filesRemoved']),
          commit['linesAdded'],
          commit['linesRemoved'],
          commit['path'],
          commit['machine']
        )
      )
    con.commit()

  except sql.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)

  finally:
    if con:
      con.close()


def pathContainsGitRepo(path):
  for root, dirs, files in os.walk(path):
    if '.git' in dirs:
      return True
    else:
      return False


if __name__ == "__main__":
  repoPath = os.getcwd()
  if not pathContainsGitRepo(repoPath):
    print "No git repository in the current working directory. Please call this script from within a git repo."
    sys.exit(0)

  repoInfo = extractRepoInfo(git.Repo(repoPath), 1)
  fillDatabase(repoInfo)

  print "Inserted commit {} into database.".format(repoInfo[0]['hash'][:10])

