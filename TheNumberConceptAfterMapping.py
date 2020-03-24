import os

Name="SUMO"
Level=8
#Note: SUMO (Consider m[0]), Babelnet (Consider m[1]), Wikidata (Consider m[2])

#note: _1_.. need to remove
mapping = open("MAPPING/Data_MappingSUMO2WIKIDATA_Merging_NewName.txt", "r")
output1 = open("Concept_AfterMapping/SUMO_AfterMapping_Concept.txt".format(Name,Level), 'w')
output2 = open("Concept_AfterMapping/WIKIDATA_AfterMapping_Concept.txt".format(Name,Level), 'w')
output3 = open("Concept_AfterMapping/BABELNET_AfterMapping_Concept.txt".format(Name,Level), 'w')
#source = open("{0}/{0}_Taxonomy_level{1}.txt".format(Name,Level), "r")
count=0
SUMO=[]
BABELNET=[]
WIKIDATA=[]
Taxonomy=[]
Mapping=[]

print("Level "+str(Level))
print("Loading dataset.")

#Read from mapping source
for eachMapping in mapping:
	p = eachMapping.strip().split(",")
	Mapping.append([p[0],p[1],p[2],p[3]])
	SUMO.append(p[0])
	BABELNET.append(p[1])
	WIKIDATA.append(p[2])


SUMO = list(dict.fromkeys(SUMO))
print("SUMO",len(SUMO))

WIKIDATA = list(dict.fromkeys(WIKIDATA))
print("Wikidata:",len(WIKIDATA))

BABELNET = list(dict.fromkeys(BABELNET))
print("Babelnet:",len(BABELNET))


print("Done!, Read Dataset.")

#-------------------------------
for each in SUMO:
	output1.write(each+"\n")
	#print(data)

print("Done SUMO!")
output1.close()
#-------------------------------
for each in WIKIDATA:
	output2.write(each+"\n")
	#print(data)

print("Done WIKIDATA!")
output2.close()
#-------------------------------
for each in BABELNET:
	output3.write(each+"\n")
	#print(data)

print("Done BABELNET!")
output3.close()





