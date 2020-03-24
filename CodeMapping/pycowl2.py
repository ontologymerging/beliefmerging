# -*- coding: utf-8 -*-
import os
import os.path
import gzip
import json
import jmespath
import time
import rdflib

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


def PrintList(object_list):
    for i in object_list.items():
        print(i)

def writeFile_items(Filename, object_list):
    output = open(Filename, 'w', encoding='utf-8')
    for key,val in  object_list.items():
        data = "{0} ==> {1}".format(key,val)
        print(data)
        output.write(data + '\n')
    output.close()
    print("{0} is done!".format(Filename))


#nameFile="C:\\Code\\powl1\\dataset\\baseball.owl"
#nameFile="C:\\Code\\powl1\\dataset\\Product.owl"
nameFile="C:\\Code\\powl1\\dataset\\SUMO.owl"
#nameFile="C:\\Code\\powl1\\dataset\\Shopping.owl"
#nameFile="C:\\Code\\powl1\\dataset\\WordNet.owl"
#nameFile="C:\\Code\\powl1\\dataset\\dbpedia.owl"
o = Ontology(nameFile)

if __name__ == "__main__":

    '''------------------------------------ URI and file name---------------------------------'''
    print("\nLink:",o.URI," --> Result: " ,o.URI is o.info.URI)
    fname = str(nameFile).split('\\')[-1:][0].split(".")[0]

    '''------------------------------------ Directory to store the storage files---------------------------------'''
    directory="File/{0}/".format(fname)
    if not os.path.exists(directory):
        os.makedirs(directory)

    print("====================================== -- Subclass -- ===============================================")

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
    output = open("File/{0}/{0}_SuperClass.txt".format(fname), 'w', encoding='utf-8')
    for id, value in o.SubClassOf.items():
        for eachValue in value:
            data = "Class {0} ==> FatherClass: {1}".format(id, eachValue)
            print(data)
            output.write(data + '\n')
    output.close()
    print("Done!")
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
            data = "Individual:{0}  ==>  Annotation: {1}".format(id, eachValue)
            print(data)
            output.write(data + '\n')
    output.close()
    print("Done!")
    print("==================================== --------Get Wordnet of SUMO----------------- =====================")
    for id, value in o.AnnotationIndividual.items():
        for eachValue in value:
            if "wn" in eachValue:
                data = "Individual:{0}  ==>  Annotation: {1}".format(id, eachValue)
                print(data)
    print("Done!")
'''
    print()

    #print(o.SubClassOf["City"])
    #print(o.SuperClassOf["City"])
    print("classes", o.Classes)
    print()
    print("subclasses", o.SubClassOf)
    # "Country" in o.SubClassOf["City"]
    print()
    print("objectProperties", o.ObjectProperties)
    print()
    # print([c for c in o.Classes if "City" in o.SubClassOf[c]])
    print("City" in o.Classes)
    print()
    print("equivalentClasses", o.EquivalentClasses)
    print()
    print("disjointClasses", o.DisjointClasses)
    print()
    #print("subObjectProperty", o.SubObjectPropertyOf)
    print("objectPropertyDomain", o.ObjectPropertyDomain)
    print()
    print("objectPropertyRange", o.ObjectPropertyRange)
    print()
    #print("classAssertion", o.ClassAssertion)
    #print("type", o.Type)
    print("namedIndividuals", o.NamedIndividuals)
    print()
    #print("objectPropertyAssertion", o.ObjectPropertyAssertion)
    print("functionalObjectProperty", o.FunctionalObjectProperty)
    print()
    print(o.Classes)
    print()
    print(o.URI)
'''