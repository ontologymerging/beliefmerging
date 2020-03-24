# -*- coding: utf-8 -*-
import os
import os.path
import gzip
import json
import time
#import rdflib

from py4j.java_gateway import JavaGateway

gateway = JavaGateway()

def wrap_java(obj):
    """Adds a decent __repr__ method to obj's class. obj is a Java object."""
    def __repr__(self):
        return str(self)
    setattr(obj.__class__, "__repr__", __repr__)
    return obj

class RdfDict():
    """An RdfDict is a dict that associates either a URI or a name with a value.
For instance, "http://www.w3.org/2002/07/owl#Class" and "Class" are associated with the same value.
When a key is not found, rather than raising an exception, a None value is returned."""

    def __init__(self, d):
        self.d = d
        # 'short' is a fallback dictionary, with non-prefixed names as strings.
        # For instance, "http://www.w3.org/2002/07/owl#Class" becomes "Class".
        self.short = {k.split("#")[-1]: d[k] for k in d.keys()}
    
    def __getitem__(self, key):
        if key in self.d:
            return self.d[key]
        elif key in self.short:
            return self.short[key]
        return None

    def __repr__(self):
        return self.d.__repr__()


class OntologyTerminology():
    def __init__(self, onto):
        self.onto = onto
        self.Classes = self.onto.Classes
        self.ObjectProperties = self.onto.ObjectProperties

    def __getattr__(self, name: str):
        """__getattr__ performs a lazy evaluation of most methods."""
        if name == "SubClassOf":
            return self._SubClassOf()
        elif name == "SuperClassOf":
            return self._SuperClassOf()
        elif name == "EquivalentClasses":
            return self._EquivalentClasses()
        elif name == "DisjointClasses":
            return self._DisjointClasses()
        elif name == "SubObjectPropertyOf":
            return self._SubObjectPropertyOf()
        elif name == "ObjectPropertyDomain":
            return self._ObjectPropertyDomain()
        elif name == "ObjectPropertyRange":
            return self._ObjectPropertyRange()
        elif name == "FunctionalObjectProperty":
            return self._FunctionalObjectProperty()
        else:
            raise AttributeError("unknown attribute '{0}'".format(name))
    
    def _SubClassOf(self):
        self.SubClassOf = self.onto.SubClassOf
        return self.SubClassOf
    
    def _SuperClassOf(self):
        self.SuperClassOf = self.onto.SuperClassOf
        return self.SuperClassOf
    
    def _EquivalentClasses(self):
        self.EquivalentClasses = self.onto.EquivalentClasses
        return self.EquivalentClasses
    
    def _DisjointClasses(self):
        self.DisjointClasses = self.onto.DisjointClasses
        return self.DisjointClasses
    
    def _SubObjectPropertyOf(self):
        self.SubObjectPropertyOf = self.onto.SubObjectPropertyOf
        return self.SubObjectPropertyOf
    
    def _ObjectPropertyDomain(self):
        self.ObjectPropertyDomain = self.onto.ObjectPropertyDomain
        return self.ObjectPropertyDomain
    
    def _ObjectPropertyRange(self):
        self.ObjectPropertyRange = self.onto.ObjectPropertyRange
        return self.ObjectPropertyRange
    
    def _FunctionalObjectProperty(self):
        self.FunctionalObjectProperty = self.onto.FunctionalObjectProperty
        return self.FunctionalObjectProperty


class OntologyFacts():
    def __init__(self, onto):
        self.onto = onto
        self.NamedIndividuals = self.onto.NamedIndividuals
    
    def __getattr__(self, name: str):
        """__getattr__ performs a lazy evaluation of most methods."""
        if name == "ClassAssertion":
            return self._ClassAssertion()
        elif name == "Type":
            return self._Type()
        elif name == "ObjectPropertyAssertion":
            return self._ObjectPropertyAssertion()
        else:
            raise AttributeError("unknown attribute '{0}'".format(name))
    
    def _ClassAssertion(self):
        self.ClassAssertion = self.onto.ClassAssertion
        return self.ClassAssertion
    
    def _Type(self):
        self.Type = self.onto.Type
        return self.Type
    
    def _ObjectPropertyAssertion(self):
        self.ObjectPropertyAssertion = self.onto.ObjectPropertyAssertion
        return self.ObjectPropertyAssertion


