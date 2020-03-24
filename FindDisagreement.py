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


level=6
previouslevel=level-1
Name1="SUMO"
Level1=level
Name2="WIKIDATA"
Level2=level
Name3="BABELNET"
Level3=level
timestart = time.time()

inputINTERSECTION = open("INTERSECTION03SOURCE/INTERSECTION_level{0}.txt".format(level), "r")

#sourceSUMO = open("{0}/NewName/{0}_Taxonomy_level{1}_NewName.txt".format(Name1,Level1), "r")
#sourceWIKIDATA = open("{0}/NewName/{0}_Taxonomy_level{1}_NewName.txt".format(Name2,Level2), "r")
sourceBABELNET = open("{0}/NewName/{0}_Taxonomy_level{1}_NewName.txt".format(Name3,Level3), "r")

#print("{0}/GENERALCONCEPT/{0}_level{1}.txt".format(Name1,previouslevel))
#inputSUMO = open("{0}/GENERALCONCEPT/{0}_level{1}.txt".format(Name1,previouslevel), "r")
#inputWIKIDATA = open("{0}/GENERALCONCEPT/{0}_level{1}.txt".format(Name2,previouslevel), "r")
#inputBABELNET = open("{0}/GENERALCONCEPT/{0}_level{1}.txt".format(Name3,previouslevel), "r")

outputSUMO = open("LIST_INTERSECTION/{0}_level{1}.txt".format(Name1,Level1), "w+")
outputWIKIDATA = open("LIST_INTERSECTION/{0}_level{1}.txt".format(Name2,Level2), "w+")
outputBABELNET = open("LIST_INTERSECTION/{0}_level{1}.txt".format(Name3,Level3), "w+")

SUMO=[]
BABELNET=[]
WIKIDATA=[]
INTERSECTION=[]
for each in inputINTERSECTION:
	each=each[:-1]
	INTERSECTION.append(each)




#==========================================
for i in range(level):
	link="{0}/NewName/{0}_Taxonomy_level{1}_NewName.txt".format(Name1,i+1)
	#print(link)
	sourceSUMO = open(link, "r")
	for each in sourceSUMO:
		p = each.strip().split("->")
		SUMO.append([p[0],p[1]])
	sourceSUMO.close()
print("SUMO:",len(SUMO))

for i in range(level):
	link="{0}/NewName/{0}_Taxonomy_level{1}_NewName.txt".format(Name2,i+1)
	#print(link)
	sourceWIKIDATA = open(link, "r")
	for each in sourceWIKIDATA:
		p = each.strip().split("->")
		WIKIDATA.append([p[0],p[1]])
	sourceSUMO.close()
print("WIKIDATA:",len(WIKIDATA))

for i in range(level):
	link="{0}/NewName/{0}_Taxonomy_level{1}_NewName.txt".format(Name3,i+1)
	#print(link)
	sourceBABELNET = open(link, "r")
	for each in sourceBABELNET:
		p = each.strip().split("->")
		BABELNET.append([p[0],p[1]])
	sourceBABELNET.close()
print("sourceBABELNET:",len(BABELNET))




#'''
#==========================================

LIST_TAXONOMY_INTERSECTION=[]
SUMO_Remain=[]
for each in INTERSECTION:
	for eachSource in SUMO:
		if each == eachSource[0] or each == eachSource[1]:
			#print(each, eachSource)
			outputSUMO.write(eachSource[0]+"->"+eachSource[1])
			LIST_TAXONOMY_INTERSECTION.append(eachSource)
			if each == eachSource[0]:
				SUMO_Remain.append(eachSource[1])				
			if each == eachSource[1]:
				SUMO_Remain.append(eachSource[0])
print(len(LIST_TAXONOMY_INTERSECTION))
SET_SUMO_Remain = set(SUMO_Remain)

