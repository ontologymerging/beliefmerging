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
import itertools

def PrintList(List):
	for i in List:
		print(i)

def GenerateConcepts(InputAtomicConcepts, SubsumptionRole):
    AtomicConcepts = itertools.combinations(InputAtomicConcepts, 2)
    ListOfConcepts = []
    for concept in AtomicConcepts:
        for predicate in SubsumptionRole:
            EachConcepts = concept[0], predicate, concept[1]
            ListOfConcepts.append(EachConcepts)
    return ListOfConcepts

def GetFather(Concept):
    Left=Concept[0]
    Relation = Concept[1]
    Right = Concept[2]

    if Relation=="->":
        return Right
    if Relation=="<-":
        return Left
    return Left

def GetChild(Concept):
    Left=Concept[0]
    Relation = Concept[1]
    Right = Concept[2]

    if Relation=="->":
        return Left
    if Relation=="<-":
        return Right
    return Left

def LeftSide(Concept):
    return Concept[0]

def RelationOfConcepts(Concept):
    return Concept[1]

def RightSide(Concept):
    return Concept[2]

def Initiation_ListElement(i):
    InterpretationCaseOfConcept = [
        [['a'], ['b'], ['c']],
    ]
    return InterpretationCaseOfConcept[i]

def Initiation():
    A = ['a']
    B = ['b']
    C = ['c']
    Array_Interpretation = []
    Array_Interpretation.append(A)
    Array_Interpretation.append(B)
    Array_Interpretation.append(C)
    return Array_Interpretation

def PositionOfString(letterToFind,conceptstring):
    count=0
    for i in conceptstring:
        count=count+1
        if(letterToFind == i):
            return count
    return 0

def Combinations(ListOfConcepts):
    return itertools.combinations(ListOfConcepts,2)

def closure(relation, left, right, primaryConcept,listOfInterpretation):
    result=[]
    result = listOfInterpretation
    LeftInterpretation=[]
    RightInterpretation=[]
    positionRight = PositionOfString(right, primaryConcept) - 1
    positionLeft = PositionOfString(left, primaryConcept) - 1

    if relation=="->":
        LeftInterpretation.extend(listOfInterpretation[positionLeft])
        RightInterpretation.extend(listOfInterpretation[positionLeft])

    if relation=="<-":
        LeftInterpretation.extend(listOfInterpretation[positionRight])
        RightInterpretation.extend(listOfInterpretation[positionRight])

    if relation=="=":
        LeftInterpretation.extend(listOfInterpretation[positionRight])
        RightInterpretation.extend(listOfInterpretation[positionRight])
        LeftInterpretation.extend(listOfInterpretation[positionLeft])
        RightInterpretation.extend(listOfInterpretation[positionLeft])

    result[positionLeft].extend(LeftInterpretation)
    result[positionRight].extend(RightInterpretation)
    return result;

def Abbreviation(Concept,primaryConcept):
    for i in range(0,len(primaryConcept)):
        Concept[i]=list(dict.fromkeys(Concept[i]))
        #Sorting asc
        Concept[i].sort()
    return Concept

def Aggeration_Axioms(Axiom_Left, Axiom_Right,primaryConcept):
    for i in range(0,len(primaryConcept)):
        Axiom_Left[i].extend(Axiom_Right[i])
        #Remove concepts duplication
        Axiom_Left[i]=list(dict.fromkeys(Axiom_Left[i]))
    return Axiom_Left

def TransitionBetweenConcepts(ListConcept):
    Concept1=ListConcept[0]
    Concept2 = ListConcept[1]
    if GetChild(Concept1) == GetFather(Concept2) or GetFather(Concept1)== GetChild(Concept2):
        return True
    if RelationOfConcepts(Concept1)=="=" or RelationOfConcepts(Concept2)=="=":
        return True
    return False

def FindFather_AtMost(LeftConcept, RightConcept):
    if RelationOfConcepts(LeftConcept) == "=" and RelationOfConcepts(RightConcept) == "=":
        return GetFather(RightConcept)
    if RelationOfConcepts(LeftConcept) == "=":
        return GetFather(RightConcept)
    if RelationOfConcepts(RightConcept) == "=":
        return GetFather(LeftConcept)
    if  GetChild(LeftConcept)==GetFather(RightConcept):
        return GetFather(LeftConcept)
    if GetFather(LeftConcept) == GetChild(RightConcept):
        return GetFather(RightConcept)

