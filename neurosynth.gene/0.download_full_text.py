#!/usr/bin/env python2

# This script will use the BrainBehavior.py module to find NeuroSynth papers with pubmed central (full text available) and then parse them for genes defined for a subset of 86 neurological disorders defined via malacards (mental disorders) and phenopedia (genes).  The result should be a matrix of genes by papers.

import brainbehavior.neurosyn
import brainbehavior.pubmed
import numpy as np
import re

# Read in the raw neurosynth data
data = neurosyn.get_database("8000")

# Search by title
papers = np.unique(data["title"])

# Use pubmed to look up dois
email = "vsochat@gmail.com"
pm = pubmed.Pubmed(email)

# Let's save articles here
articles = []
for paper in papers:
  articles.append(pm.get_single_article(paper))

# Save to pickle object
import pickle
pickle.dump(articles, open( "data/8000terms/articles.pkl", "wb" ) )

expression = re.compile("PMC[0-9]")

# Now for each, find the pubmed ids
pmcids = []
for a in range(0,len(articles)):
  article = articles[a]
  if article:
    print "%s of %s" %(a,len(articles))
    pmcid = [str(x) for x in article.ids if expression.match(str(x))]
    if pmcid:
      pmcids.append(pmcid[0])

pmcids = list(np.unique(pmcids))
pickle.dump(pmcids, open( "data/8000terms/pmcids_3122.pkl", "wb" ) )

# For each pubmed id, download
download_folder = "/home/vanessa/Documents/Work/PUBMED"
central_ids = pm.get_pubmed_central_ids()
pm.download_pubmed(pmcids,download_folder)
