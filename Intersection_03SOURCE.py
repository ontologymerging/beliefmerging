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


level=8
previouslevel=level-1
Name1="SUMO"
Level1=level
Name2="WIKIDATA"
Level2=level
Name3="BABELNET"
Level3=level
timestart = time.time()

INTERSECTION = open("INTERSECTION03SOURCE/INTERSECTION_level{1}.txt".format(Name1,level), "w+")

sourceSUMO = open("{0}/NewName/{0}_Taxonomy_level{1}_NewName.txt".format(Name1,Level1), "r")
sourceWIKIDATA = open("{0}/NewName/{0}_Taxonomy_level{1}_NewName.txt".format(Name2,Level2), "r")
sourceBABELNET = open("{0}/NewName/{0}_Taxonomy_level{1}_NewName.txt".format(Name3,Level3), "r")

print("{0}/GENERALCONCEPT/{0}_level{1}.txt".format(Name1,previouslevel))
inputSUMO = open("{0}/GENERALCONCEPT/{0}_level{1}.txt".format(Name1,previouslevel), "r")
inputWIKIDATA = open("{0}/GENERALCONCEPT/{0}_level{1}.txt".format(Name2,previouslevel), "r")
inputBABELNET = open("{0}/GENERALCONCEPT/{0}_level{1}.txt".format(Name3,previouslevel), "r")

outputSUMO = open("{0}/GENERALCONCEPT/{0}_level{1}.txt".format(Name1,Level1), "w+")
outputWIKIDATA = open("{0}/GENERALCONCEPT/{0}_level{1}.txt".format(Name2,Level2), "w+")
outputBABELNET = open("{0}/GENERALCONCEPT/{0}_level{1}.txt".format(Name3,Level3), "w+")

SUMO=[]
BABELNET=[]
WIKIDATA=[]
for each in sourceSUMO:
	p = each.strip().split("->")
	SUMO.append([p[0],p[1]])

for each in sourceWIKIDATA:
	p = each.strip().split("->")
	WIKIDATA.append([p[0],p[1]])

for each in sourceBABELNET:
	p = each.strip().split("->")
	BABELNET.append([p[0],p[1]])

#==========================================
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
setSUMO_WIKIDATABABELNET = setSUMO_WIKIDATA.intersection(set_BABELNET)

#PrintList(setSUMO_WIKIDATABABELNET)

print("SUMO:",len(A_SUMO))
print("WIKIDATA:",len(A_WIKIDATA))
print("BABELNET:",len(A_BABELNET))



print("Both:",len(setSUMO_WIKIDATA))
print("ThreeSources:",len(setSUMO_WIKIDATABABELNET))

endstart = time.time()
print("Time:",endstart - timestart)

#Save file
for each in A_SUMO:
	outputSUMO.write(each+"\n")
outputSUMO.close()
for each in A_WIKIDATA:
	outputWIKIDATA.write(each+"\n")
outputWIKIDATA.close()
for each in A_BABELNET:
	outputBABELNET.write(each+"\n")
outputBABELNET.close()

#Save file INTERSECTION
for each in setSUMO_WIKIDATABABELNET:
	INTERSECTION.write(each+"\n")
outputBABELNET.close()






