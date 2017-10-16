#!/usr/bin/env python
# -*- coding: utf-8 -*-
import github3
import unicodedata

import sys
import csv

if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8")


print "I'll request your GitHub username and password. Please don't worry, it is only to get higher API rate limit!"

g=github3.login(raw_input("uname: "),raw_input("passwd: "))

print "This will take a little time..."


contributor_info =[]	#the list which will hold the contributor attributes; real name, email, user name


#let's get the repository
def get_repo(our_organization,our_repo_name):

	global g

	org = g.organization(our_organization) 

	all_repos = org.repositories()

	the_repo = ""

	for r in all_repos:
		if r.name == our_repo_name:
			the_repo = r
			break

	return the_repo

#let's get the contributors of this repository
def get_contributors(repo):

	global contributor_info

	contributors = repo.contributors() 
	
	for con in contributors:
		u = g.user(con.login)
		contributor_info.append([u.name, u.email, u.login])	# put the real name, email and user name of the contributors

	return



def get_commit_info(the_repo):

	global committers_list

	commits = the_repo.commits()						#get commits of the repository

	for c in commits:
		if c.committer is not None:						#So that we do not get NoneType error!!
			committers_list.append(c.committer.login)	#put the user_name of the committer of each commit into committers_list

	return










