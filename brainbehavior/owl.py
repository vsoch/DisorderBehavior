#!/usr/bin/env python2

"""

owl: part of the brainbehavior python package for working with ontology owl files

BrainBehavior: This module will work with three databases that 
combined can make inferences about disorders and behaviors:

NeuroVault: functional and structural group analyses
Cognitive Atlas: ontology of cognitive concepts, tasks, disorder, collections
NeuroSynth: mining literature for behavioral concepts to produce brain maps

Owl:   Protege output (owl files)
       ._read_ontology:   Read in methods from ontology (owl) file
       .get_ontology:     Return list of classes
       ._parse_ontology:  Returns list of classes with alternate terms

SAMPLE USAGE: Please see README included with package


"""


# Owl------------------------------------------------------------------------------
class Owl:
    def __init__(self,infile):
        self.file = infile  # name of the owl input file
        self.rawmethod = self._read_ontology()
        self.methods = self._parse_ontology()

    ''' Return raw list of classes'''
    def get_classes():
      return self.methods

    ''' Read methods from owl file - no spaces'''
    def _read_ontology(self):
      methods = []
      filey = open(self.file,"r")
      filey = filey.readlines()
      islabel = re.compile("^<rdfs:label>*")
      # The method names will not have http
      for line in filey:
        line = line.replace(" ","").replace("\n","")
        if islabel.match(line):
          method = line.replace("<rdfs:label>","").replace(" ","").replace("</rdfs:label>","")
          methods.append(method)
      return methods

    '''Return dictionary of methods with alternate terms'''
    def _parse_ontology(self):
      methods = []
      # TODO: we should add the "searchable term" as a field in ontology?

      # Add spaces to methods - return in list
      # TODO: return in dict with alternate terms
      for m in self.rawmethod:
        # add a space to capital letters
        capitals = [c for c, (letter) in enumerate(m) if letter.isupper()]
        tmp = []
        for c in capitals:
          tmp.append(m[:c] + " ")
        tmp.append(m[c:len(m)])
        tmp = ''.join(tmp).strip().lower()
        methods.append(tmp)
      
      # TODO: Debug why the first methods in the list are single letters
      # For now get rid of them!
      methods = [m for m in methods if len(m) > 1]
      return methods
      # TODO: Use JMort method to look up alternative terms for each