def FindChild_AtLeast(LeftConcept, RightConcept):
    if RelationOfConcepts(LeftConcept) == "=" and RelationOfConcepts(RightConcept) == "=":
        return RightSide(RightConcept)
    if RelationOfConcepts(LeftConcept) == "=" :
        return GetChild(RightConcept)
    if RelationOfConcepts(RightConcept) == "=":
        return GetChild(LeftConcept)
    if  GetFather(LeftConcept)==GetChild(RightConcept):
        return GetChild(LeftConcept)
    if GetChild(LeftConcept) == GetFather(RightConcept):
        return GetChild(RightConcept)

def FindMax_ElementRanking(Concept1, Concept2, Interpretations,primaryConcept):

    if RelationOfConcepts(Concept1)=="=":
        positionRight = PositionOfString(RightSide(Concept1), primaryConcept) - 1
        positionLeft = PositionOfString(LeftSide(Concept1), primaryConcept) - 1
        if(len(Interpretations[positionLeft])>=len(Interpretations[positionRight])):
            return LeftSide(Concept1), RightSide(Concept1)
        else:
            return RightSide(Concept1), LeftSide(Concept1)
    else:
        if RelationOfConcepts(Concept2)=="=":
            positionRight = PositionOfString(RightSide(Concept2), primaryConcept) - 1
            positionLeft = PositionOfString(LeftSide(Concept2), primaryConcept) - 1
            if (len(Interpretations[positionLeft]) >= len(Interpretations[positionRight])):
                return LeftSide(Concept2),  RightSide(Concept2)
            else:
                return RightSide(Concept2),LeftSide(Concept2)

def StrutureOfConcept(GenerateAxiom):
    ConceptsStructure = []
    for atomicConcepts in GenerateAxiom:
        Concept1 = atomicConcepts[0]
        Concept2 = atomicConcepts[1]
        if (LeftSide(Concept1) == LeftSide(Concept2) and RightSide(Concept1) == RightSide(Concept2)):
            continue
        else:
            pass
        if (RelationOfConcepts(Concept1) == RelationOfConcepts(Concept2)) and (
                RelationOfConcepts(Concept1) == "=") and (RightSide(Concept1) != RightSide(Concept2)):
            continue
        else:
            ConceptsStructure.append(atomicConcepts)
    return ConceptsStructure


def FindInterpretation_Subsumption(ConceptsStructure,InputAtomicConcepts):
    Array_All_Interpretation=[]

    Array_Init_Interpretation1=[]
    Array_Init_Interpretation2=[]
    for eachConcept in ConceptsStructure:
        Concept1 = eachConcept[0]
        Concept2 = eachConcept[1]

        for i in range(1):
            Array_Init_Interpretation1 = Initiation_ListElement(i)
            Array_Init_Interpretation2 = Initiation_ListElement(i)

            Interpretation1_Left = closure(RelationOfConcepts(Concept1), LeftSide(Concept1), RightSide(Concept1),
                                           InputAtomicConcepts, Array_Init_Interpretation1)
            Interpretation2_Right = closure(RelationOfConcepts(Concept2), LeftSide(Concept2), RightSide(Concept2),
                                            InputAtomicConcepts, Array_Init_Interpretation2)
            InterpretationsOfConcepts = Aggeration_Axioms(Interpretation1_Left, Interpretation2_Right, InputAtomicConcepts)

            Result_Interpretation = []
            if TransitionBetweenConcepts(eachConcept):
                Result_Interpretation = closure("->", FindChild_AtLeast(Concept1, Concept2),
                                                FindFather_AtMost(Concept1, Concept2),
                                                InputAtomicConcepts, InterpretationsOfConcepts)
            else:
                Result_Interpretation = InterpretationsOfConcepts
            FinalResultInterpretation = Abbreviation(Result_Interpretation, InputAtomicConcepts)

            if RelationOfConcepts(Concept1) == "=" or RelationOfConcepts(Concept2) == "=":
                MaxRanking = FindMax_ElementRanking(Concept1, Concept2, FinalResultInterpretation, InputAtomicConcepts)
                MaxRankingInterpretation = closure("->", MaxRanking[0], MaxRanking[1], InputAtomicConcepts,
                                                   FinalResultInterpretation)
                FinalResultInterpretation = Abbreviation(MaxRankingInterpretation, InputAtomicConcepts)

            Array_All_Interpretation.append(FinalResultInterpretation)


    return Array_All_Interpretation



