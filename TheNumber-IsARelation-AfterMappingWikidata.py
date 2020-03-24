import os

Name="SUMO"
Level=8
#Note: SUMO (Consider m[0]), Babelnet (Consider m[1]), Wikidata (Consider m[2])


inputWIKIDATA = open("WIKIDATA/WIKIDATA_Father_Child.txt", "r")
inputWIKIDATA_ConceptAfterMapping = open("Concept_AfterMapping/WIKIDATA_AfterMapping_Concept.txt", "r")

output2 = open("IsARelation_AfterMapping/WIKIDATA_IsARelation_AfterMapping_Concept.txt".format(Name,Level), 'w')


WIKIDATA=[]
WIKIDATA_ConceptAfterMapping=[]
WIKIDATA_Output=[]


print("Loading dataset.")

#Read from mapping source


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


#-------------------------------
for each in WIKIDATA_Output:
	data = str(each[0])+"->"+str(each[1])+"\n"
	output2.write(data)
print("Done WIKIDATA!")


