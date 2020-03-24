#!/bin/bash
clear
pushd java1
mvn package -e
popd
java -jar java1/target/owlapi-generator-1.0.1.jar