def CheckCorrectionOfInterpretation_EachConcept(Concept1, Interpretations,primaryConcept):

    resultChecking_Concept1 = False
    # -----------------------Concept 1--------------------------------
    positionRight_1 = PositionOfString(RightSide(Concept1), primaryConcept) - 1
    positionLeft_1 = PositionOfString(LeftSide(Concept1), primaryConcept) - 1
    LeftSet = set(Interpretations[positionLeft_1])
    RightSet = set(Interpretations[positionRight_1])
    if RelationOfConcepts(Concept1) == "->":
        if LeftSet.issubset(RightSet):
            resultChecking_Concept1 = True
    if RelationOfConcepts(Concept1) == "<-":
        if RightSet.issubset(LeftSet):
            resultChecking_Concept1 = True
    if RelationOfConcepts(Concept1) == "=":
        if all([Interpretations[positionLeft_1][i] in Interpretations[positionRight_1] for i in range(len(Interpretations[positionLeft_1]))]) == True \
                and len(Interpretations[positionLeft_1]) == len(Interpretations[positionRight_1]):
            resultChecking_Concept1 = True

    return resultChecking_Concept1



def Statistics_Interpretation(ConceptsStructure, Array_All_Interpretation,InputAtomicConcepts):
	#number=[1,1,4]
	#doi ten
	#Dung dinh dang
	number=[1,2,3]
	id=0
	Sum_ThreeOntology=[]
	Sum_Interpretation=[]
	for i in ConceptsStructure:
		id=id+1
		for h in range(len(number)):
			tang=0
			if (id == number[h]):
				print("->", i)
				for j in Array_All_Interpretation:
					tang = tang + 1
					countTrue = 0
					countFalse = 0
					if(CheckCorrectionOfInterpretation_EachConcept(i[0],j,InputAtomicConcepts)):
						countTrue=countTrue+1
					else:
						countFalse = countFalse +1
					if(CheckCorrectionOfInterpretation_EachConcept(i[1],j,InputAtomicConcepts)):
						countTrue=countTrue+1
					else:
						countFalse = countFalse +1

					#print("%s. %s -- %s"%(tang,countTrue, countFalse))
					Sum_Interpretation.append(countFalse)

				Sum_ThreeOntology.append(Sum_Interpretation)
				Sum_Interpretation=[]

	List_Sum_ThreeOntologies=[]
	for i in range(len(Sum_ThreeOntology[0])):
		SumAll = Sum_ThreeOntology[0][i]+ Sum_ThreeOntology[1][i]+ Sum_ThreeOntology[2][i]
		List_Sum_ThreeOntologies.append(SumAll)
	Sum_ThreeOntology.append(List_Sum_ThreeOntologies)
	Sum_ThreeOntology.append(Array_All_Interpretation)

	#Vertical to horizontal in array
	Rotate_Array = [[Sum_ThreeOntology[j][i] for j in range(len(Sum_ThreeOntology))] for i in range(len(Sum_ThreeOntology[0]))]
	Rotate_Array.sort(key=lambda Rotate_Array: Rotate_Array[3])#,reverse=True)
	#Number_Sorted_Array=[]
	#Number_Sorted_Array.sort()
	return Rotate_Array


def GetTopModel(ArrayResult):
	ListInterpretation=[]
	for each in ArrayResult:
		Result = each[3]
		Interpretation = each[4]
		if Result==0:
			ListInterpretation.append(Interpretation)
	return ListInterpretation

def Frequency(List):
	l = List
	l = list( dict.fromkeys(l))
	ListFrequency={}
	for each in l:
		ListFrequency[each] = []
		ListFrequency[each].append(List.count(each))
	return ListFrequency

def SIFAlgorithm(ArrayResult, Concept):
	SIFT={}
	ListInterpretation={}
	i=0
	for C in Concept:
		ListInterpretation[C]=[]
		for each in ArrayResult:
			ListInterpretation[C].extend(each[i])
		i=i+1
	#print(ListInterpretation)
	for nameConcept, valueList in ListInterpretation.items():
		SIFT[nameConcept]=[]
		fre = Frequency(valueList)
		t = len(ArrayResult)/2
		#print("Concept:{0}".format(C))
		#print("Interpretation:{0}".format(fre))
		for i,v in fre.items():
			#print("{0}>{1},{2}={3}".format(v[0],t, v[0], len(ArrayResult)))
			if v[0]>t and v[0]==len(ArrayResult):
				SIFT[nameConcept].append(i)
	print(SIFT)		
	return SIFT

