#!/usr/bin/env python

"""

NeuroSynth: part of the brainbehavior python package

BrainBehavior: This module will work with three databases that 
combined can make inferences about disorders and behaviors:

NeuroVault: functional and structural group analyses
Cognitive Atlas: ontology of cognitive concepts, tasks, disorder, collections
NeuroSynth: mining literature for behavioral concepts to produce brain maps

SAMPLE USAGE: Please see README included with package


"""

from neurosynth.base.dataset import Dataset
from neurosynth.base.dataset import FeatureTable
from neurosynth.base import mask
from neurosynth.base import imageutils
from neurosynth.analysis import meta
from neurosynth.analysis import decode
import nibabel as nb
from nibabel import nifti1
import re
import pandas as pd

__author__ = ["Vanessa Sochat (vsochat@stanford.edu)"]
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2011/09/09 $"
__license__ = "Python"

# Functions to work with raw database
def get_database(database_size):
  return pd.read_csv("data/%sterms/database.txt" % (database_size),sep="\t")

# NeuroSynth Functions--------------------------------------------------------------
class NeuroSynth:

  """Initialize Neurosynth Database"""
  def __init__(self,dbsize):
    print "Initializing Neurosynth database..."
    self.db = Dataset('data/' + str(dbsize) + 'terms/database.txt')
    self.db.add_features('data/' + str(dbsize) + 'terms/features.txt')
    self.ids = self.getIDs()
    self.decoder = None
    #self.masker = mask.Mask("data/X.nii.gz")

  """Do contrast analysis between two sets of """
  def neurosynthContrast(self,papers1,papers2,fdr,outdir=None,outprefix=None,image_list=None):
    
    # Do a meta analysis to contrast the two
    ma = meta.MetaAnalysis(self.db,papers1,papers2,q=float(fdr))
    if outdir:
      print "Saving results to %s" % (outdir)
      ma.save_results(outdir, prefix=outprefix, prefix_sep='_', image_list=image_list)
    return ma.images
    
  """Conduct meta analysis with particular set of ids"""
  def neurosynthMeta(self,papers,fdr,outdir=None,outprefix=None, image_list=None):
    # Get valid ids from user list
    valid_ids = self.get_valid_ids(papers)

    if (len(valid_ids) > 0):
      # Do meta analysis
      ma = meta.MetaAnalysis(self.db,valid_ids,q=float(fdr))
      if outdir:
        print "Saving results to output directory %s" % (outdir)
        ma.save_results(outdir, prefix=outprefix, prefix_sep='_', image_list=image_list)
      return ma.images
    else:
      print "No studies found in database for ids in question!"

  """Return list of valid ids from user input"""
  def get_valid_ids(self,papers):
  # Input is DOI with list of papers
    valid_ids = [x for x in papers if int(x.strip(" ")) in self.ids]
    print "Found %s valid ids." % (str(len(valid_ids)))
    return valid_ids

  """Decode an image, return 100 results"""
  def decode(self,images,outfile,mrs=None,round=4):
    if not self.decoder:
      self.decoder = decode.Decoder(self.db)

    # If mrs is not specified, do decoding against neurosynth database
    if not mrs:
      result = self.decoder.decode(images, save=outfile)
  
    # If mrs is specified, do decoding against custom set of images
    else:
      # This is akin to traditional neurosynth method - pearson's r correlation
      imgs_to_compare = imageutils.load_imgs(mrs,self.masker)
      imgs_to_decode = imageutils.load_imgs(images,self.masker)
      x, y = imgs_to_compare.astype(float),imgs_to_decode.astype(float)
      x, y = x - x.mean(0), y - y.mean(0)
      x, y = x / np.sqrt((x ** 2).sum(0)), y / np.sqrt((y ** 2).sum(0))
      result = np.around(x.T.dot(y).T,round)
      features = [os.path.basename(m) for m in mrs]
      rownames = [os.path.basename(m) for m in images]
      df = pd.DataFrame(result,columns=features)
      df.index = rownames
      df.to_csv(outfile,sep="\t")
    return result

  """Return features in neurosynth database"""
  def getFeatures(self,dataset):
    return dataset.get_feature_names()

  """Extract pubmed IDs or dois from Neurosynth Database"""
  def getIDs(self):
    # Get all IDs in neuroSynth
    return self.db.image_table.ids


  """Extract author names for a given pmid or doi"""
  def getAuthor(self,db,id):   
   article = self.db.get_mappables(id)
   meta = article[0].__dict__
   tmp = meta['data']['authors']
   tmp = tmp.split(",")
   authors = [ x.strip("^ ") for x in tmp]
   return authors

  """Extract all author names in database"""
  def getAuthors(self,db):
    articles = db.mappables
    uniqueAuthors = []
    for a in articles:
      meta = a.__dict__
      tmp = meta['data']['authors']
      tmp = tmp.split(",")
      authors = [ x.strip("^ ") for x in tmp]
      for a in authors:
        uniqueAuthors.append(a)
    uniqueAuthors = list(np.unique(uniqueAuthors))
    return uniqueAuthors

  """Extract activation points and all meta information for a particular pmid"""
  def getPaperMeta(self,db,pmid):
    articles = db.mappables
    m = []
    for a in articles:
        tmp = a.__dict__
        if tmp['data']['id'] == str(pmid):
          journal = tmp['data']['journal']
          title = tmp['data']['title']
          year = tmp['data']['year']
          doi = tmp['data']['doi']
          auth = tmp['data']['authors']
          peaks = tmp['data']['peaks']
          pmid = tmp['data']['id']
          tmp = (journal,title,year,doi,pmid,auth,peaks)
          m.append(tmp)
    return m