class OntologyInfo():
    def __init__(self, onto):
        self.onto = onto
        self.URI = self.onto.URI


class Ontology():
    def __init__(self, path: str):

        self.onto = gateway.entry_point.loadOWLOntology(path)
        self.Classes = [wrap_java(c) for c in self.onto.classesInSignature().toArray()]
        self.NamedIndividuals = [wrap_java(c) for c in self.onto.individualsInSignature().toArray()]
        self.ObjectProperties = [wrap_java(c) for c in self.onto.objectPropertiesInSignature().toArray()]
        self.URI = self.onto.getOntologyID().getOntologyIRI().get()
        self.generalClassAxioms = self.onto.generalClassAxioms().toArray()
        #self.ObjectProperties = {s for s, _, o in self.onto if str(o) == "http://www.w3.org/2002/07/owl#ObjectProperty"}
        #self.NamedIndividuals = {s for s, _, o in self.onto if str(o) == "http://www.w3.org/2002/07/owl#NamedIndividual"}
        self.info = OntologyInfo(self)
        self.DataProperties = [wrap_java(c) for c in self.onto.dataPropertiesInSignature().toArray()]


        #self.term = OntologyTerminology(self)
        #self.facts = OntologyFacts(self)

        '''Get Instance and Concetps'''






    
    def __getattr__(self, name: str):
        """__getattr__ performs a lazy evaluation of most methods."""
        if name == "SubClassOf":
            return self._SubClassOf()
        elif name == "ClassIndividual":
            return self._ClassIndividual()
        elif name == "AnnotationClass":
            return self._AnnotationClass()
        elif name == "AnnotationIndividual":
            return self._AnnotationIndividual()
        elif name == "SuperClassOf":
            return self._SuperClassOf()
        elif name == "Taxonomy":
            return self._Taxonomy()
        elif name == "Taxonomy1":
            return self._Taxonomy1()
        elif name == "EquivalentClasses":
            return self._EquivalentClasses()
        elif name == "DisjointClasses":
            return self._DisjointClasses()
        elif name == "SubObjectPropertyOf":
            return self._SubObjectPropertyOf()
        elif name == "ObjectPropertyDomain":
            return self._ObjectPropertyDomain()
        elif name == "ObjectPropertyRange":
            return self._ObjectPropertyRange()
        elif name == "ClassAssertion":
            return self._ClassAssertion()
        elif name == "Type":
            return self._Type()
        elif name == "ObjectPropertyAssertion":
            return self._ObjectPropertyAssertion()
        elif name == "FunctionalObjectProperty":
            return self._FunctionalObjectProperty()
        else:
            raise AttributeError("unknown attribute '{0}'".format(name))

    def _AnnotationIndividual(self):
        self.AnnotationIndividual = {}
        for i in self.NamedIndividuals:
            self.AnnotationIndividual[i] = []
            annotationIndividual = gateway.entry_point.loadAnnotationEntity(i,self.onto)
            while annotationIndividual.hasNext():
                self.AnnotationIndividual[i].append(annotationIndividual.next().getValue())
        return self.AnnotationIndividual


    def _AnnotationClass(self):
        self.AnnotationClass = {}
        for c in self.Classes:
            self.AnnotationClass[c]=[]
            annotationClass = gateway.entry_point.loadAnnotationEntity(c,self.onto)
            while annotationClass.hasNext():
                self.AnnotationClass[c].append(annotationClass.next().getValue())
        return self.AnnotationClass
    def _Taxonomy1(self):
        self.Taxonomy1 = {}
        for c in self.Classes:
            self.Taxonomy1[c] = []
            #print("HienThiSubclass:",c)
            sco = self.onto.subClassAxiomsForSubClass(c).toArray()
            for it in sco:
                sup = it.getSuperClass()
                self.Taxonomy1[c].append(wrap_java(sup))
        for id, value in self.Taxonomy1.items():

            cls =str(id)
            if "[]" in str(value) :
                #cls = cls[cls.find('dataset/')+7:]
                cls = cls[cls.find('#')+1:-1]
                data = "{0}".format(cls)
                print(data)
                KQ = self.onto.subClassAxiomsForSuperClass(id).toArray()
                for it in KQ:
                    sub = it.getSubClass()
                    strwrap = str(wrap_java(sub))
                    strwrap = strwrap[strwrap.find('dataset/')+8:]
                    strwrap = strwrap[strwrap.find('#')+1:-1]
                    data1 = data +" -> "+strwrap
                    print(data1)              
        return self.Taxonomy1

    def _Taxonomy(self):
        self.Taxonomy = {}
        self.Ta=[]
        for c in self.Classes:
            self.Taxonomy[c] = []
            sco = self.onto.subClassAxiomsForSubClass(c).toArray()
            for it in sco:
                sup = it.getSuperClass()
                self.Taxonomy[c].append(wrap_java(sup))
        StackClass =[]
        data=""
        count=0
        LuuVet=[]
        output = open("File/{0}/{0}_Taxonomy.txt".format(fname), 'w', encoding='utf-8')
        for id, value in self.Taxonomy.items():
            data=""
            if "[]" in str(value) :                
                StackClass.append(id)
                d1=str(id)
                d1 = d1[d1.find('#')+1:-1]
                LuuVet.append(d1+"_1")
                count=count+1
                level=0
                while len(StackClass)>0:

                    cStack = StackClass.pop()                    
                    R = self.onto.subClassAxiomsForSuperClass(cStack).toArray()

                    if len(R)==0: 
                        data = LuuVet.pop()                       
                        print(data)
                        output.write(data+"\n")
                        #self.Ta.append(LuuVet.pop())
                    else:
                        val_LuuVet = LuuVet.pop()
                        level = int(val_LuuVet[len(val_LuuVet)-1:])
                        level=level+1
                        #Notice that we can modify the level
                        if level>2:
                            break;

                    for it in R:
                        sub = it.getSubClass()
                        StackClass.append(sub)
                        
                        d1=str(val_LuuVet)
                        d1 = d1[d1.find('#')+1:]
                        d2 = str(wrap_java(sub))
                        d2 = d2[d2.find('#')+1:-1]
                        data = d1 +"->"+ d2+"_"+str(level)
                        LuuVet.append(data)
        output.close()
        return self.Taxonomy
    
    def _SubClassOf(self):
        self.SubClassOf = {}
        for c in self.Classes:
            self.SubClassOf[c] = []
            #print("HienThiSubclass:",c)
            sco = self.onto.subClassAxiomsForSubClass(c).toArray()
            for it in sco:
                sup = it.getSuperClass()
                self.SubClassOf[c].append(wrap_java(sup))
        #self.SubClassOf = RdfDict(self.SubClassOf)
        return self.SubClassOf
    
    def _SuperClassOf(self):
        self.SuperClassOf = {}
        for c in self.Classes:
            self.SuperClassOf[c] = []
            sco = self.onto.subClassAxiomsForSuperClass(c).toArray()
            for it in sco:
                sub = it.getSubClass()
                self.SuperClassOf[c].append(wrap_java(sub))
                #print each superClass
                #print(self.SuperClassOf[c])
        #self.SuperClassOf = RdfDict(self.SuperClassOf)
        return self.SuperClassOf
    
    def _EquivalentClasses(self):
        self.EquivalentClasses = {}
        for c in self.Classes:
            self.EquivalentClasses[c] = []
            eca = self.onto.equivalentClassesAxioms(c).toArray()
            for it in eca:
                classes = it.namedClasses().toArray()
                for c2 in classes:
                    if c2 is not c:
                        self.EquivalentClasses[c].append(wrap_java(c2))
        return self.EquivalentClasses
    
    def _DisjointClasses(self):
        self.DisjointClasses = {}
        for c in self.Classes:
            self.DisjointClasses[c] = []
            dca = self.onto.disjointClassesAxioms(c).toArray()
            for it in dca:
                classes = it.operands().toArray()
                for c2 in classes:
                    if c2 != c:
                        self.DisjointClasses[c].append(wrap_java(c2))
        #self.DisjointClasses = RdfDict(self.DisjointClasses)
        return self.DisjointClasses
    
    def _SubObjectPropertyOf(self):
        self.SubObjectPropertyOf = {}
        for s, p, o in self.onto:
            if str(p) == "http://www.w3.org/2000/01/rdf-schema#subPropertyOf":
                if s not in self.SubObjectPropertyOf:
                    self.SubObjectPropertyOf[s] = [o]
                else:
                    self.SubObjectPropertyOf[s].append(o)
        self.SubObjectPropertyOf = RdfDict(self.SubObjectPropertyOf)
        return self.SubObjectPropertyOf
    
    def _ObjectPropertyDomain(self):
        self.ObjectPropertyDomain = {}
        for p in self.ObjectProperties:
            self.ObjectPropertyDomain[p] = []
            opd = self.onto.objectPropertyDomainAxioms(p).toArray()
            for it in opd:
                compo = it.componentsWithoutAnnotations().toArray()
                for p2 in compo:
                    if p2 != p:
                        self.ObjectPropertyDomain[p].append(p2)
        #self.ObjectPropertyDomain = RdfDict(self.ObjectPropertyDomain)
        return self.ObjectPropertyDomain
    
    def _ObjectPropertyRange(self):
        self.ObjectPropertyRange = {}
        for p in self.ObjectProperties:
            self.ObjectPropertyRange[p] = []
            opd = self.onto.objectPropertyRangeAxioms(p).toArray()
            for it in opd:
                compo = it.componentsWithoutAnnotations().toArray()
                for p2 in compo:
                    if p2 != p:
                        self.ObjectPropertyRange[p].append(p2)
        #self.ObjectPropertyRange = RdfDict(self.ObjectPropertyRange)
        return self.ObjectPropertyRange
    
    def _ClassAssertion(self):
        self.ClassAssertion = {}
        for s, p, o in self.onto:
            if str(p) == "http://www.w3.org/2002/07/owl#classAssertion":
                if s not in self.ClassAssertion:
                    self.ClassAssertion[s] = [o]
                else:
                    self.ClassAssertion[s].append(o)
        self.ClassAssertion = RdfDict(self.ClassAssertion)
        return self.ClassAssertion

    def _Type(self):
        self.Type = {}
        for s, p, o in self.onto:
            if str(p) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
                if s not in self.Type:
                    self.Type[s] = [o]
                else:
                    self.Type[s].append(o)
        self.Type = RdfDict(self.Type)
        return self.Type
    
    def _ObjectPropertyAssertion(self):
        self.ObjectPropertyAssertion = {}
        for s, p, o in self.onto:
            if str(p) == "http://www.w3.org/2002/07/owl#objectPropertyAssertion":
                if s not in self.ObjectPropertyAssertion:
                    self.ObjectPropertyAssertion[s] = [o]
                else:
                    self.ObjectPropertyAssertion[s].append(o)
        self.ObjectPropertyAssertion = RdfDict(self.ObjectPropertyAssertion)
        return self.ObjectPropertyAssertion
    
    def _FunctionalObjectProperty(self):
        self.FunctionalObjectProperty = set()
        for p in self.ObjectProperties:
            self.ObjectPropertyRange[p] = []
            fop = self.onto.functionalObjectPropertyAxioms(p).toArray()
            if len(fop) != 0:
                self.FunctionalObjectProperty.add(p)
        return self.FunctionalObjectProperty


    def _ClassIndividual(self):
        self.ClassIndividual = {}
        self.Reasoner = gateway.entry_point.loadReasoner(self.onto)
        for c in self.Classes:
            self.ClassIndividual[c] = []
            ci = self.Reasoner.getInstances(c, True)
            self.ClassIndividual[c].append(ci.getFlattened())
        return self.ClassIndividual