def WriteText_Dist(lst_dict):
	listdict=""
	for each,val in lst_dict.items():
		listdict="{0}{1}:{2}\n\n".format(listdict,each, val)
	return listdict

def WriteText_List(lst_dict):
	listdict=""
	for each in lst_dict:
		listdict="{0}{1}\n\n".format(listdict,each)
	return listdict
#------------------------------------------------------------

level=1
previouslevel=level-1
Name1="SUMO"
Level1=level
Name2="WIKIDATA"
Level2=level
Name3="BABELNET"
Level3=level
timestart = time.time()


SUMO_Merging=[]
WIKIDATA_Merging=[]
BABELNET_Merging=[]

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
MAPPING_SUMO=[]
MAPPING_WIKIDATA=[]
MAPPING_BABELNET=[]

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
	MAPPING_WIKIDATA.append(p[2])
	MAPPING_BABELNET.append(p[1])
	#stringSUMO="{0}\n{1}->{2}".format(stringSUMO,p[0],p[1])
print("Mapping:",len(MAPPING))


#--------------------------interface---------------------
window = tk.Tk()
window.title('CRIL(Thanh): Subsumption and Equivalence')
frame = tk.Frame(window,width=500)
frame.pack()

listbox = Listbox(window, bg="snow", height=100, width=55, selectmode='multiple')
listboxMapping = Listbox(window, bg="snow",height=100,  width=35)

listboxSUMO = Listbox(window, bg="snow", height=100, width=30, selectmode='multiple')
listboxWIKIDATA = Listbox(window, bg="snow",height=100,  width=45, selectmode='multiple')
listboxBABELNET = Listbox(window, bg="snow",height=100,  width=55, selectmode='multiple')

MergingChoose = Listbox(window, bg="snow",height=25,  width=100)
listboxWIKIDATA_Choose = Listbox(window, bg="snow",height=75,  width=45)
listboxBABELNET_Choose = Listbox(window, bg="snow",height=75,  width=55)

i=1
for each  in SUMO:
	listbox.insert(i, "{0}->{1}".format(each[0],each[1]))
	i=i+1


#------------------function Button-----------
def print_me():
	selection = listbox.curselection()

	#SelectedData = listbox.get(clicked_items)
	#print(SelectedData)
	chooseList=[]
	for each in selection:
		dataList = listbox.get(each)
		p = dataList.strip().split("->")	
		chooseList.append(p[0])
		chooseList.append(p[1])
		chooseList = list( dict.fromkeys(chooseList))
	
	#pDataSUMO = SelectedData.strip().split("->")
	
	#--------Reset Listbox---------
	listboxMapping.delete(0,tk.END)
	listboxSUMO.delete(0,tk.END)
	listboxWIKIDATA.delete(0,tk.END)
	listboxBABELNET.delete(0,tk.END)
	#----------------SUMO--------------------
	FindSUMOMapping=[]
	i=0
	for each in MAPPING:
		for eachChooseList in chooseList:
			if each[0] == eachChooseList:
				FindSUMOMapping.append(each[0])
				listboxMapping.insert(i,each)
				i+=1			

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


#------------------function Button-----------
def Searching():
	#--------Reset Listbox---------
	listboxWIKIDATA_Choose.delete(0,tk.END)
	listboxBABELNET_Choose.delete(0,tk.END)
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
					ListWIKIDATA1.append("{0}->{1} ({2}->{3})".format(name1,name2,eachWIKI[0],eachWIKI[1]))
	
	ListWIKIDATA1 = list( dict.fromkeys(ListWIKIDATA1))
	for each in ListWIKIDATA1:
		listboxWIKIDATA_Choose.insert(i,"{0}".format(each))
		i=i+1
	
	#-----------------BABELNET--------------------
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
					ListBABELNET1.append("{0}->{1} ({2}->{3})".format(name1,name2,eachBABELNET[0],eachBABELNET[1]))
	
	ListBABELNET1 = list( dict.fromkeys(ListBABELNET1))
	for each in ListBABELNET1:
		listboxBABELNET_Choose.insert(i,"{0}".format(each))
		i=i+1
	
