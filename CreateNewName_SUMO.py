import os

Name="SUMO"
Level=8
#Note: SUMO (Consider m[0]), Babelnet (Consider m[1]), Wikidata (Consider m[2])

#note: _1_.. need to remove
mapping = open("MAPPING/Data_MappingSUMO2WIKIDATA_Merging_NewName.txt", "r")
output = open("{0}/NewName/{0}_Taxonomy_level{1}_1_NewName.txt".format(Name,Level), 'w')
source = open("{0}/{0}_Taxonomy_level{1}.txt".format(Name,Level), "r")
count=0
SUMO=[]
BABELNET=[]
WIKIDATA=[]
Taxonomy=[]
Mapping=[]

print("Level "+str(Level))
print("Loading dataset.")
#Read from Taxonomy of each level
for each in source:
	p = each.strip().split("->")
	Taxonomy.append([p[0],p[1]])

#for i in Taxonomy:
#	print(i[0])

#Read from mapping source
for eachMapping in mapping:
	p = eachMapping.strip().split(",")
	Mapping.append([p[0],p[1],p[2],p[3]])

#for i in Mapping:
#	print(i[0])

print("Done!, Read Dataset.")

Array_NewName=[]
for t in Taxonomy:	
	for m in Mapping:
		bn = t[0]#t[0][:t[0].find("_")]
		#print(bn, m[1])
		if bn == m[0]:			
			Array_NewName.append([m[3],t[1]])
			#print(m[3],t[1])
			#print(t,m)

print("Done!, Change Father.")


Array_NewName2=[]
for t in Array_NewName:	
	for m in Mapping:
		bn = t[1]#t[1][:t[1].find("_")]
		#print(m[0],bn)
		if bn == m[0]:
			Array_NewName2.append([t[0],m[3]])
			#print(t[0],m[3])

#output
print("Done!, Change Child.")
for each in Array_NewName2:
	#print(each)
	data = str(each[0])+"->"+str(each[1])
	output.write(data+"\n")
	#print(data)

print("Done all!")
output.close()





