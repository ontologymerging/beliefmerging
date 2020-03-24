
#from wikidata.client import Client
# -*- coding: utf-8 -*-
import os
import os.path
import gzip
import json
import time
from collections import OrderedDict

#import rdflib

from collections import deque


print("Loading dataset.")
startTime = time.time()
output = open("BABELNET/BABELNET_Taxonomy_level1.txt", "w+")
file = open("BABELNET/Babelnet_Father_Child.txt", "r")
List_Father=[]
Father_Child=[]
List_Child=[]
count=0
List_FatherOfChild={}
#'''
for eachline in file:
	eachline=eachline[:-1]
	parts = eachline.split(" ");
	#print(parts)
	if parts[1] in List_FatherOfChild:
		List_FatherOfChild[parts[1]].append(parts[0])
	else:
		List_FatherOfChild[parts[1]]=[parts[0]]

	List_Father.append(parts[1])
	List_Child.append(parts[0])

	#count+=1
	#if count==5000:
	#	break			
	
file.close()

endTime = time.time()
print(endTime-startTime)

print(len(List_FatherOfChild),"/",len(List_Father))
#'''
# Creating an empty dictionary 
List_Father = list( dict.fromkeys(List_Father))
List_Child = list( dict.fromkeys(List_Child))
print(len(List_Father))
#print(len(List_Child))
Set_Father = set(List_Father)
Set_Child = set(List_Child)
#Has a child
Most_Father = Set_Father.difference(Set_Child)
#Have relationships

List_Most_Father = list(Most_Father)
print(len(List_Most_Father))
print(List_Most_Father)
c=0
print("COUNT:",count)
count=0
#'''

for F in List_Most_Father:
	output.write("Top->"+F+"\n")

output.close()
print("Done!")

#'''