def GetSameConcept():
	#--------Reset Listbox---------
	listboxWIKIDATA.delete(0,tk.END)
	listboxBABELNET.delete(0,tk.END)
	#-------------Choose from Listbox------------
	selection = listboxSUMO.curselection()	
	chooseList=[]
	for each in selection:
		dataList = listboxSUMO.get(each)
		p = dataList.strip().split("->")	
		chooseList.append(p[0])
		chooseList.append(p[1])
		chooseList = list( dict.fromkeys(chooseList))

	messagebox.showinfo("Information","{0}".format(chooseList))



	#--------------choose same concepts-------------
	#--------------MAPPING--------------------
	FindWikidataMapping=[]
	FindBabelnetMapping=[]
	timestart = time.time()
	for each in MAPPING:
		for eachChooseList in chooseList:
			if each[0] == eachChooseList:
				FindWikidataMapping.append(each[2])
				FindBabelnetMapping.append(each[1])					

	FindWikidataMapping = list( dict.fromkeys(FindWikidataMapping))
	FindBabelnetMapping = list( dict.fromkeys(FindBabelnetMapping))
	endstart = time.time()
	print("Time 1:",endstart - timestart)

	timestart = time.time()
	i=1
	ListWIKIDATA1=[]
	for each in FindWikidataMapping:
		for eachWIKI in WIKIDATA:
			if each ==	eachWIKI[0] or each == eachWIKI[1]:
				if eachWIKI[0] in set(MAPPING_WIKIDATA) and eachWIKI[1] in set(MAPPING_WIKIDATA):
					ListWIKIDATA1.append(eachWIKI)

	List_WIKIDATA=[]
	for each in ListWIKIDATA1:
		name1=""
		name2=""
		Array_Name1=[]
		Array_Name2=[]

		for eachNameMapping in MAPPING:
			if each[0] == eachNameMapping[2]:
				name1 = eachNameMapping[0]
				Array_Name1.append(name1)
			if each[1] == eachNameMapping[2]:
				name2 = eachNameMapping[0]
				Array_Name2.append(name2)

		for eachName1 in Array_Name1:
			for eachName2 in Array_Name2:
				if 	eachName1 in set(chooseList) and eachName2 in set(chooseList) and eachName1 != eachName2:
					List_WIKIDATA.append("{0}->{1} ({2}->{3})".format(eachName1,eachName2,each[0],each[1]))
	
	List_WIKIDATA = list( dict.fromkeys(List_WIKIDATA))
	for each in List_WIKIDATA:
		listboxWIKIDATA.insert(i,"{0}".format(each))
		i=i+1

	endstart = time.time()
	print("Time 2:",endstart - timestart)
	#-----------------------------------------------
	#-----------------BABELNET--------------------
	timestart = time.time()
	i=1
	Temp_BABELNET=[]
	ListBABELNET1=[]
	for each in FindBabelnetMapping:
		for eachBABELNET in BABELNET:
			if each ==	eachBABELNET[0] or each==eachBABELNET[1]:
				Temp_BABELNET.append(eachBABELNET)
	
	for each in Temp_BABELNET:
		if each[0] in set(MAPPING_BABELNET) and each[1] in set(MAPPING_BABELNET):
			ListBABELNET1.append(each)

	endstart = time.time()
	print("Time 3:",endstart - timestart)
	print("Lenght:",len(ListBABELNET1))
	
	#if eachBABELNET[0] in set(MAPPING_WIKIDATA) and 
	timestart = time.time()
	List_BABELNET=[]
	for each in ListBABELNET1:
		name1=""
		name2=""
		Array_Name1=[]
		Array_Name2=[]
		for eachNameMapping in MAPPING:
			if each[0] == eachNameMapping[1]:
				name1 = eachNameMapping[0]
				Array_Name1.append(name1)
			if each[1] == eachNameMapping[1]:
				name2 = eachNameMapping[0]
				Array_Name2.append(name2)
				#break
		endstart = time.time()
		#print(name1,"-",name2)
		#print("Time step:",endstart - timestart)	
		for eachName1 in Array_Name1:
			for eachName2 in Array_Name2:
				if 	eachName1 in set(chooseList) and eachName2 in set(chooseList) and eachName1 != eachName2:				
					List_BABELNET.append("{0}->{1} ({2}->{3})".format(eachName1,eachName2,each[0],each[1]))
		endstart = time.time()
		#print("Time running:",endstart - timestart)

	endstart = time.time()
	print("Time 4:",endstart - timestart)	
	
	List_BABELNET = list( dict.fromkeys(List_BABELNET))
	for each in List_BABELNET:
		listboxBABELNET.insert(i,"{0}".format(each))
		i=i+1


