#from wikidata.client import Client
# -*- coding: utf-8 -*-
import os
import os.path
import gzip
import json
import time
from collections import OrderedDict
import itertools
import tkinter as tk
from tkinter import messagebox
from collections import deque
from tkinter import *  

def PrintList(List):
	for i in List:
		print(i)


level=1
previouslevel=level-1
Name1="SUMO"
Level1=level
Name2="WIKIDATA"
Level2=level
Name3="BABELNET"
Level3=level
timestart = time.time()

SUMO_CONCEPT=[]
SUMO=[]
WIKIDATA=[]
BABELNET=[]
MAPPING=[]
inputSUMO_Concept = open("{0}/{0}_Concepts_Name.txt".format(Name1), "r")
inputSUMO = open("{0}/{0}_Father_Child.txt".format(Name1), "r")
inputWIKIDATA = open("{0}/{0}_Father_Child.txt".format(Name2), "r")
inputBABELNET = open("{0}/{0}_Father_Child.txt".format(Name3), "r")
#inputMapping = open("MAPPING/Data_MappingSUMO2WIKIDATA_Merging_NewName.txt", "r")
inputMapping = open("MAPPING/Data_MappingSUMO2WIKIDATA_Words.txt", "r")


stringSUMO="";
stringWIKIDATA="";
stringBABELNET="";


for each in inputSUMO_Concept:
	SUMO_CONCEPT.append(each)


for each in inputSUMO:
	p = each.strip().split("->")
	SUMO.append([p[0],p[1]])
	#stringSUMO="{0}\n{1}->{2}".format(stringSUMO,p[0],p[1])
print("SUMO:",len(SUMO))

for each in inputWIKIDATA:
	p = each.strip().split(" ")
	WIKIDATA.append([p[0],p[3]])
	#stringWIKIDATA="{0}\n{1}->{2}".format(stringWIKIDATA,p[0],p[3])
	#print(stringWIKIDATA)
print("WIKIDATA:",len(WIKIDATA))

for each in inputBABELNET:
	p = each.strip().split(" ")
	BABELNET.append([p[0],p[1]])
	#stringBABELNET="{0}{1}->{2}".format(stringBABELNET,p[0],p[1])
print("BABELNET:",len(BABELNET))


for each in inputMapping:
	p = each.strip().split(",")
	#MAPPING.append([p[0],p[1],p[2],p[3]])
	MAPPING.append([p[0],p[1],p[2]])
	#stringSUMO="{0}\n{1}->{2}".format(stringSUMO,p[0],p[1])
print("Mapping:",len(MAPPING))


#--------------------------interface---------------------
window = tk.Tk()
window.title('CRIL(Thanh): Subsumption and Equivalence')
frame = tk.Frame(window,width=500)
frame.pack()

listbox = Listbox(window, bg="snow", height=100, width=60)
listboxMapping = Listbox(window, bg="snow",height=100,  width=40)

listboxSUMO = Listbox(window, bg="snow", height=100, width=30, selectmode='multiple')
listboxWIKIDATA = Listbox(window, bg="snow",height=100,  width=50)
listboxBABELNET = Listbox(window, bg="snow",height=100,  width=60)
listboxWIKIDATA_Choose = Listbox(window, bg="snow",height=100,  width=50)
listboxBABELNET_Choose = Listbox(window, bg="snow",height=100,  width=60)

i=1
for each  in SUMO:
	listbox.insert(i, "{0}->{1}".format(each[0],each[1]))
	i=i+1


