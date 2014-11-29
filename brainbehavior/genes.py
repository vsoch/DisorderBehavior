#!/usr/bin/env python

"""

Genes: part of the brainbehavior python package

BrainBehavior: This module will work with three databases that 
combined can make inferences about disorders and behaviors:

NeuroVault: functional and structural group analyses
Cognitive Atlas: ontology of cognitive concepts, tasks, disorder, collections
NeuroSynth: mining literature for behavioral concepts to produce brain maps

SAMPLE USAGE: Please see README included with package


"""

import numpy as np
import re
import sys
import os.path
import pandas as pd
import os
import pickle

__author__ = ["Vanessa Sochat (vsochat@stanford.edu)"]
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2011/09/09 $"
__license__ = "Python"

# Genes 
# These functions will work with genes! Currently very simple - just
# genes for 86 mala cards defined "mental" disorders from phenotype
class Genes:

  """Init Genes Object"""
  def __init__(self):
    self.genes = self._get_genes()

  """Read in gene pickle file, should be dictionary"""
  def _get_genes(self,gene_file=None):
    if not gene_file:
      cwd = os.path.dirname(os.path.realpath(__file__))
      gene_file = "%s/data/genes/mental_disorder_mala_phenopedia.pkl" %(cwd)
    return pickle.load(open(gene_file,"rb"))

  """Get all unique genes in database"""  
  def get_unique_genes(self):
    all_genes = []
    for disorder,genes in self.genes.iteritems():
      all_genes = all_genes + genes
    all_genes = np.unique(all_genes)
    return all_genes