#nameFile="dataset/baseball.owl"
#nameFile="dataset/Product.owl"
nameFile="dataset/SUMO.owl"
#nameFile="dataset/Shopping.owl"
#nameFile="dataset/WordNet.owl"
#nameFile="dataset/dbpedia.owl"
#nameFile="dataset/pizza.owl"
o = Ontology(nameFile)
from wikidata.client import Client
import re

if __name__ == "__main__":


    '''------------------------------------ URI and file name---------------------------------'''
    print("\nLink:",o.URI," --> Result: " ,o.URI is o.info.URI)
    fname = str(nameFile).split('/')[-1:][0].split(".")[0]

    '''------------------------------------ Directory to store the storage files---------------------------------'''
    directory="File/{0}/".format(fname)

    if not os.path.exists(directory):
        os.makedirs(directory)

    print("================== -- START PROGRAMME -- =======================")
    #--------------------SUMO2WIKIDATA (Split words----------------------------
    # Example: HighSchool --> High School     in order to find on Babelnet.
    print("====================================== -- Taxonomy -- ===============================================")
    output = open("File/{0}/{0}_Taxonomy.txt".format(fname), 'w', encoding='utf-8')
    o.Taxonomy
 
    '''
    for id, value in o.SubClassOf.items():
        #print("ID:",id,"VALUE:",value)
        #for eachValue in value:
        cls = id
        id =str(id)
        if "#" in id:
            id = id[id.find('#')+1:-1]
        data = "{0}".format(id)
        if "[]" in str(value) :
            #print(data)
            output.write(data + '\n')
    output.close()
    '''
    print("Done!")
    '''
    print("==================================== -- Class and Individual -- =====================")
    fileWikidata = open("/home/thanhma/Downloads/Concept_Instance_wikidata.txt", "r")
    client = Client()
    count=0
    for eachID in fileWikidata:
        id_WikiData=eachID.split()[0]
        entity = client.get('P31')
        print(id_WikiData,". ",entity.attributes) #['labels']['en']['value']
        count=count+1
        print(entity.description)
        if count==10:
            break
    '''
    '''
    count=0
    for id, value in o.ClassIndividual.items():
        name= "{0}".format(id)
        if "#" in name:
	        name = name[name.find('#')+1:-1]
        else:
            if "owl:" in name:
                name = name[name.find('owl:')+4: ]
            else:
                name = name[name.find('dataset/')+8:-1]
        count=count+1
        print(count,". ", name)
        output = open("File/{0}/File/{1}_{2}.txt".format(fname,count,name), 'w', encoding='utf-8')
        for eachValue in value:
            for e in eachValue:
                #print("Concept: ",id, "==> Instance: ", e)
                #output = open("File/{0}/{0}/File/.txt".format(fname), 'w', encoding='utf-8')
                data = "Concept:{0}  ==>  Instance: {1}".format(id, e)                
                #data = "Concept:{0}  ==>  Instance: {1}".format(id, e)
                output.write(data + '\n')
  
        output.close()
    print("Done!")
    '''
    #'''
    output = open("File/{0}/{0}_SUMO2WIKIDATA_Split_Words.txt".format(fname), 'w', encoding='utf-8')
    output_except = open("File/{0}/{0}_SUMO2WIKIDATA_Split_Words_Except1.txt".format(fname), 'w', encoding='utf-8')
    client = Client() 
    count=0
    for value in o.Classes:
        name= "{0}".format(value)
        #print("DauTien:",name)
        if "EnglishLanguage:" in name:
            name = name[name.find('EnglishLanguage:')+16:-1]
        else:
            if "#" in name:
	            name = name[name.find('#')+1:-1]
            else:
                if "owl:" in name:
                    name = name[name.find('owl:')+4: ]
                else:
                    name = name[name.find('dataset/')+8:-1]
        print("Name:",name)
        #WordByWord= re.findall('[A-Z][^A-Z]*', name)
        WordByWord=re.sub( r"([A-Z])", r" \1", name).split()

        Name_SplitWords=""
        for eachWord in WordByWord:
            if len(eachWord)==1:
                Name_SplitWords = "{0}{1}".format(Name_SplitWords, eachWord)                    
            else:
                Name_SplitWords = "{0} {1}".format(Name_SplitWords, eachWord)
        print(Name_SplitWords.strip())
        if Name_SplitWords=="":
            Name_SplitWords= name
        Name_SplitWords=Name_SplitWords.strip()
        count=count+1	
        print(count,". Split Word:",Name_SplitWords)  
              
        try:
            Babelnet = gateway.entry_point.loadBabelNet_Words(Name_SplitWords)
            if "{0}".format(Babelnet)!="":
                for i in Babelnet:        
                    id_WikiData= "{0}".format(i)
                    id_WikiData = id_WikiData[id_WikiData.find("WIKIDATA:")+9:]
                    entity = client.get(id_WikiData, load=True)
                    data="SUMO:{0} - {1} - Description_WIKI: {2}".format(Name_SplitWords,i,entity.description)
                    print(data)
                    output.write(data + '\n')
            
                    output_except.write(Name_SplitWords + '\n')
        except:
            pass
        
    output.close()
    output_except.close()
    print("Done!") 
    #'''
           

    #--------------------SUMO2WIKIDATA (not yet splitting words)----------------------------
    '''
    output = open("File/{0}/{0}_SUMO2WIKIDATA_Words.txt".format(fname), 'w', encoding='utf-8')
    client = Client() 
    for value in o.Classes:
        name= "{0}".format(value)
        if "#" in name:
            name = name[name.find('#')+1:-1]
        else:
            if "EnglishLanguage:" in name:
	            name = name[name.find('EnglishLanguage:')+16:-1]
            else:
                if "owl:" in name:
                    name = name[name.find('owl:')+4: ]
                else:
                    name = name[name.find('dataset/')+8:-1]

        print(name)
        try:
            Babelnet = gateway.entry_point.loadBabelNet_Words(name)
            if "{0}".format(Babelnet)!="":
                for i in Babelnet:        
                    id_WikiData= "{0}".format(i)
                    id_WikiData = id_WikiData[id_WikiData.find("WIKIDATA:")+9:]
                    entity = client.get(id_WikiData, load=True)
                    data="SUMO:{0} - {1} - Description_WIKI: {2}".format(name,i,entity.description)
                    print(data)
                    output.write(data + '\n')
        except:
            pass

    output.close()
    print("Done!") 
    '''

    '''
    output = open("File/{0}/{0}_SUMO2WIKIDATA1.txt".format(fname), 'w', encoding='utf-8')
    
    try:
        client = Client() 
        for id, value in o.AnnotationClass.items():
            for eachValue in value:
                if "wn#" in "{0}".format(eachValue):
                    data = "Concept:{0}  ==>  Annotation: {1}".format(id, eachValue)
                    eachAnnotation="{0}".format(eachValue)
                    idwordnet = "wn:{0}n".format(eachAnnotation[-8:])
                    print(idwordnet)                    
                    try:
                        Babelnet = gateway.entry_point.loadBabelNet_WordNet(idwordnet)
                        data ="SUMOConcept: {0} - {1} -  {2}".format(id, idwordnet, Babelnet)
                        print("Babelnet:",Babelnet)                        

                        if "{0}".format(Babelnet)!="":
                            id_WikiData= "{0}".format(Babelnet)
                            id_WikiData = id_WikiData[id_WikiData.find("WIKIDATA:")+9:]
                            print("idWikidata:",id_WikiData)
                            entity = client.get(id_WikiData, load=True)
                            print(entity.description)
                            data="{0} - Description: {1}".format(data,entity.description)
                            print(data)
                            output.write(data + '\n') 

                    except:
                        pass
            #break
    except :
        print("An error!!!: ")

    output.close()
    print("Done!")    
    '''
    '''
    for id, value in o.AnnotationClass.items():
        for eachValue in value:
            if "wn#" in "{0}".format(eachValue):
                data = "Concept:{0}  ==>  Annotation: {1}".format(id, eachValue)
                eachAnnotation="{0}".format(eachValue)
                idwordnet = "wn:{0}n".format(eachAnnotation[-8:])
                print(idwordnet)                    
                #try:
                Babelnet = gateway.entry_point.loadBabelNet_WordNet(idwordnet)
                data ="SUMOConcept: {0} - {1} -  {2}".format(id, idwordnet, Babelnet)
                print("Babelnet:",Babelnet)
   
                if "{0}".format(Babelnet)!="":
                    print(data)
                    output.write(data + '\n')
                    id_WikiData= "{0}".format(Babelnet)
                    id_WikiData = id_WikiData[id_WikiData.find(":")+1:]
                    print("idWikidata:",id_WikiData)
                    entity = client.get(id_WikiData, load=True)
                    print(entity.description) 
                    #except:
                    #    pass
            #break
    '''