#------------------function Button-----------
def print_me():
	clicked_items = listbox.curselection()
	SelectedData = listbox.get(clicked_items)
	#print(SelectedData)
	pDataSUMO = SelectedData.strip().split("->")
	
	#--------Reset Listbox---------
	listboxMapping.delete(0,tk.END)
	listboxSUMO.delete(0,tk.END)
	listboxWIKIDATA.delete(0,tk.END)
	listboxBABELNET.delete(0,tk.END)
	#--------Mapping---------
	for each in MAPPING:
		if each[0] == pDataSUMO[0]:
			listboxMapping.insert(1,each)
		if each[0] == pDataSUMO[1]:
			listboxMapping.insert(1,each)

	#----------------SUMO--------------------

	FindSUMOMapping=[]
	for each in MAPPING:
		if each[0] == pDataSUMO[0]:
			FindSUMOMapping.append(each[0])			
		if each[0] == pDataSUMO[1]:
			FindSUMOMapping.append(each[0])
	FindSUMOMapping = list( dict.fromkeys(FindSUMOMapping))

	i=1
	ListSUMO=[]
	for each in FindSUMOMapping:
		for eachSUMO in SUMO:
			if each ==	eachSUMO[0] or each==eachSUMO[1]:
				#listboxSUMO.insert(i,"{0}->{1}".format(eachSUMO[0],eachSUMO[1]))	
				ListSUMO.append("{0}->{1}".format(eachSUMO[0],eachSUMO[1]))

	ListSUMO = list(dict.fromkeys(ListSUMO))
	for each in ListSUMO:
		listboxSUMO.insert(i,"{0}".format(each))
		i=i+1

	#-----------------WIKIDATA--------------------
	FindWikidataMapping=[]
	for each in MAPPING:
		if each[0] == pDataSUMO[0]:
			FindWikidataMapping.append(each[2])			
		if each[0] == pDataSUMO[1]:
			FindWikidataMapping.append(each[2])
	FindWikidataMapping = list( dict.fromkeys(FindWikidataMapping))

	i=1
	ListWIKIDATA=[]
	for each in FindWikidataMapping:
		for eachWIKI in WIKIDATA:
			if each ==	eachWIKI[0] or each==eachWIKI[1]:
				name1=""
				name2=""
				for eachNameMapping in MAPPING:
					if eachWIKI[0] == eachNameMapping[2]:
						name1 = eachNameMapping[0]
						break
				for eachNameMapping in MAPPING:
					if eachWIKI[1] == eachNameMapping[2]:
						name2 = eachNameMapping[0]
						break
				if 	name1 == "" or name2 =="":
					continue
				else:				
					#listboxWIKIDATA.insert(i,"{0}->{1}".format(eachWIKI[0],eachWIKI[1]))
					#listboxWIKIDATA.insert(i,"{0}->{1} ({2}->{3})".format(name1,name2,eachWIKI[0],eachWIKI[1]))				
					ListWIKIDATA.append("{0}->{1} ({2}->{3})".format(name1,name2,eachWIKI[0],eachWIKI[1]))
	
	ListWIKIDATA = list( dict.fromkeys(ListWIKIDATA))
	for each in ListWIKIDATA:
		listboxWIKIDATA.insert(i,"{0}".format(each))
		i=i+1

	#-----------------BABELNET------------------
	FindBabelnetMapping=[]
	for each in MAPPING:
		if each[0] == pDataSUMO[0]:
			FindBabelnetMapping.append(each[1])
		if each[0] == pDataSUMO[1]:
			FindBabelnetMapping.append(each[1])
	FindBabelnetMapping = list( dict.fromkeys(FindBabelnetMapping))

	i=1
	ListBABELNET=[]
	for each in FindBabelnetMapping:
		for eachBABELNET in BABELNET:
			if each == eachBABELNET[0] or each==eachBABELNET[1]:
				name1=""
				name2=""
				for eachNameMapping in MAPPING:
					if eachBABELNET[0] == eachNameMapping[1]:
						name1 = eachNameMapping[0]
						break
				for eachNameMapping in MAPPING:
					if eachBABELNET[1] == eachNameMapping[1]:
						name2 = eachNameMapping[0]
						break
				if 	name1 == "" or name2 =="":
					continue
				else:		
					#listboxBABELNET.insert(i,"{0}->{1} ({2}->{3})".format(name1,name2,eachBABELNET[0],eachBABELNET[1]))	
					#listboxBABELNET.insert(i,"{0}->{1}".format(eachBABELNET[0],eachBABELNET[1]))	
					ListBABELNET.append("{0}->{1} ({2}->{3})".format(name1,name2,eachBABELNET[0],eachBABELNET[1]))	
					#i=i+1

	ListBABELNET = list( dict.fromkeys(ListBABELNET))
	for each in ListBABELNET:
		listboxBABELNET.insert(i,"{0}".format(each))
		i=i+1
	#------------------------------------------
	if listboxBABELNET.size() == 0 or listboxWIKIDATA.size() == 0:
		messagebox.showinfo("Information", "Dataset is not full enough!")


