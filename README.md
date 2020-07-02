# Belief Merging
## Belief Merging in Open-Domain Ontologies
Our ontology merging application tool focuses on handling the conflicts in which the open-domain sources consider the same concept but expressing the knowledge differently. The input of the tool is open-domain ontologies and the output is a merged result between the sources. We implemented the tool in three sources including: SUMO, Wikidata and Babelnet. Namely, we first collected a mapping between three sources to perform a common name synchronizing process. Finally, we utilized the fundamental theory of belief merging to apply ontology merging. We also identified the most plausible interpretation corresponding a merged syntactic as the ontology merging result of our tool.

How to run the Ontology Merging application:
```
python3 Tool.py
```

## Mapping:

![Test Image 1](Images/Mapping.png)


## An interface of the application:

<img src="https://github.com/ontologymerging/beliefmerging/blob/master/Images/Application.png" width="700"/>


Choose concepts to merge from three sources (SUMO, WIKIDATA, BABELNET)

![Test Image 5](Images/SUMO_WIKIDATA_BABELNET.png)

## Some examples:


### Example: Seafood, Shellfish, Shrimp

![Test Image 4](Images/Example_Application.png)

### Example: Stone, Rock, Gravel

![Test Image 3](Images/Example2.png)

### Example: Book, Text and Thing (TOP)

![Test Image 6](Images/Example_Book1.png)

### Example: Book, Text, Document

![Test Image 7](Images/Example_Book2.png)

### Example: Region, LandForm, Valley

![Test Image 10](Images/Example_Region.png)