WIKIDATA_Remain=[]
for each in INTERSECTION:
	for eachSource in WIKIDATA:
		if each == eachSource[0] or each == eachSource[1]:
			#print(each, eachSource)
			LIST_TAXONOMY_INTERSECTION.append(eachSource)
			if each == eachSource[0]:
				WIKIDATA_Remain.append(eachSource[1])				
			if each == eachSource[1]:
				WIKIDATA_Remain.append(eachSource[0])
print(len(LIST_TAXONOMY_INTERSECTION))
SET_WIKIDATA_Remain = set(WIKIDATA_Remain)

BABELNET_Remain=[]
for each in INTERSECTION:
	for eachSource in BABELNET:
		if each == eachSource[0] or each == eachSource[1]:
			#print(each, eachSource)
			LIST_TAXONOMY_INTERSECTION.append(eachSource)
			if each == eachSource[0]:
				BABELNET_Remain.append(eachSource[1])				
			if each == eachSource[1]:
				BABELNET_Remain.append(eachSource[0])
print(len(LIST_TAXONOMY_INTERSECTION))
SET_BABELNET_Remain = set(BABELNET_Remain)

setSUMO_WIKIDATA = SET_SUMO_Remain.intersection(SET_WIKIDATA_Remain)
#print(setSUMO_WIKIDATA)
setSUMO_WIKIDATABABELNET = setSUMO_WIKIDATA.intersection(SET_BABELNET_Remain)

#PrintList(setSUMO_WIKIDATABABELNET)

print("SUMO:",len(SET_SUMO_Remain))
print("WIKIDATA:",len(SET_WIKIDATA_Remain))
print("BABELNET:",len(SET_BABELNET_Remain))


print("Both:",len(setSUMO_WIKIDATA))
print("ThreeSources:",len(setSUMO_WIKIDATABABELNET))
print(setSUMO_WIKIDATABABELNET)


#'''
#============================================
'''
A_SUMO=[]
for each in SUMO:
	A_SUMO.append(each[1])
A_SUMO = list(dict.fromkeys(A_SUMO))
set_SUMO = set(A_SUMO)
#------------------------------------------
A_WIKIDATA=[]
for each in WIKIDATA:
	A_WIKIDATA.append(each[1])
A_WIKIDATA = list(dict.fromkeys(A_WIKIDATA))
set_WIKIDATA = set(A_WIKIDATA)
#------------------------------------------
A_BABELNET=[]
for each in BABELNET:
	A_BABELNET.append(each[1])
A_BABELNET = list(dict.fromkeys(A_BABELNET))
set_BABELNET= set(A_BABELNET)
#------------------------------------------
#==========================================
#A_SUMO=[]
#A_WIKIDATA=[]
#A_BABELNET=[]
for each in inputSUMO:
	each=each[:-1]
	A_SUMO.append(each)
A_SUMO = list(dict.fromkeys(A_SUMO))
set_SUMO = set(A_SUMO)
#------------------------------------------
for each in inputWIKIDATA:
	each=each[:-1]
	A_WIKIDATA.append(each)
A_WIKIDATA = list(dict.fromkeys(A_WIKIDATA))
set_WIKIDATA = set(A_WIKIDATA)
#------------------------------------------
for each in inputBABELNET:
	each=each[:-1]
	A_BABELNET.append(each)
A_BABELNET = list(dict.fromkeys(A_BABELNET))
set_BABELNET= set(A_BABELNET)
#------------------------------------------


setSUMO_WIKIDATA = set_SUMO.intersection(set_WIKIDATA)
#print(setSUMO_WIKIDATA)
setSUMO_WIKIDATABABELNET = set_SUMO.intersection(set_BABELNET)

#PrintList(setSUMO_WIKIDATABABELNET)

print("SUMO:",len(A_SUMO))
print("WIKIDATA:",len(A_WIKIDATA))
print("BABELNET:",len(A_BABELNET))



print("Both:",len(setSUMO_WIKIDATA))
print("ThreeSources:",len(setSUMO_WIKIDATABABELNET))
'''
endstart = time.time()
print("Time:",endstart - timestart)







