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

//-------------  BabelNet  --------------------
import it.uniroma1.lcl.babelnet.BabelNet;
import it.uniroma1.lcl.babelnet.BabelNetQuery;
import it.uniroma1.lcl.babelnet.BabelNetUtils;
import it.uniroma1.lcl.babelnet.BabelSense;
import it.uniroma1.lcl.babelnet.BabelSenseComparator;
import it.uniroma1.lcl.babelnet.BabelSynset;
import it.uniroma1.lcl.babelnet.BabelSynsetComparator;
import it.uniroma1.lcl.babelnet.BabelSynsetID;
import it.uniroma1.lcl.babelnet.BabelSynsetRelation;
import it.uniroma1.lcl.babelnet.InvalidSynsetIDException;
import it.uniroma1.lcl.babelnet.data.BabelGloss;
import it.uniroma1.lcl.babelnet.data.BabelImage;
import it.uniroma1.lcl.babelnet.data.BabelSenseSource;
import it.uniroma1.lcl.jlt.util.Language;
import it.uniroma1.lcl.jlt.util.ScoredItem;
import it.uniroma1.lcl.jlt.wordnet.WordNetVersion;
import it.uniroma1.lcl.babelnet.*;
import static java.util.stream.Collectors.toList;

import it.uniroma1.lcl.babelnet.BabelNetConfiguration;
//-----------------------------------------------
import java.io.IOException;
import py4j.GatewayServer;
//-------------------------------------------
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVPrinter;
import org.apache.commons.csv.CSVRecord;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.stream.Collectors;


import static java.util.stream.Collectors.toList;

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

    public  String loadBabelNet_WordNet(String input) throws IOException {
	        
	final BabelNetConfiguration config = BabelNetConfiguration.getInstance();
        config.setConfigurationFile(new File("/home/thanhma/Documents/Code/powl/config/babelnet.properties"));
        final BabelNet bn = BabelNet.getInstance();
	
        BabelSynset _synSetWordNet = bn.getSynset(new WordNetSynsetID(input));
        String fileContent="";
        for (BabelSense sense : _synSetWordNet.getSenses(BabelSenseSource.WIKIDATA)) {
            String sensekey = sense.getSensekey();
            if(Objects.equals(sense.getLanguage().toString(),"EN"))
            {
                fileContent= "BabelNet: "+sense.getFullLemma() + "\t - " + "WIKIDATA:" + sensekey    ;
		break;
            }
        }
        return  fileContent;
    }
	public  List<String> loadBabelNet_Words(String input) throws IOException {
	
		final BabelNetConfiguration config = BabelNetConfiguration.getInstance();
        config.setConfigurationFile(new File("/home/thanhma/Documents/Code/powl/config/babelnet.properties"));
        final BabelNet bn = BabelNet.getInstance();
		List<String> fileContent = new ArrayList<String>();
		BabelNetQuery query = new BabelNetQuery.Builder(input).from(Language.EN).build();
		int k=0;
       
		for(BabelSynset byl : bn.getSynsets(query))
		{
			BabelSynset by = bn.getSynset(new BabelSynsetID(byl.getID().toString()));
			for (BabelSense sense : by.getSenses(BabelSenseSource.WIKIDATA)) {
				if(Objects.equals(sense.getLanguage().toString(),"EN"))
				{
					k=k+1;
					String sensekey = sense.getSensekey();
					fileContent.add(byl.getID() + " - "+ sense.getFullLemma()  + "- WIKIDATA:" + sensekey);				
					//System.out.println(fileContent);
					break;
				}
			}
		}
		return	 fileContent;
	}    

    public static void main(String[] args) {
        final GatewayServer gatewayServer = new GatewayServer(new Main());
        gatewayServer.start();
        System.out.println("Gateway Server Started");
    }
}
