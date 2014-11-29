#!/usr/bin/env python2

# This script will use the BrainBehavior.py modules to parse full next NeuroSynth articles for phenopedia defined genes.  We will then have a matrix of genes by papers, and we can see how this maps onto rdoc, or try neurosynth meta analysis.  Ultimately I want to look carefully at what the gene (should be) doing in the region, and try to pinpoint timepoints that are important to map disorders to.

import brainbehavior.neurosyn
import brainbehavior.genes as gen
import numpy as np
import re
import glob
import pandas as pd
from lxml import etree
from brainbehavior.pubmed import get_xml_tree, recursive_text_extract, search_text

# Select papers from download directory
papers_directory = "/home/vanessa/Documents/Work/PUBMED"
targz = glob.glob(papers_directory + "/*.tar.gz")

# Create genes object and get unique genes
genes = gen.Genes()
genelist = genes.get_unique_genes()

# Here we will hold a matrix of pmids by genes
genematrix = pd.DataFrame(columns=genelist)

# For each targz file, get the text
pmids = []
for t in range(212,len(targz)):
  tar = targz[t]
  try:
    tree = get_xml_tree(tar)
    data = etree.XML(tree)
    text = recursive_text_extract(data)
    pmid = text[0]
    pmids.append(pmid)
    text = text[1]
    dump = " ".join(text)
    # Search the dump for the genes
    vector =  search_text(dump,genelist)
    genematrix.loc[genematrix.shape[0]] = vector
  except:
    print "skipping %s" %(tar)


# Add the pmids!
genematrix.to_pickle("brainbehavior/data/genes/nsynth_genes.pkl")
genematrix["PMID"] = pmids
genematrix.to_pickle("brainbehavior/data/genes/nsynth_genes.pkl")
genematrix.to_csv("brainbehavior/data/gene/nsynth_genes.tsv",sep="\t")
