package fr.cril.pycowl;

import java.io.File;

import org.semanticweb.owlapi.model.OWLOntologyManager;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyCreationException;

public class Ontology {
    private OWLOntology ontology;

    public Ontology(OWLOntologyManager manager, String path) throws OWLOntologyCreationException {
        File f = new File(path);
        ontology = manager.loadOntologyFromOntologyDocument(f);
    }

    public Object[] axioms() {
        return ontology.axioms().toArray();
    }

    public Object[] generalClassAxioms() {
        return ontology.generalClassAxioms().toArray();
    }

    public Object[] classesInSignature() {
        return ontology.classesInSignature().toArray();
    }
}