def OntologyMerging():


	#--------Reset Listbox---------
	listboxWIKIDATA_Choose.delete(0,tk.END)
	listboxBABELNET_Choose.delete(0,tk.END)
	#-------------Choose from Listbox------------
	#messagebox.showinfo("Information SUMO","{0}\n{1}\n{2}".format(SUMO_Merging,WIKIDATA_Merging,BABELNET_Merging))
	
	ListOfConcepts=GenerateConcepts(InputAtomicConcepts,Relations)
	GenerateAxiom = Combinations(ListOfConcepts)
	ConceptsStructure = StrutureOfConcept(GenerateAxiom)
	Array_All_Interpretation = FindInterpretation_Subsumption(ConceptsStructure,InputAtomicConcepts)	

	
	ListConceptSelection = []
	predicate="->"
	List_Simple_Concept=[]
	List_Temp=[]
	for each in SUMO_Merging:
		p1 = each.strip().split ("->")
		List_Simple_Concept.append(p1)
		EachConcepts = p1[0], predicate, p1[1]
		List_Temp.append(EachConcepts)
	ListConceptSelection.append(List_Temp)

	List_Temp=[]
	for each in WIKIDATA_Merging:
		p1 = each.strip().split ("->")
		List_Simple_Concept.append(p1)
		EachConcepts = p1[0], predicate, p1[1]
		List_Temp.append(EachConcepts)
	ListConceptSelection.append(List_Temp)

	List_Temp=[]
	for each in BABELNET_Merging:
		p1 = each.strip().split ("->")
		List_Simple_Concept.append(p1)
		EachConcepts = p1[0], predicate, p1[1]
		List_Temp.append(EachConcepts)
	ListConceptSelection.append(List_Temp)

	InputAtomicConcepts1=[]
	for value in List_Simple_Concept:
		for each in value:
			InputAtomicConcepts1.append(each)			
	InputAtomicConcepts1 = list( dict.fromkeys(InputAtomicConcepts1))
	
	if listboxWIKIDATA.size()==0 or listboxBABELNET==0:
		messagebox.showinfo("Information","Currently, The axioms of three sources need to be full. Please check three sources: Wikidata, Babelnet, SUMO!")		
		return 1

	if len(InputAtomicConcepts1)>3:
		messagebox.showinfo("Information","The number of Concepts must be at most 3.\n{0}\n. Please check the concepts".format(InputAtomicConcepts1))
	else:
		messagebox.showinfo("Information","The concepts consider:{0}".format(InputAtomicConcepts1))	
		Result = Statistics_Interpretation(ListConceptSelection, Array_All_Interpretation,InputAtomicConcepts1)
		ResultTop = GetTopModel(Result)

		resultSIF = SIFAlgorithm(ResultTop,InputAtomicConcepts1)

		PrintListBox(ResultTop,listboxWIKIDATA_Choose)
		PrintListBox_Dist(resultSIF,listboxBABELNET_Choose)

		ListResultMerging=[]
		SyntacticResult_OntologyMerging=[]
		for each, value in resultSIF.items():
			ListResultMerging.append(value)

		index=0
		for each in Array_All_Interpretation:
			if each == ListResultMerging:
				SyntacticResult_OntologyMerging.append(ConceptsStructure[index])
			index = index+1

		FinalResultMerging=[]
		string_each=""
		for each in SyntacticResult_OntologyMerging:
			string_each = '{0}'.format(each)
			for i in range(3):
				string_each = string_each.replace("'{0}'".format(InputAtomicConcepts[i]),"'{0}'".format(InputAtomicConcepts1[i]))
			FinalResultMerging.append(string_each)
		
		List_String=""
		for i in range(3):
				List_String = "{0}   {1}:{2}".format(List_String,InputAtomicConcepts[i],InputAtomicConcepts1[i])
		
		MergingChoose.delete(8)
		MergingChoose.delete(7)
		MergingChoose.delete(6)
		MergingChoose.delete(5)
		MergingChoose.delete(4)
		MergingChoose.delete(3)
		MergingChoose.insert(3,"----------------------------:")
		MergingChoose.insert(4,"------    MERGING RESULT    ----:")
		MergingChoose.insert(5,"{0}".format(WriteText_List(SyntacticResult_OntologyMerging)))
		MergingChoose.insert(6,"{0}".format(WriteText_List(FinalResultMerging)))
		MergingChoose.insert(7,"{0}".format(List_String))
		MergingChoose.insert(8,"{0}".format(WriteText_Dist(resultSIF)))
		
		messagebox.showinfo("Information","The result of Ontology Merging: \n\n {0}\n{1} \n{2}\n\n{3}".format(WriteText_List(SyntacticResult_OntologyMerging),WriteText_List(FinalResultMerging),List_String,WriteText_Dist(resultSIF)))

