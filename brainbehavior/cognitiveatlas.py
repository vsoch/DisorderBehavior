#!/usr/bin/env python

"""

CognitiveAtlas: part of the brainbehavior python package

BrainBehavior: This module will work with three databases that 
combined can make inferences about disorders and behaviors:

NeuroVault: functional and structural group analyses
Cognitive Atlas: ontology of cognitive concepts, tasks, disorder, collections
NeuroSynth: mining literature for behavioral concepts to produce brain maps

SAMPLE USAGE: Please see README included with package


"""

import pickle

__author__ = ["Vanessa Sochat (vsochat@stanford.edu)","Matthew Sacchet (msacchet@stanford.edu)"]
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2011/09/09 $"
__license__ = "Python"

# Cognitive Atlas Functions---------------------------------------------------------
class CognitiveAtlas:

  # In future we should download rdf, and get from there!
  def __init__(self):
    print "Reading Cognitive Atlas disorders..."
    self.disorders = self.loadDisorders()

  """Read in file of local disorders to create pickle object"""
  def readLocalDisorder(self):
    import pickle
    filey = open("data/disorder_subset_10-31-14.csv","r")
    disorders = filey.readlines()
    filey.close()
    header = disorders.pop(0).strip("\n").strip("\r").strip(" ").split(",")
    disorder = dict()
    for d in disorders:
      tmp = d.strip("\n").strip("\r").strip("'").strip('"').split("\t")
      did = tmp.pop(0).strip('"')
      # Here are the search terms
      labels = tmp[2].strip('"')
      disorder[did] = labels
    # Save to pickle object
    pickle.dump(disorder, open( "data/CAdisorders.pkl", "wb" ) )
      
  def loadDisorders(self):
    import pickle
    return pickle.load( open( "data/CAdisorders.pkl", "rb" ) )

