#!/usr/bin/env python
from socket import gethostname
import sqlite3 as sql
import os, sys
import git
import subprocess


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

    # get information about the chagned files in this commit
    hash = commit.name_rev.split(' ')[0]
    path = repo.git_dir[:-4]
    p = subprocess.Popen(['git', '--git-dir='+repo.git_dir, '--work-tree='+path, 'show', '--name-status', '--oneline', hash], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    # output is one long string, split it into lists
    filesAdded = []
    filesRemoved = []
    filesChanged = []
    for line in out.splitlines()[1:]:
      fileStat = line.split('\t')
      if len(fileStat) != 2:
        continue
      if fileStat[0] == 'A':
        filesAdded.append(fileStat[1])
      elif fileStat[0] == 'D':
        filesRemoved.append(fileStat[1])
      elif fileStat[0] in ['C', 'R']:
        filesChanged.append(fileStat[1])

    # fill the list
    commitInfo.append({
      'hash': hash,
      'message': commit.message.encode('utf8').strip(),
      'timestamp': commit.authored_date,
      'path': path,
      'filesAdded': filesAdded,
      'filesChanged': filesChanged,
      'filesRemoved': filesRemoved,
      'linesAdded': commit.stats.total['insertions'],
      'linesRemoved': commit.stats.total['deletions'],
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