def SUMOSelection():
	MergingChoose.delete(0)
	global  SUMO_Merging
	#............... SUMO...............
	selection = listboxSUMO.curselection()	
	chooseListSUMO=[]
	for each in selection:
		dataList = listboxSUMO.get(each)
		chooseListSUMO.append(dataList)
		chooseListSUMO = list(dict.fromkeys(chooseListSUMO))
	
	if len(chooseListSUMO)<2:
		chooseListSUMO.append(AddThingIntoConcept(chooseListSUMO[0]))

	SUMO_Merging = chooseListSUMO
	MergingChoose.insert(0,"SUMO:{0}".format(chooseListSUMO))


def WIKIDATASelection():
	MergingChoose.delete(1)
	global WIKIDATA_Merging
	#............... WIKIDATA...............
	selection = listboxWIKIDATA.curselection()	
	chooseListWIKIDATA=[]
	for each in selection:
		dataList = listboxWIKIDATA.get(each)
		p = dataList.strip().split (" ")	
		chooseListWIKIDATA.append(p[0])
		chooseListWIKIDATA = list( dict.fromkeys(chooseListWIKIDATA))

	if len(chooseListWIKIDATA)<2:
		chooseListWIKIDATA.append(AddThingIntoConcept(chooseListWIKIDATA[0]))

	WIKIDATA_Merging = chooseListWIKIDATA
	MergingChoose.insert(1,"WIKIDATA:{0}".format(chooseListWIKIDATA))


def BABELNETSelection():
	MergingChoose.delete(2)
	global BABELNET_Merging
	#............... BABELNET...............
	selection = listboxBABELNET.curselection()	
	chooseListBABELNET=[]
	for each in selection:
		dataList = listboxBABELNET.get(each) 
		p = dataList.strip().split(" ")	
		chooseListBABELNET.append(p[0])
		chooseListBABELNET = list( dict.fromkeys(chooseListBABELNET))

	if len(chooseListBABELNET)<2:
		chooseListBABELNET.append(AddThingIntoConcept(chooseListBABELNET[0]))

	BABELNET_Merging = chooseListBABELNET
	MergingChoose.insert(2,"BABELNET:{0}".format(chooseListBABELNET))


def PrintListBox(ListOfInformation,listbox):
	listbox.delete(0,tk.END)
	i=1
	for each in ListOfInformation:
		listbox.insert(i,"{0}".format(each))
		i=i+1

def PrintListBox_Dist(ListOfInformation,listbox):
	listbox.delete(0,tk.END)
	i=1
	for each, value in ListOfInformation.items():
		listbox.insert(i,"{0}:{1}".format(each,value))
		i=i+1
def AddThingIntoConcept(concept):
	p = concept.strip().split ("->")
	result = "{0}->Thing".format(p[1])
	return result

def List_SimpleConcept_FromAxioms(list_data):
	Temp_SUMO=[]
	for each in list_data:
		p1 = each.strip().split ("->")
		Temp_SUMO.append(p1[0])
		Temp_SUMO.append(p1[1])
		Temp_SUMO = list( dict.fromkeys(Temp_SUMO))
	return Temp_SUMO

def Deduction_Concepts(data):
	result=[]
	for each1 in data:
		p1 = each1.strip().split ("->")
		for each2 in data:
			p2 = each2.strip().split ("->")
			if p1[0] == p2[1]:
				result.append("{0}->{1}".format(p2[0],p1[1]))
			if p2[0] == p1[1]:
				result.append("{0}->{1}".format(p1[0],p2[1]))
	result = list( dict.fromkeys(result))
	result.extend(data)
	return result

