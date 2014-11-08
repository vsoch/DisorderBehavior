#!/usr/bin/env python2

# This script will use the BrainBehavior.py module to search for disorder terms in
# NeuroSynth abstracts, and return a matrix of disorder ids (columns) by papers (rows)
# with "1" indicating that a disorder term was found, and "0" not.

import brainbehavior.cognitiveatlas
import brainbehavior.neurosynth
import brainbehavior.pubmed

# Create a CognitiveAtlas object, get disorders
ca = CognitiveAtlas()
disorders = ca.disorders

# Create a NeuroSynth Object to get all Ids
ns = NeuroSynth(8000)
ids = ns.ids
# or just load from file
#import pickle
#ids = pickle.load( open( "data/8000terms/nsids.pkl", "rb" ) )

# Create a pubmed object to query pubmed
email = "vsochat@stanford.edu"
pub = Pubmed(email)
articles = dict()
for i in ids:
  if i not in articles.keys():
    articles[i] = pub.getArticle(i)
# Or again, load from file, faster
# articles = pickle.load( open( "data/8000terms/articles.pkl", "rb" ) )

# Here are column labels, the disorder ids
cols = []
for d,v in disorders.iteritems():
  cols.append(d)

# Sanity check: ids[3] is Alzheimer's disease'

# For each article, search for terms!
results = []
rows = ids
for aa in range(0,len(ids)):
  matches = []
  a = articles[ids[aa]]
  print "Creating matrix for article " + str(aa) + " of " + str(len(ids))
  for d,v in disorders.iteritems():
    matches.append(pub.searchArticle(a,v))
  results.append(matches)

# Column names are the article pmids
# Row names are the disorder ids

# Write table to file
outfile = "output/disorder_pid_matrix.v3.txt"
filey = open(outfile,'w')
filey.writelines( "ID\t"+ "\t".join(cols) + "\n")
for r in range(0,len(results)):
  filey.writelines(rows[r] + "\t" + "\t".join([str(x) for x in results[r]]) + "\n")

filey.close()
