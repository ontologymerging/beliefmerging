# PYCOWL

This is **pycowl**, an ontology-management library for python developers.

It is currently under development at the [CRIL](https://www.cril.univ-artois.fr/).

It is based on the owlapi Java library.

## Dependencies

To install and use pycowl, you will need at least the following:

- [Python](https://www.pythn.org) version 3.7 or higher,
- [Java](https://www.java.com) version 11 or higher,
- The [Maven build automation tool](https://maven.apache.org/).

## Installation

To install pycowl, you first need to install the java to python gateway,
that will make the connection between owlapi and pycowl.

To do so, just go to the java directory and run

    mvn package

This will download and install all the java dependencies.

Once everything is downloaded and installed, just run:

    java -jar target/owlapi-generator.jar

Now the gateway will be started.