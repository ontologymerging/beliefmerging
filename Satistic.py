#from wikidata.client import Client
# -*- coding: utf-8 -*-
import os
import os.path
import gzip
import json
import time
from collections import OrderedDict

from collections import deque

def PrintList(List):
	for i in List:
		print(i)

timestart = time.time()

Name1="SUMO"
Name2="WIKIDATA"
Name3="BABELNET"
CurrentLevel=7
List_Father=[]
List_Child=[]

for i in range(CurrentLevel):
	level=i+1
	SUMO = open("{0}/{0}_Taxonomy_level{1}.txt".format(Name1,level), "r")
	WIKIDATA = open("{0}/{0}_Taxonomy_level{1}.txt".format(Name2,level), "r")
	BABELNET = open("{0}/{0}_Taxonomy_level{1}.txt".format(Name3,level), "r")
	#output = open("{0}/{0}_Taxonomy_level{1}.txt".format(Name,NextLevel), "w+")
	'''
	DATASET=[]
	for i in source:
		DATASET.append(i)
	num=len(DATASET)
	print("Concept of Level",CurrentLevel,":",num)
	'''
	print("Concept of Level",level)

	SUMO_A=[]
	for i in SUMO:
		SUMO_A.append(i)
	print("SUMO",len(SUMO_A))
	SUMO.close()

	WIKIDATA_A=[]
	for i in WIKIDATA:
		WIKIDATA_A.append(i)
	print("WIKIDATA",len(WIKIDATA_A))
	WIKIDATA.close()

	BABELNET_A=[]
	for i in BABELNET:
		BABELNET_A.append(i)
	print("BABELNET",len(BABELNET_A))
	BABELNET.close()




'''
BABELNET_F = open("BABELNET/BABELNET_Father_Child.txt", "r")
for eachline in BABELNET_F:
	eachline=eachline[:-1]
	parts = eachline.split(" ");
	List_Father.append(parts[1])
	List_Child.append(parts[0])
Set_Father = set(List_Father)
Set_Child = set(List_Child)
setU = Set_Father.union(Set_Child)
print("Father:"+str(len(Set_Father)))
print("Child:"+str(len(Set_Child)))
print("Union:"+str(len(setU)))
'''

timeend = time.time()
print("Time",str(timeend-timestart))

