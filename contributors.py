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


#holder lists

contributor_info =[]	#the list which will hold the contributor attributes; real name, email, user name

committers_list =[]		#the list which will hold the committers' only user_names

com_with_nums=[]	#the list which will first hold the committers along with their number of commits; later on the other attributes will be added to this list


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


#get actual committers rather than contributors
def get_commit_info(the_repo):

	global committers_list

	commits = the_repo.commits()						#get commits of the repository

	for c in commits:
		if c.committer is not None:						#So that we do not get NoneType error!!
			committers_list.append(c.committer.login)	#put the user_name of the committer of each commit into committers_list

	return



def committer_and_number():

	#finding the total numbers of commits, each committer did

	#making sure that there are no duplicates
	
	global committers_list
	global com_with_nums

	i=0
	j=0
	flag =0;
	for c in committers_list:
		if j==0:
			com_with_nums.append([c,1])
			j= j+1
			continue
		while i <len(com_with_nums):
			if com_with_nums[i][0] == c:
				com_with_nums[i][1] +=1
				flag+=1
			i=i+1
		if flag ==0:
			com_with_nums.append([c,1])	
		flag=0	
		i=0

	return


def unite():					

	global com_with_nums
	global contributor_info

	#put the related user data into committer with numbers list
	for y in com_with_nums:
		for z in contributor_info:
			if y[0] == z[2]:		#if it is same user_name
				y.append(z[0])		#add the real name of the committer
				y.append(z[1])		#add the email of the committer

	#now the order of info inside the com_with_nums is user_name, num_of_commits, real_name, email


	#let's sort the committers by their total number of commits in descending order, for the sake of simplicity

	com_with_nums.sort(key=lambda k: -k[1])	

	return



def csv_format_output():

	#it's time to create the csv formatted output file with the desired info
	global com_with_nums

	#we want to deliver full name, email, username, total number of commits, respectively

	print "Press 1 if you want to receive the information related to the committers who haven't submitted their real names, otherwise press any other number."
	input = int(raw_input())
	if input == 1:
	
		with open('output_notRealNames_included.csv','w') as csvfile:
			csv_writer =csv.writer(csvfile,delimiter=',')
			csv_writer.writerow(["Full Name","Email","Username", "Total Number of Commits"])
			for x in com_with_nums:
				if len(x) > 2:
					if x[3] is not None and x[3].find('@') is not -1:
						csv_writer.writerow([x[2] , x[3], x[0], x[1]])	
					else:
						csv_writer.writerow([x[2] , "UNKNOWN", x[0], x[1]])	
				
				else:
					csv_writer.writerow(["", "UNKNOWN", x[0], x[1]])		#taking care of index errors
		
		#checking len(x)>2 in case if there's a committer, which is not in contributors of the project, so we cannot reach its real name and email unfortunately

	else:
		with open('output_with_only_RealNames.csv','w') as csvfile:
			csv_writer =csv.writer(csvfile,delimiter=',')
			csv_writer.writerow(["Full Name","Email","Username", "Total Number of Commits"])
			for x in com_with_nums:
				if len(x) > 2:
					if len(x[2]) is not 0 and x[2][0].isalpha():			#check if it is a real name->check if anything submitted and check the first letter of the name
						if x[3] is not None and x[3].find('@') is not -1:
							csv_writer.writerow([x[2] , x[3], x[0], x[1]])	
						else:
							csv_writer.writerow([x[2] , "UNKNOWN", x[0], x[1]])	
						


	return