def Collection_ThreeConcept_Normalization(data,data_common):
	Data_Normalization=[]
	for each1 in data:
		p1 = each1.strip().split ("->")
		if p1[0] in set(data_common) and p1[1] in set(data_common):
			Data_Normalization.append("{0}".format(each1))
	return Data_Normalization

def  Normalization_SameConcept():
	global  SUMO_Merging
	global  WIKIDATA_Merging
	global  BABELNET_Merging
	SUMO_Data1 = SUMO_Merging  
	WIKIDATA_Data1 = WIKIDATA_Merging 
	BABELNET_Data1 = BABELNET_Merging 

	SUMO_Data = List_SimpleConcept_FromAxioms(SUMO_Data1)		
	WIKIDATA_Data = List_SimpleConcept_FromAxioms(WIKIDATA_Data1)		
	BABELNET_Data = List_SimpleConcept_FromAxioms(BABELNET_Data1)
	data_common = (set(SUMO_Data).intersection(set(WIKIDATA_Data))).intersection(set(BABELNET_Data))

	if(len(SUMO_Data)>3):
		data_Deduction_Concepts = Deduction_Concepts(SUMO_Data1)
		SUMO_Merging = Collection_ThreeConcept_Normalization(data_Deduction_Concepts,data_common)
		messagebox.showinfo("Information","SUMO's dataset is normalized as follows:\n{0}".format(SUMO_Merging))
	if(len(WIKIDATA_Data)>3):
		data_Deduction_Concepts = Deduction_Concepts(WIKIDATA_Data1)
		WIKIDATA_Merging = Collection_ThreeConcept_Normalization(data_Deduction_Concepts,data_common)
		messagebox.showinfo("Information","WIKIDATA's dataset is normalized as follows:\n{0}".format(WIKIDATA_Merging))
	if(len(BABELNET_Data)>3):
		data_Deduction_Concepts = Deduction_Concepts(BABELNET_Data1)
		BABELNET_Merging = Collection_ThreeConcept_Normalization(data_Deduction_Concepts,data_common)
		messagebox.showinfo("Information","BABELNET's dataset is normalized as follows:\n{0}".format(BABELNET_Merging))
		
#--------------------MODEL -----------------------
Relations = "->","<-","="
#Relations = "&#8549;","&#8550","="
InputAtomicConcepts="ABC"



#----------------------Button-------------------
m1 = PanedWindow()
m1.pack()
btn = Button(window, text="print",command=print_me)
m1.add(btn)
btn1 = Button(window, text="Search",command=Searching)
m1.add(btn1)
btn2 = Button(window, text="Get Same Concepts",command=GetSameConcept)
m1.add(btn2)
btnMerging = Button(window, text="Ontology Merging",command=OntologyMerging)
m1.add(btnMerging)
btnNormalization = Button(window, text="Normalization",command=Normalization_SameConcept)
m1.add(btnNormalization)



m2 = PanedWindow()
m2.pack()
btnSUMO = Button(window, text="Select SUMO",command=SUMOSelection)
m2.add(btnSUMO)
btnWIKIDATA = Button(window, text="Select WIKIDATA",command=WIKIDATASelection)
m2.add(btnWIKIDATA)
btnBABELNET = Button(window, text="Select BABELNET",command=BABELNETSelection)
m2.add(btnBABELNET)


scrollbar = Scrollbar(window, orient="vertical")
scrollbar.config(command=listbox.yview)
scrollbar.pack(side="left", fill="y")

listbox.pack(side=tk.LEFT)
listbox.config(yscrollcommand=scrollbar.set)

listboxMapping.pack(side=tk.LEFT)

listboxSUMO.pack(side=tk.LEFT)
listboxWIKIDATA.pack(side=tk.LEFT)
listboxBABELNET.pack(side=tk.LEFT)

MergingChoose.pack(side=tk.TOP)
listboxWIKIDATA_Choose.pack(side=tk.LEFT)



listboxBABELNET_Choose.pack(side=tk.LEFT)

window.resizable(tk.TRUE,tk.TRUE)
window.mainloop()






endstart = time.time()
print("Time:",endstart - timestart)







