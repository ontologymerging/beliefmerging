import rdflib

from py4j.java_gateway import JavaGateway

gateway = JavaGateway()

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
        self.onto = rdflib.Graph()
        self.onto.load(path)
        all_uris = [s for s, p, o in self.onto if str(p) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" and str(o) == "http://www.w3.org/2002/07/owl#Ontology"]
        # There should be only one URI
        self.URI = all_uris[0]
        self.Classes = {s for s, _, o in self.onto if str(o) == "http://www.w3.org/2002/07/owl#Class"}
        self.ObjectProperties = {s for s, _, o in self.onto if str(o) == "http://www.w3.org/2002/07/owl#ObjectProperty"}
        self.NamedIndividuals = {s for s, _, o in self.onto if str(o) == "http://www.w3.org/2002/07/owl#NamedIndividual"}
        self.info = OntologyInfo(self)
        self.term = OntologyTerminology(self)
        self.facts = OntologyFacts(self)
    
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
    
    def _SubClassOf(self):
        self.SubClassOf = {}
        for s, p, o in self.onto:
            if str(p) == "http://www.w3.org/2000/01/rdf-schema#subClassOf":
                if s not in self.SubClassOf:
                    self.SubClassOf[s] = [o]
                else:
                    self.SubClassOf[s].append(o)
        self.SubClassOf = RdfDict(self.SubClassOf)
        return self.SubClassOf
    
    def _SuperClassOf(self):
        self.SuperClassOf = {}
        for s, p, o in self.onto:
            if str(p) == "http://www.w3.org/2000/01/rdf-schema#subClassOf":
                if o not in self.SuperClassOf:
                    self.SuperClassOf[o] = [s]
                else:
                    self.SuperClassOf[o].append(s)
        self.SuperClassOf = RdfDict(self.SuperClassOf)
        return self.SuperClassOf
    
    def _EquivalentClasses(self):
        self.EquivalentClasses = {}
        for s, p, o in self.onto:
            if str(p) == "http://www.w3.org/2002/07/owl#equivalentClass":
                if s not in self.EquivalentClasses:
                    self.EquivalentClasses[s] = [o]
                else:
                    self.EquivalentClasses[s].append(o)
        self.EquivalentClasses = RdfDict(self.EquivalentClasses)
        return self.EquivalentClasses
    
    def _DisjointClasses(self):
        self.DisjointClasses = {}
        for s, p, o in self.onto:
            if str(p) == "http://www.w3.org/2002/07/owl#disjointWith":
                if s not in self.DisjointClasses:
                    self.DisjointClasses[s] = [o]
                else:
                    self.DisjointClasses[s].append(o)
        self.DisjointClasses = RdfDict(self.DisjointClasses)
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
        for s, p, o in self.onto:
            if str(p) == "http://www.w3.org/2000/01/rdf-schema#domain":
                if s not in self.ObjectPropertyDomain:
                    self.ObjectPropertyDomain[s] = [o]
                else:
                    self.ObjectPropertyDomain[s].append(o)
        self.ObjectPropertyDomain = RdfDict(self.ObjectPropertyDomain)
        return self.ObjectPropertyDomain
    
    def _ObjectPropertyRange(self):
        self.ObjectPropertyRange = {}
        for s, p, o in self.onto:
            if str(p) == "http://www.w3.org/2000/01/rdf-schema#range":
                if s not in self.ObjectPropertyRange:
                    self.ObjectPropertyRange[s] = [o]
                else:
                    self.ObjectPropertyRange[s].append(o)
        self.ObjectPropertyRange = RdfDict(self.ObjectPropertyRange)
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
        for s, p, o in self.onto:
            if str(p) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" and str(o) == "http://www.w3.org/2002/07/owl#FunctionalProperty":
                self.FunctionalObjectProperty.add(s)
        return self.FunctionalObjectProperty

def PrintList(object_list):
    for i in object_list.items():
        print(i)

def writeFile(Filename, object_list):
    output = open(Filename, 'w', encoding='utf-8')
    for key,val in  object_list.items():
        data = "{0} ==> {1}".format(key,val)
        print(data)
        output.write(data + '\n')
    output.close()
    print("{0} is done!".format(Filename))

#o = Ontology("SUMO.owl")

o = Ontology("C:\\Code\\powl1\\dataset\\wikidata.xml.bz2")
print(o.URI, o.URI is o.info.URI)
#writeFile("File/SubClass1.txt", o.term.SubClassOf)
#writeFile("File/SuperClass1.txt", o.SuperClassOf)
#print("subClassOf", o.term.SubClassOf)
print("============================================================================================================")
print("superClassOf", o.SuperClassOf)
print()
#for i in o.SuperClassOf.short.items():
#    print(i)
'''
print(o.SubClassOf["City"])
print(o.SuperClassOf["City"])
print("classes", o.Classes)
print("objectProperties", o.ObjectProperties)
# print([c for c in o.Classes if "City" in o.SubClassOf[c]])
print("City" in o.Classes)
print("equivalentClasses", o.EquivalentClasses)
print("disjointClasses", o.DisjointClasses)
print("subObjectProperty", o.SubObjectPropertyOf)
print("objectPropertyDomain", o.ObjectPropertyDomain)
print("objectPropertyRange", o.ObjectPropertyRange)
print("classAssertion", o.ClassAssertion)
print("type", o.Type)
print("namedIndividuals", o.NamedIndividuals)
print("objectPropertyAssertion", o.ObjectPropertyAssertion)
print("functionalObjectProperty", o.FunctionalObjectProperty)
'''