#------------------function Button-----------
def Searching():
	#--------Reset Listbox---------
	listboxWIKIDATA_Choose.delete(0,tk.END)
	listboxWIKIDATA_Choose.delete(0,tk.END)
	#-------------Choose from Listbox------------
	i=1
	selection = listboxSUMO.curselection()	
	chooseList=[]
	for each in selection:
		dataList = listboxSUMO.get(each)
		p = dataList.strip().split("->")	
		chooseList.append(p[0])
		chooseList.append(p[1])
		chooseList = list( dict.fromkeys(chooseList))


	messagebox.showinfo("Information","{0}".format(chooseList))
	#-----------------WIKIDATA--------------------
	FindWikidataMapping=[]
	for each in MAPPING:
		for eachChooseList in chooseList:
			if each[0] == eachChooseList:
				FindWikidataMapping.append(each[2])			

	FindWikidataMapping = list( dict.fromkeys(FindWikidataMapping))
	
	i=1
	ListWIKIDATA1=[]
	for each in FindWikidataMapping:
		for eachWIKI in WIKIDATA:
			if each ==	eachWIKI[0] or each==eachWIKI[1]:
				name1=""
				name2=""
				for eachNameMapping in MAPPING:
					if eachWIKI[0] == eachNameMapping[2]:
						name1 = eachNameMapping[0]
						break
				for eachNameMapping in MAPPING:
					if eachWIKI[1] == eachNameMapping[2]:
						name2 = eachNameMapping[0]
						break
				if 	name1 == "" or name2 =="":
					continue
				else:				
					#listboxWIKIDATA.insert(i,"{0}->{1}".format(eachWIKI[0],eachWIKI[1]))
					#listboxWIKIDATA.insert(i,"{0}->{1} ({2}->{3})".format(name1,name2,eachWIKI[0],eachWIKI[1]))				
					ListWIKIDATA1.append("{0}->{1} ({2}->{3})".format(name1,name2,eachWIKI[0],eachWIKI[1]))
	
	ListWIKIDATA1 = list( dict.fromkeys(ListWIKIDATA1))
	for each in ListWIKIDATA1:
		listboxWIKIDATA_Choose.insert(i,"{0}".format(each))
		i=i+1
	
	#-----------------WIKIDATA--------------------
	FindBabelnetMapping=[]
	for each in MAPPING:
		for eachChooseList in chooseList:
			if each[0] == eachChooseList:
				FindBabelnetMapping.append(each[1])			

	FindBabelnetMapping = list( dict.fromkeys(FindBabelnetMapping))
	
	i=1
	ListBABELNET1=[]
	for each in FindBabelnetMapping:
		for eachBABELNET in BABELNET:
			if each ==	eachBABELNET[0] or each==eachBABELNET[1]:
				name1=""
				name2=""
				for eachNameMapping in MAPPING:
					if eachBABELNET[0] == eachNameMapping[1]:
						name1 = eachNameMapping[0]
						break
				for eachNameMapping in MAPPING:
					if eachBABELNET[1] == eachNameMapping[1]:
						name2 = eachNameMapping[0]
						break
				if 	name1 == "" or name2 =="":
					continue
				else:				
					#listboxWIKIDATA.insert(i,"{0}->{1}".format(eachWIKI[0],eachWIKI[1]))
					#listboxWIKIDATA.insert(i,"{0}->{1} ({2}->{3})".format(name1,name2,eachWIKI[0],eachWIKI[1]))				
					ListBABELNET1.append("{0}->{1} ({2}->{3})".format(name1,name2,eachBABELNET[0],eachBABELNET[1]))
	
	ListBABELNET1 = list( dict.fromkeys(ListBABELNET1))
	for each in ListBABELNET1:
		listboxBABELNET_Choose.insert(i,"{0}".format(each))
		i=i+1
	




#----------------------Button-------------------
btn = Button(window, text="print",command=print_me)
btn.pack()
btn1 = Button(window, text="Search",command=Searching)
btn1.pack()


listbox.pack(side=tk.LEFT)
listboxMapping.pack(side=tk.LEFT)
listboxSUMO.pack(side=tk.LEFT)
listboxWIKIDATA.pack(side=tk.LEFT)
listboxBABELNET.pack(side=tk.LEFT)

listboxWIKIDATA_Choose.pack(side=tk.LEFT)
listboxBABELNET_Choose.pack(side=tk.LEFT)

window.resizable(tk.TRUE,tk.TRUE)
window.mainloop()














'''
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

'''
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