#-----------------------------------------------------------------------------------------------------------



    #print("================== -- Subclass -- =======================")
    '''
    output = open("File/{0}/{0}_SubClass.txt".format(fname), 'w', encoding='utf-8')
    for id, value in o.SuperClassOf.items():
        if(len(value)>=1):
            for eachValue in value:
                data = "Class: {0} ==> SubClass: {1}".format(id, eachValue)
                output.write(data + '\n')
                print(data)
        else:
            if len(value)==0:
                data = "Class: {0} ==> SubClass: NULL".format(id)
                output.write(data + '\n')
                print(data)
            else:
                for eachValue in value:
                    data = "Class: {0} ==> SubClass: {1}".format(id, eachValue)
                    output.write(data + '\n')
                    print(data)
    output.close()
    print("Done!")
    print("====================================== -- Superclass -- ===============================================")
    output = open("File/{0}/{0}_SuperClass_1.txt".format(fname), 'w', encoding='utf-8')
    for id, value in o.SubClassOf.items():
        for eachValue in value:
            data = "Class {0} ==> FatherClass: {1}".format(id, eachValue)
            print(data)
            output.write(data + '\n')
    output.close()
    print("Done!")
    '''

    '''
    print("====================================== -- Classes -- ===============================================")
    #for  value in o.Classes:
    #    print(value)
    output = open("File/{0}/{0}_Classes.txt".format(fname), 'w', encoding='utf-8')
    for val in o.Classes:
        data = "Concept: {0}".format(val)
        print(data)
        output.write(data + '\n')
    output.close()
    print("Done!")
    print("====================================== -- Individuals -- ===============================================")
    output = open("File/{0}/{0}_Individual.txt".format(fname), 'w', encoding='utf-8')
    for value in o.NamedIndividuals:
        data = "Instance: {0}".format(value)
        print(data)
        output.write(data + '\n')
    output.close()
    print("Done!")
    print("====================================== -- ObjectProperty or Roles or Relations -- =====================")
    output = open("File/{0}/{0}_ObjectProperty.txt".format(fname), 'w', encoding='utf-8')
    if(len(o.ObjectProperties)==0):
        print("ObjectProperty is Empty!")
        output.write("Object Property is empty" + '\n')
    else:
        for value in o.ObjectProperties:
            data = "Object Property: {0}".format(value)
            print(data)
            output.write(data + '\n')
    output.close()
    print("Done!")
    print("====================================== -- Domain of ObjectProperty -- =====================")
    output = open("File/{0}/{0}_Subject-Predicate-Object.txt".format(fname), 'w', encoding='utf-8')

    for id, value in o.ObjectPropertyDomain.items():
        if len(value)>0:
            for eachValue in value:
                data = "Role: {0} - Concept(Subject): {1}".format(id, eachValue)
                print(data)
                output.write(data + '\n')
    for id, value in o.ObjectPropertyRange.items():
        if len(value)>0:
            for eachValue in value:
                data = "Role: {0} - Concept(Object): {1}".format(id, eachValue)
                print(data)
                output.write(data + '\n')
    output.close()
    print("Done!")


    print("====================================== -- DataProperty -- =====================")
    output = open("File/{0}/{0}_DataProperty.txt".format(fname), 'w', encoding='utf-8')
    if (len(o.DataProperties) == 0):
        print("Data Property is Empty!")
        output.write("Data Property is empty" + '\n')
    else:
        for value in o.DataProperties:
            data = "Object Property (Role): {0}".format(value)
            print(data)
            output.write(data + '\n')
    output.close()
    print("Done!")
    print("==================================== -- Class and Individual -- =====================")
    output = open("File/{0}/{0}_ClassIndividual.txt".format(fname), 'w', encoding='utf-8')
    for id, value in o.ClassIndividual.items():
        for eachValue in value:
            for e in eachValue:
                print("Concept: ",id, "==> Instance: ", e)
                data = "Concept:{0}  ==>  Instance: {1}".format(id, e)
                output.write(data + '\n')
    output.close()
    print("Done!")
    print("==================================== -- Class and Annotation -- =====================")
    output = open("File/{0}/{0}_AnnotationClass.txt".format(fname), 'w', encoding='utf-8')
    for id, value in o.AnnotationClass.items():
        for eachValue in value:
            data = "Concept:{0}  ==>  Annotation: {1}".format(id, eachValue)
            print(data)
            output.write(data + '\n')
    output.close()
    print("Done!")

    print("==================================== -- Individual and Annotation -- =====================")
    output = open("File/{0}/{0}_AnnotationIndividual.txt".format(fname), 'w', encoding='utf-8')
    for id, value in o.AnnotationIndividual.items():
        for eachValue in value:
            data = "Concept:{0}  ==>  Annotation: {1}".format(id, eachValue)
            print(data)
            output.write(data + '\n')
    output.close()
    print("Done!")
    
    print("==================================== --------Get Wordnet of SUMO----------------- =====================")
    output = open("File/{0}/{0}_WORDNETSUMO.txt".format(fname), 'w', encoding='utf-8')
    for id, value in o.AnnotationClass.items():
        for eachValue in value:
            if "wn#" in "{0}".format(eachValue):
                data = "Concept:{0}  ==>  Annotation: {1}".format(id, eachValue)
                print(data)
                output.write(data + '\n')
    for id, value in o.AnnotationIndividual.items():
        for eachValue in value:
            if "wn#" in "{0}".format(eachValue):
                data = "Individual:{0}  ==>  Annotation: {1}".format(id, eachValue)
                print(data)
                output.write(data + '\n')
    output.close()
    print("Done!")
    '''
    #---------------------------------------------------------------------------------------
    '''
    print("==================================== -- Individual and Annotation -- =====================")
    output = open("File/{0}/{0}_AnnotationIndividual_1.txt".format(fname), 'w', encoding='utf-8')
    for id, value in o.AnnotationIndividual.items():
        for eachValue in value:
            data = "Individual:{0}  ==>  Annotation: {1}".format(id, eachValue)
            print(data)
            if "WN30-" in "{0}".format(eachValue):
                print("Save:",data)
                output.write(data + '\n')
    output.close()
    print("Done!")
    print("==================================== -- Class and Individual -- =====================")
    output = open("File/{0}/{0}_ClassIndividual_1.txt".format(fname), 'w', encoding='utf-8')
    for id, value in o.ClassIndividual.items():
        for eachValue in value:
            for e in eachValue:
                data = "Concept:{0}  ==>  Instance: {1}".format(id, e)
                print(data)
                if "WN30-" in "{0}".format(e):
                    print("Save:",data)
                    output.write(data + '\n')
    output.close()
    print("Done!")
    '''

