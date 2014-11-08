#!/usr/bin/env python

"""

Pubmed: part of the brainbehavior python package

BrainBehavior: This module will work with three databases that 
combined can make inferences about disorders and behaviors:

NeuroVault: functional and structural group analyses
Cognitive Atlas: ontology of cognitive concepts, tasks, disorder, collections
NeuroSynth: mining literature for behavioral concepts to produce brain maps

SAMPLE USAGE: Please see README included with package


"""

import numpy as np
import string
import urllib2
import json
from Bio import Entrez
import nltk
from nltk import word_tokenize
import re
import sys
import os.path

__author__ = ["Vanessa Sochat (vsochat@stanford.edu)","Matthew Sacchet (msacchet@stanford.edu)"]
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2011/09/09 $"
__license__ = "Python"

# Pubmed 
# These functions will find papers of interest to crosslist with Neurosynth
class Pubmed:

  def __init__(self,email):
    self.email = email

  """Load pubmed FTP info from pickle"""
  def self.loadPubmed(self):
    self.ftp = pd.io.pickle.read_pickle("data/pubmed/pubmed.pkl")

  """Download full text"""
  # STOPPED HERE - this needs to be a string
  def loadPubmed(self,pmids):
    all_ids = [str(x) for x in self.ftp.PMID]
    valid_ids = [p for p in pmid if p in all_ids]


  """Read articles from pubmed"""
  def getArticle(self,id1):
    Entrez.email = self.email
    handle = Entrez.esearch(db='pubmed',term=id1,retmax=1)
    record = Entrez.read(handle)

    # If we have a match
    if "IdList" in record:
      if record["Count"] != "0":
        # Fetch the paper!
        print "Retrieving paper " + str(id1) + "..."
        handle = Entrez.efetch(db='pubmed', id=id1,retmode='xml',retmax=1)
        record = Entrez.read(handle)
        record = record[0]
        article = Article(record)
      else: 
        print "No articles found for " + str(id1)
    return article

  """Search article for a term of interest - no processing of expression. return 1 if found, 0 if not"""
  def searchArticle(self,article,term):
    text = [article.getAbstract()] + article.getMesh() + article.getKeywords()
    text = text[0].lower()
    expression = re.compile(term)
    # Search abstract for terms, return 1 if found
    found = expression.search(text)
    if found:
      return 1
    else:
      return 0


  """Search article for a term of interest - stem list of words first - return 1 if found, 0 if not"""
  def searchArticleList(self,article,term):
    text = [article.getAbstract()] + article.getMesh() + article.getKeywords()
    text = text[0].lower()
    # Perform stemming of disorder terms
    words = []
    porter = nltk.PorterStemmer()
    [[words.append(str(porter.stem(t))) for t in word_tokenize(x.lower())] for x in term]
    # Get rid of general disease terms
    diseaseterms = ["disord","diseas","of","mental","impuls","control","health","specif","person","cognit","type","form","syndrom","spectrum","eat","depend","development","languag","by","endog","abus"]
    words = filter(lambda x: x not in diseaseterms, words)
    if len(words) > 0:
      # Get unique words
      words = list(set(words))
      term = "|".join([x.strip(" ").lower() for x in words])
      expression = re.compile(term)
      # Search abstract for terms, return 1 if found
      found = expression.search(text)
      if found:
        return 1
      else:
        return 0
    else:
      print "Insufficient search term for term " + str(term)
      return 0

  """Return dictionaries of dois, pmids, each with order based on author name (Last FM)"""
  def getAuthorArticles(self,author):
    
    print "Getting pubmed articles for author " + author
    
    Entrez.email = self.email
    handle = Entrez.esearch(db='pubmed',term=author,retmax=5000)
    record = Entrez.read(handle)

    # If there are papers
    if "IdList" in record:
      if record["Count"] != "0":
        # Fetch the papers
        ids = record['IdList']
        handle = Entrez.efetch(db='pubmed', id=ids,retmode='xml',retmax=5000)
        records = Entrez.read(handle)
        # We need to save dois for database with 525, pmid for newer
        dois = dict(); pmid = dict()
        for record in records:
          authors = record["MedlineCitation"]["Article"]["AuthorList"]
          order = 1
          for p in authors:
            # If it's a collective, won't have a last name
            if "LastName" in p and "Initials" in p:
              person = p["LastName"] + " " + p["Initials"]
              if person == author:

                # Save the pmid of the paper and author order
                # it's possible to get a different number of pmids than dois
                if order == len(authors):
                  pmid[int(record["MedlineCitation"]["PMID"])] = order
                else:
                  pmid[int(record["MedlineCitation"]["PMID"])] = "PI"

                # We have to dig for the doi
                for r in record["PubmedData"]["ArticleIdList"]:
                  # Here is the doi
                  if bool(re.search("[/]",str(r))):
                    # If they are last, they are PI
                    if order == len(authors):
                      dois[str(r)] = "PI"
                    else:
                      pmid[int(record["MedlineCitation"]["PMID"])] = order
                      dois[str(r)] = order

            order = order + 1

      # If there are no papers
      else:
        print "No papers found for author " + author + "!"

    # Return dois, pmids, each with author order
    print "Found " + str(len(pmid)) + " pmids for author " + author + " (for NeuroSynth 3000 database)."
    print "Found " + str(len(dois)) + " dois for author " + author + " (for NeuroSynth 525 database)."
    return (dois, pmid)


"""An articles object holds a pubmed article"""
class Article:

  def __init__(self,record):
    self.parseRecord(record)

  def parseRecord(self,record):
    if "MedlineCitation" in record:
      self.authors = record["MedlineCitation"]["Article"]["AuthorList"]
      if "MeshHeadingList" in record:
        self.mesh = record["MedlineCitation"]["MeshHeadingList"]
      else:
        self.mesh = []
      self.keywords = record["MedlineCitation"]["KeywordList"]
      self.medline = record["MedlineCitation"]["MedlineJournalInfo"]
      self.journal = record["MedlineCitation"]["Article"]["Journal"]
      self.title = record["MedlineCitation"]["Article"]["ArticleTitle"]
      self.year = record["MedlineCitation"]["Article"]["ArticleTitle"]
      if "Abstract" in record["MedlineCitation"]["Article"]:
        self.abstract = record["MedlineCitation"]["Article"]["Abstract"]
      else:
        self.abstract = ""

  """get Abstract text"""
  def getAbstract(self):
    if "AbstractText" in self.abstract:
      return self.abstract["AbstractText"][0]
    else:
      return ""

  """get mesh terms"""
  def getMesh(self):
    return [ str(x["DescriptorName"]).lower() for x in self.mesh]

  """get keywords"""
  def getKeywords(self):
    return self.keywords

