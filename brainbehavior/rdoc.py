#!/usr/bin/env python

"""

rdoc: part of the brainbehavior python package to work with rdoc matrix

BrainBehavior: This module will work with three databases that 
combined can make inferences about disorders and behaviors:

NeuroVault: functional and structural group analyses
Cognitive Atlas: ontology of cognitive concepts, tasks, disorder, collections
NeuroSynth: mining literature for behavioral concepts to produce brain maps

SAMPLE USAGE: Please see README included with package

rdoc:   Methods for working with on and offline pubmed data
       .get_xml_text:  Get raw text from pubmed xml file.  Uses:
       ._recursiveTextExtract: pull text from all xml elements
       .get_construct: 
       .find_construct: Searches for rdoc features in paper
       .extract_sentences: return dictionary ["methodname","sentence it's in!'"]

"""

import re
from pubmed import extract_xml_compressed, read_xml, recursive_text_extract, get_xml_tree
from lxml import etree
import pandas as pd
import tarfile
import os

__author__ = ["Vanessa Sochat (vsochat@stanford.edu)"]
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2011/09/09 $"
__license__ = "Python"


# RDoC ---------------------------------------------------------------------------
class rdoc:

    '''Construct file should be tab separated with the following fields
    ID\tUNIT\tFEATURE\tDOMAIN\tCONSTRUCT\tSUBCONSTRUCT\tSEARCHTERM'''
    def __init__(self,construct_file="data/rdoc/negative_valence.csv"):
      self.construct_file = construct_file
      self.read_construct() 

    '''Read in rdoc construct matrix'''
    def read_construct(self):
      self.features = pd.read_csv(self.construct_file,sep="\t")

    '''Extract construct will determine filetype (xml or tar.gz) for one or more files and extract appropraitely'''
    def extract_construct(self,papers):
    
      # Let's create a data frame to hold the featres
      feature_matrix = pd.DataFrame(columns=self.features["ID"])
      matches_matrix = pd.DataFrame(columns=self.features["ID"])
      pmids = []

      for paper in papers:
        # If there is an error with a paper, we don't want it to 
        # end the whole process! Just don't add it.
        try:
          raw = get_xml_tree(paper)           
          data = etree.XML(raw)

          # For now, parse the entire article - may want to eventually limit scope
          # Get text - recursively go through elements
          parsed = recursive_text_extract(data)
          pmid = parsed[0]      
          text = parsed[1]
          pmids.append(pmid)

          # Now extract construct features from text
          hits = self.search_for_features(text)
          scores = hits[0]  # list
          matches = hits[1] # dict
          feature_matrix.loc[feature_matrix.shape[0]] = scores
          matches_matrix.loc[matches_matrix.shape[0]] = matches.values() 
        except:
          print "XML parsing error with paper %s" % (paper)
        
      # Add pmid to matrices
      feature_matrix["PMID"] = pmids
      matches_matrix["PMID"] = pmids
      result = {"features":feature_matrix,"matches":matches_matrix}
      return result

    '''Match features to sentences in the xml text'''
    def search_for_features(self,text):
      matches = dict()
      # Make a list to hold text matches and scores
      scores = []
      print "Searching article for construct features..."
      fulltext = " ".join(text).lower()
      
      for f in self.features.iterrows():
        matchlist = list()
        feature = f[1]["SEARCHTERM"].lower()
        feature_id = f[1]["ID"]
        expression = re.compile(feature)
        match = expression.search(fulltext)
        if match:
          print "Found match for " + f[1]["SEARCHTERM"] + "!"
          # Extract the gist - 10 words before and after
          start = match.start() - 100
          end = match.start() + 100
          if start < 0: start = 0
          if end > len(fulltext): end = len(fulltext)
          matchlist.append(fulltext[start:end].encode('utf-8'))
        matches[feature_id] = "|".join(matchlist)
        # We will just append a raw count for now - should probably normalize by
        # the length of the article, etc.
        scores.append(len(matchlist))
      return (scores,matches)  
      

# MAIN ----------------------------------------------------------------------------------
def main():
    print __doc__

'''Parse RDoC results into pickle and csv files'''
def parse_pickle_results(rdoc_files,output_file_prefix):
  
  # Sort the files by name
  rdoc_files.sort()  

  # Create the initial data frames from the first result
  tmp = pickle.load(open(rdoc_files.pop(0),"rb"))
  if any([x in tmp.keys() for x in ["features","matches"]]) == False:
    print "Error: file does not match rdoc expectation: should be dictionary with 'matches' and 'features' as keys!"
  else
    # We need a matrix for results, and for the matches
    match_matrix = tmp["matches"]
    score_matrix = tmp["features"]
    # Now iterate over results, add to matrix
    for r in range(0,len(rdoc_files)):
      print "Parsing file %s of %s" % (r,len(rdoc_files))
      rdoc_file = rdoc_files[r]
      tmp = pickle.load(open(rdoc_file,"rb"))
      match_matrix = match_matrix.append(tmp["matches"])
      score_matrix = score_matrix.append(tmp["features"])
    # Write to pickle, and to text file (dangerous?)
    print "Saving results as pickle and csv/tsv with prefix %s." output_file_prefix
    match_matrix.to_pickle("%s_matches.pkl" % output_file_prefix)
    score_matrix.to_pickle("%s_features.pkl" % output_file_prefix)
    match_matrix.to_csv("%s_matches.pkl" % output_file_prefix,sep="\t",index_label="PMID")
    score_matrix.to_csv("%s_features.csv" % output_file_prefix, index_label="PMID")


if __name__ == "__main__":
    main()
