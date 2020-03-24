package fr.cril.pycowl;

import java.io.File;
import java.util.Iterator;

import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyCreationException;
import org.semanticweb.owlapi.model.OWLOntologyManager;
import org.semanticweb.owlapi.reasoner.OWLReasonerFactory;
import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.structural.StructuralReasonerFactory;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.model.OWLEntity;
import org.semanticweb.owlapi.search.EntitySearcher;

import it.uniroma1.lcl.babelnet.BabelNet;
import it.uniroma1.lcl.babelnet.*;
import it.uniroma1.lcl.babelnet.WordNetSynsetID;
import java.io.IOException;
import py4j.GatewayServer;

public class Main {
    private final OWLOntologyManager manager;

    public Main() {
        manager = OWLManager.createOWLOntologyManager();
    }

    public Ontology loadOntology(String path) throws OWLOntologyCreationException {
        return new Ontology(manager, path);
    }

    public OWLOntology loadOWLOntology(String path) throws OWLOntologyCreationException {
        final File f = new File(path);
        manager.clearOntologies();
        final OWLOntology onto = manager.loadOntologyFromOntologyDocument(f);
        onto.subClassAxiomsForSubClass(null);
        return onto;
    }
    //add this method to support for reasoning - date/time: 15h12  29/11/2019
    public OWLReasoner loadReasoner(OWLOntology myOntology)  {
        OWLReasonerFactory reasonerFactory = new StructuralReasonerFactory();
        OWLReasoner reasoner = reasonerFactory.createReasoner(myOntology);
        return reasoner;
    }
    //add this method to support for getting annotation of each concept - date/time: 08h48  02/12/2019
    public Iterator<OWLAnnotation> loadAnnotationEntity(OWLEntity entity, OWLOntology myOntology)
    {
        final Iterator<OWLAnnotation> iterator = EntitySearcher.getAnnotations(entity, myOntology).iterator();
        return iterator;
    }
    //BabelnetAPI

    public void loadBabelNet_WordNet(String idWN) throws IOException {
        BabelNet bn = BabelNet.getInstance();
        //bn.getSynset(new BabelSynsetID("bn:00000356n")).getSenses();
        //BabelSynset by =
        //return bn;
    }
    public static void main(String[] args) {
        final GatewayServer gatewayServer = new GatewayServer(new Main());
        gatewayServer.start();
        System.out.println("Gateway Server Started");
    }
}