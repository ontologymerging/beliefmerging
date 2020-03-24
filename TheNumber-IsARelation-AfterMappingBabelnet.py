import os

Name="SUMO"
Level=8
#Note: SUMO (Consider m[0]), Babelnet (Consider m[1]), Wikidata (Consider m[2])



inputBABELNET = open("BABELNET/BABELNET_Father_Child.txt", "r")
inputBABELNET_ConceptAfterMapping = open("Concept_AfterMapping/BABELNET_AfterMapping_Concept.txt", "r")

output3 = open("IsARelation_AfterMapping/BABELNET_IsARelation_AfterMapping_Concept.txt".format(Name,Level), 'w')

SUMO=[]
SUMO_ConceptAfterMapping=[]
SUMO_Output=[]

BABELNET=[]
BABELNET_ConceptAfterMapping=[]
BABELNET_Output=[]


WIKIDATA=[]
WIKIDATA_ConceptAfterMapping=[]
WIKIDATA_Output=[]


print("Loading dataset.")

#Read from mapping source



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
	if each[0] in set_BABELNET:
		flag1=1
	if each[1] in set_BABELNET:
		flag2=1
	if flag1==1 and flag2==1:
		print(each)
		BABELNET_Output.append(each)
		
			
	#print(each)
	#for e in BABELNET_ConceptAfterMapping:
	#	if each[0] == e:
	#		flag1=1
	#		print(each)
	#		break
	#for e in BABELNET_ConceptAfterMapping:
	#	if each[1] == e:
	#		flag2=1
	#		break
	
	
print("Done BABELNET!")
print("BABELNET",len(BABELNET_Output))
#======================================================================


#-------------------------------
for each in BABELNET_Output:
	data = str(each[0])+"->"+str(each[1])+"\n"
	output3.write(data)
print("Done BABELNET!")
	#print(data)

print("Done BABELNET!")
#output3.close()




