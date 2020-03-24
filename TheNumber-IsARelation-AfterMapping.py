import os

Name="SUMO"
Level=8
#Note: SUMO (Consider m[0]), Babelnet (Consider m[1]), Wikidata (Consider m[2])

#note: _1_.. need to remove
#mapping = open("MAPPING/Data_MappingSUMO2WIKIDATA_Merging_NewName.txt", "r")
inputSUMO = open("SUMO/SUMO_Father_Child.txt", "r")
inputSUMO_ConceptAfterMapping = open("Concept_AfterMapping/SUMO_AfterMapping_Concept.txt", "r")

inputWIKIDATA = open("WIKIDATA/WIKIDATA_Father_Child.txt", "r")
inputWIKIDATA_ConceptAfterMapping = open("Concept_AfterMapping/WIKIDATA_AfterMapping_Concept.txt", "r")

inputBABELNET = open("BABELNET/BABELNET_Father_Child.txt", "r")
inputBABELNET_ConceptAfterMapping = open("Concept_AfterMapping/BABELNET_AfterMapping_Concept.txt", "r")

output1 = open("IsARelation_AfterMapping/SUMO_IsARelation_AfterMapping_Concept.txt".format(Name,Level), 'w')
output2 = open("IsARelation_AfterMapping/WIKIDATA_IsARelation_AfterMapping_Concept.txt".format(Name,Level), 'w')
output3 = open("IsARelation_AfterMapping/BABELNET_IsARelation_AfterMapping_Concept.txt".format(Name,Level), 'w')
#source = open("{0}/{0}_Taxonomy_level{1}.txt".format(Name,Level), "r")
count=0

SUMO=[]
SUMO_ConceptAfterMapping=[]
SUMO_Output=[]

BABELNET=[]
BABELNET_ConceptAfterMapping=[]
BABELNET_Output=[]


WIKIDATA=[]
WIKIDATA_ConceptAfterMapping=[]
WIKIDATA_Output=[]

Taxonomy=[]
Mapping=[]


print("Loading dataset.")

#Read from mapping source

#'''
for each in inputSUMO:
	p = each.strip().split("->")
	SUMO.append([p[0],p[1]])
for each in inputSUMO_ConceptAfterMapping:
	#print(each)
	SUMO_ConceptAfterMapping.append(each)

#for each in SUMO_ConceptAfterMapping:
#	print(each)
print("Done Loading SUMO.")
for each in SUMO:
	flag1=0
	flag2=0
	for e in SUMO_ConceptAfterMapping:
		if each[0] in e:
			flag1=1
			break
	for e in SUMO_ConceptAfterMapping:
		if each[1] in e:
			flag2=1
			break
	if flag1==1 and flag2==1:
		SUMO_Output.append(each)


print("Done SUMO!")

#SUMO = list(dict.fromkeys(SUMO))
print("SUMO",len(SUMO_Output))

#'''

print("Loading WIKIDATA dataset.")
#---------------------------------------------------------------------
for each in inputWIKIDATA:
	p = each.strip().split(" ")
	WIKIDATA.append([p[0],p[3]])

for each in inputWIKIDATA_ConceptAfterMapping:
	p = each.strip().split("\n")
	WIKIDATA_ConceptAfterMapping.append(p[0])

print("Done SUMO!")
#for each in WIKIDATA:
#	print(each)
set_WIKIDATA = set(WIKIDATA_ConceptAfterMapping)
#print(set_WIKIDATA)
for each in WIKIDATA:
	flag1=0
	flag2=0
	if each[0] in set_WIKIDATA:
		flag1=1
	if each[1] in set_WIKIDATA:
		flag2=1
	if flag1==1 and flag2==1:
		print(each)
		WIKIDATA_Output.append(each)

print("Done WIKIDATA!")
print("WIKIDATA",len(WIKIDATA_Output))

'''

#======================BABELNET===================================
print("Running Babelnet")
for each in inputBABELNET:
	p = each.strip().split(" ")
	BABELNET.append([p[0],p[1]])

for each in inputBABELNET_ConceptAfterMapping:
	p = each.strip().split("\n")
	BABELNET_ConceptAfterMapping.append(p[0])
print("Reading Done!")

#for each in BABELNET:
#	print(each)
set_BABELNET = set(BABELNET_ConceptAfterMapping)
#print(set_WIKIDATA)
for each in BABELNET:
	flag1=0
	flag2=0
	#print(each)
	for e in BABELNET_ConceptAfterMapping:
		if each[0] == e:
			flag1=1
			#print(each)
			break
	for e in BABELNET_ConceptAfterMapping:
		if each[1] == e:
			flag2=1
			break
	
	if flag1==1 and flag2==1:
		print(each)
		BABELNET_Output.append(each)

print("Done BABELNET!")
print("BABELNET",len(BABELNET_Output))
#======================================================================
'''



#-------------------------------
for each in SUMO_Output:
	data = str(each[0])+"->"+str(each[1])+"\n"
	output1.write(data)
print("Done SUMO!")
#output1.close()
#-------------------------------
for each in WIKIDATA_Output:
	data = str(each[0])+"->"+str(each[1])+"\n"
	output2.write(data)
print("Done WIKIDATA!")

#print("Done WIKIDATA!")
#output2.close()
'''

#-------------------------------
for each in BABELNET_Output:
	data = str(each[0])+"->"+str(each[1])+"\n"
	output3.write(data)
	print("Done BABELNET!")
	#print(data)

print("Done BABELNET!")
#output3.close()
'''



