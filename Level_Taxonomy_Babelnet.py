
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
CurrentLevel=9
NextLevel=10
Name="BABELNET"
source = open("{0}/{0}_Father_Child.txt".format(Name), "r")
Taxonomy = open("{0}/{0}_Taxonomy_level{1}.txt".format(Name,CurrentLevel), "r")
output = open("{0}/{0}_Taxonomy_level{1}.txt".format(Name,NextLevel), "w+")

List_FatherOfChild={}
print("Running {0} Level {1} -> {2}!".format(Name,CurrentLevel,NextLevel))
for eachline in source:
	eachline=eachline[:-1]
	parts = eachline.split(" ");
	#print(parts[3])
	if parts[1] in List_FatherOfChild:
		List_FatherOfChild[parts[1]].append(parts[0])
	else:
		List_FatherOfChild[parts[1]]=[parts[0]]

	#List_Father.append(parts[1])
	#List_Child.append(parts[0])

	#count+=1
	#if count==5000:
	#	break			
	
source.close()

print("Done!, Read Dataset.")
NextFather=[]
for tx in Taxonomy:
	tx=tx[:-1]
	val = tx.split("->")
	NextFather.append(val[1])
#print(T)
NextFather = list( dict.fromkeys(NextFather))

Taxonomy.close()
#for value in NextFather:
#	print(value)
for value in NextFather:
	for F,listChild in List_FatherOfChild.items():
		if value == F:
			for child in listChild:
				#print(F,listChild)
				data= F + "->"+child
				output.write(data+"\n")
			break

output.close()
print("Done!")

#'''



