#!/usr/bin/ python
import sqlite3 as sql
import os
# import argparse

# configuration values
_pathToDB = '/Users/andre/Development/QuantifiedSelf/Commits/gitCommits.db'


def getLocalGitRepos():
  listOfRepos = []
  for root, dirs, files in os.walk(os.path.expanduser('~/')):
    if '.git' in dirs:
      listOfRepos.append(root)

    # during development we don't want to wait too long
    if len(listOfRepos) > 2:
      break
  return listOfRepos


def importLocalCommits(localGitRepos):
  dbConnection = sql.connect(_pathToDB)
  with dbConnection:
    dbCursor = dbConnection.cursor()

  for repo in listOfRepos:
    # TODO: open repo, extract data, fill DB


if __name__ == "__main__":
  localGitRepos = getLocalGitRepos()
  importLocalCommits(localGitRepos)
