#!/usr/bin/env python
# -*- coding: utf-8 -*-
import github3
import unicodedata

import sys
import csv

if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8")


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














