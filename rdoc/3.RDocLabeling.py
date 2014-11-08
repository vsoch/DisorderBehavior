#!/usr/bin/env python2

# This script will read in the RDoC matrix, NeuroSynth ids, and attempt to search for the terms in the abstract.  Each paper will have a vector of features to assess the probability
# of a paper belonging to a particular concept group.

import pubmed as pm

# First we need to download full article text
# Create a pubmed object
email = "vsochat@stanford.edu"
pub = pm.Pubmed(email)
pub.loadPubmed()

# Get our list of ids for each disorder
filey = open("data/disorder_pid_groups_thresh15.v3.txt","r")
groups = dict()
for f in filey.readlines():
  group = f.strip("\n").split("\t")
  name = group.pop(0)
  groups[name] = group

filey.close()

# If we need to download the articles
allpmids = []
for g,pmids in groups.iteritems():
  allpmids = allpmids + pmids

# Download the articles
pub.downloadFull(allpmids)

# Create a CognitiveAtlas object, get disorders
ca = BB.CognitiveAtlas()
disorders = ca.disorders

# Create a NeuroSynth Object to get all Ids
ns = BB.NeuroSynth(8000)
ids = ns.ids
# or just load from file
#import pickle
#ids = pickle.load( open( "data/3000terms/nsids.pkl", "rb" ) )

articles = dict()
for i in ids:
  if i not in articles.keys():
    articles[i] = pub.getArticle(i)
# Or again, load from file, faster
# articles = pickle.load( open( "data/3000terms/articles.pkl", "rb" ) )

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
outfile = "data/disorder_pid_matrix.txt"
filey = open(outfile,'w')
filey.writelines( "ID\t"+ "\t".join(cols) + "\n")
for r in range(0,len(results)):
  filey.writelines(rows[r] + "\t" + "\t".join([str(x) for x in results[r]]) + "\n")

filey.close()
